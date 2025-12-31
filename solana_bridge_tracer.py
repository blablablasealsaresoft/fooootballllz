#!/usr/bin/env python3
"""
SOLANA 5-HOP BRIDGE TRACER
===========================
Traces USDC deposits from Solana through Wormhole/Allbridge to Polygon Polymarket wallets.
Identifies original funding sources with multi-hop analysis.

REQUIREMENTS:
pip install solana solders base58 requests aiohttp

USAGE:
python solana_bridge_tracer.py --polygon-address 0x123... --hops 5
python solana_bridge_tracer.py --tx-hash 0xabc... --trace-back
"""

import requests
import json
import time
import argparse
import base58
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
SOLANA_RPC_BACKUP = "https://solana-api.projectserum.com"

# Known addresses
USDC_MINT_SOLANA = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDT_MINT_SOLANA = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"

# Wormhole addresses
WORMHOLE_TOKEN_BRIDGE_SOLANA = "wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb"
WORMHOLE_CORE_BRIDGE_SOLANA = "worm2ZoG2kUd4vFXhvjh93UUH596ayRfgQ2MgjNMTth"

# Known CEX hot wallets on Solana
SOLANA_CEX_WALLETS = {
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM": "Binance",
    "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9": "Binance",
    "2ojv9BAiHUrvsm9gxDe7fJSzbNZSJcxZvf8dqmWGHG8S": "Binance",
    "AC5RDfQFmDS1deWZos921JfqscXdByf8BKHs5ACWjtW2": "Coinbase",
    "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE": "Coinbase Prime",
    "H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS": "FTX (defunct)",
    "CuieVDEDtLo7FypA9SbLM9saXFdb1dsshEkyErMqkRQq": "Kraken",
    "FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5": "Kraken",
    "ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ": "OKX",
    "5VCwKtCXgCJ6kit5FybXjvriW3xELsFDhYrPSqtJNmcD": "Gate.io",
}

# Known DeFi protocols on Solana
SOLANA_DEFI_PROTOCOLS = {
    "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin": "Serum DEX",
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "Orca Whirlpool",
    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "Raydium CLMM",
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "Raydium AMM",
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "Jupiter",
    "MERLuDFBMmsHnsBPZw2sDQZHvXFMwp8EdjudcU2HKky": "Mercurial",
}

# Bridge contracts
BRIDGE_CONTRACTS = {
    "wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb": "Wormhole Token Bridge",
    "3u8hJUVTA4jH1wYAyUur7FFZVQ8H635K3tSHHF4ssjQ5": "Allbridge Core",
    "br1xwubggTiEZ6b7iNZUwfA3psygFfaXGfZ1heaN9AW": "Allbridge",
}


# ============================================================================
# SOLANA CLIENT
# ============================================================================

class SolanaTracer:
    """Advanced Solana blockchain tracer"""
    
    def __init__(self, rpc_url: str = SOLANA_RPC):
        self.rpc_url = rpc_url
        self.session = requests.Session()
        self.cache = {}
    
    def _rpc_call(self, method: str, params: list) -> Optional[Dict]:
        """Make RPC call to Solana"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        try:
            resp = self.session.post(self.rpc_url, json=payload, timeout=30)
            data = resp.json()
            
            if "error" in data:
                print(f"  [RPC Error] {data['error']}")
                return None
            
            return data.get("result")
        except Exception as e:
            print(f"  [Error] RPC call failed: {e}")
            return None
    
    def get_signatures_for_address(self, address: str, limit: int = 100, 
                                   before: str = None) -> List[Dict]:
        """Get transaction signatures for an address"""
        params = [address, {"limit": limit}]
        if before:
            params[1]["before"] = before
        
        result = self._rpc_call("getSignaturesForAddress", params)
        return result or []
    
    def get_transaction(self, signature: str) -> Optional[Dict]:
        """Get full transaction details"""
        if signature in self.cache:
            return self.cache[signature]
        
        result = self._rpc_call("getTransaction", [
            signature,
            {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
        ])
        
        if result:
            self.cache[signature] = result
        
        return result
    
    def get_token_accounts_by_owner(self, owner: str) -> List[Dict]:
        """Get all token accounts owned by address"""
        result = self._rpc_call("getTokenAccountsByOwner", [
            owner,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ])
        
        return result.get("value", []) if result else []
    
    def get_account_info(self, address: str) -> Optional[Dict]:
        """Get account information"""
        result = self._rpc_call("getAccountInfo", [
            address,
            {"encoding": "jsonParsed"}
        ])
        return result.get("value") if result else None
    
    def parse_token_transfers(self, tx: Dict) -> List[Dict]:
        """Extract token transfers from a transaction"""
        transfers = []
        
        if not tx:
            return transfers
        
        meta = tx.get("meta", {})
        
        # Pre and post token balances
        pre_balances = {b["accountIndex"]: b for b in meta.get("preTokenBalances", [])}
        post_balances = {b["accountIndex"]: b for b in meta.get("postTokenBalances", [])}
        
        # Find changes
        all_indices = set(pre_balances.keys()) | set(post_balances.keys())
        
        for idx in all_indices:
            pre = pre_balances.get(idx, {})
            post = post_balances.get(idx, {})
            
            pre_amount = float(pre.get("uiTokenAmount", {}).get("uiAmount") or 0)
            post_amount = float(post.get("uiTokenAmount", {}).get("uiAmount") or 0)
            
            diff = post_amount - pre_amount
            
            if abs(diff) > 0.01:  # Significant change
                mint = post.get("mint") or pre.get("mint")
                owner = post.get("owner") or pre.get("owner")
                
                transfers.append({
                    "mint": mint,
                    "owner": owner,
                    "amount_change": diff,
                    "pre_amount": pre_amount,
                    "post_amount": post_amount,
                    "is_usdc": mint == USDC_MINT_SOLANA,
                    "is_usdt": mint == USDT_MINT_SOLANA,
                })
        
        return transfers
    
    def parse_sol_transfers(self, tx: Dict) -> List[Dict]:
        """Extract SOL transfers from a transaction"""
        transfers = []
        
        if not tx:
            return transfers
        
        meta = tx.get("meta", {})
        message = tx.get("transaction", {}).get("message", {})
        
        pre_balances = meta.get("preBalances", [])
        post_balances = meta.get("postBalances", [])
        account_keys = message.get("accountKeys", [])
        
        for i, (pre, post) in enumerate(zip(pre_balances, post_balances)):
            diff = (post - pre) / 1e9  # Lamports to SOL
            
            if abs(diff) > 0.001:
                pubkey = account_keys[i] if i < len(account_keys) else "unknown"
                if isinstance(pubkey, dict):
                    pubkey = pubkey.get("pubkey", "unknown")
                
                transfers.append({
                    "address": pubkey,
                    "sol_change": diff,
                    "direction": "IN" if diff > 0 else "OUT"
                })
        
        return transfers
    
    def identify_address_type(self, address: str) -> str:
        """Identify what type of address this is"""
        if address in SOLANA_CEX_WALLETS:
            return f"CEX: {SOLANA_CEX_WALLETS[address]}"
        
        if address in SOLANA_DEFI_PROTOCOLS:
            return f"DeFi: {SOLANA_DEFI_PROTOCOLS[address]}"
        
        if address in BRIDGE_CONTRACTS:
            return f"Bridge: {BRIDGE_CONTRACTS[address]}"
        
        # Check if it's a program
        account_info = self.get_account_info(address)
        if account_info:
            if account_info.get("executable"):
                return "Program"
            
            owner = account_info.get("owner")
            if owner == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
                return "Token Account"
        
        return "EOA (User Wallet)"


# ============================================================================
# 5-HOP ANALYSIS
# ============================================================================

class FiveHopAnalyzer:
    """Performs 5-hop analysis to trace funding sources"""
    
    def __init__(self):
        self.tracer = SolanaTracer()
        self.visited = set()
        self.funding_graph = defaultdict(list)
        self.cex_sources = []
        self.bridge_sources = []
        self.defi_interactions = []
    
    def trace_address(self, start_address: str, max_hops: int = 5,
                     min_amount: float = 100) -> Dict:
        """
        Perform N-hop trace starting from an address.
        Follows USDC transfers backwards to find original sources.
        """
        print(f"\n{'='*60}")
        print(f"STARTING 5-HOP TRACE FOR: {start_address[:20]}...")
        print(f"{'='*60}")
        
        result = {
            "start_address": start_address,
            "hops": [],
            "cex_sources": [],
            "bridge_sources": [],
            "defi_sources": [],
            "unknown_sources": [],
            "total_usdc_traced": 0,
            "total_sol_traced": 0,
        }
        
        current_addresses = [(start_address, 0, None)]  # (address, depth, parent_tx)
        
        for hop in range(max_hops):
            print(f"\n[HOP {hop + 1}/{max_hops}]")
            print(f"  Analyzing {len(current_addresses)} addresses...")
            
            next_addresses = []
            hop_data = {
                "hop_number": hop + 1,
                "addresses_analyzed": 0,
                "transfers_found": 0,
                "sources_identified": []
            }
            
            for address, depth, parent_tx in current_addresses:
                if address in self.visited:
                    continue
                self.visited.add(address)
                hop_data["addresses_analyzed"] += 1
                
                print(f"    Tracing: {address[:16]}...")
                
                # Identify address type first
                addr_type = self.tracer.identify_address_type(address)
                print(f"      Type: {addr_type}")
                
                # Check if we've hit a source
                if "CEX" in addr_type:
                    source = {
                        "address": address,
                        "type": addr_type,
                        "hop": hop + 1,
                        "parent_tx": parent_tx
                    }
                    result["cex_sources"].append(source)
                    hop_data["sources_identified"].append(source)
                    print(f"      [!] CEX SOURCE FOUND: {addr_type}")
                    continue
                
                if "Bridge" in addr_type:
                    source = {
                        "address": address,
                        "type": addr_type,
                        "hop": hop + 1,
                        "parent_tx": parent_tx
                    }
                    result["bridge_sources"].append(source)
                    hop_data["sources_identified"].append(source)
                    print(f"      [!] BRIDGE SOURCE FOUND: {addr_type}")
                    continue
                
                if "DeFi" in addr_type:
                    source = {
                        "address": address,
                        "type": addr_type,
                        "hop": hop + 1
                    }
                    result["defi_sources"].append(source)
                    print(f"      [~] DeFi interaction: {addr_type}")
                
                # Get transaction history
                signatures = self.tracer.get_signatures_for_address(address, limit=50)
                
                for sig_info in signatures[:20]:  # Limit per address
                    sig = sig_info.get("signature")
                    
                    tx = self.tracer.get_transaction(sig)
                    if not tx:
                        continue
                    
                    # Parse transfers
                    token_transfers = self.tracer.parse_token_transfers(tx)
                    sol_transfers = self.tracer.parse_sol_transfers(tx)
                    
                    # Look for incoming USDC/USDT
                    for transfer in token_transfers:
                        if transfer["amount_change"] > min_amount:
                            if transfer["is_usdc"] or transfer["is_usdt"]:
                                hop_data["transfers_found"] += 1
                                result["total_usdc_traced"] += transfer["amount_change"]
                                
                                # Find the sender
                                sender = self._find_sender(tx, transfer)
                                if sender and sender not in self.visited:
                                    next_addresses.append((sender, depth + 1, sig))
                                    
                                    self.funding_graph[address].append({
                                        "from": sender,
                                        "amount": transfer["amount_change"],
                                        "token": "USDC" if transfer["is_usdc"] else "USDT",
                                        "tx": sig
                                    })
                    
                    # Also track large SOL transfers
                    for transfer in sol_transfers:
                        if transfer["sol_change"] > 1 and transfer["direction"] == "IN":
                            result["total_sol_traced"] += transfer["sol_change"]
                    
                    time.sleep(0.1)  # Rate limiting
                
                time.sleep(0.3)  # Rate limiting between addresses
            
            result["hops"].append(hop_data)
            current_addresses = next_addresses[:30]  # Limit branching
            
            if not current_addresses:
                print(f"\n  [!] No more addresses to trace after hop {hop + 1}")
                break
        
        # Identify any remaining unknown sources
        for addr in self.visited:
            addr_type = self.tracer.identify_address_type(addr)
            if addr_type == "EOA (User Wallet)":
                # Check if this is a leaf node (no incoming we found)
                if addr not in [a for addrs in self.funding_graph.values() for a in [x["from"] for x in addrs]]:
                    if addr != start_address:
                        result["unknown_sources"].append({
                            "address": addr,
                            "type": "Unknown Origin"
                        })
        
        return result
    
    def _find_sender(self, tx: Dict, transfer: Dict) -> Optional[str]:
        """Find the sender of a token transfer"""
        meta = tx.get("meta", {})
        
        # Look through inner instructions for transfer info
        inner_instructions = meta.get("innerInstructions", [])
        
        for inner in inner_instructions:
            for inst in inner.get("instructions", []):
                parsed = inst.get("parsed", {})
                if parsed.get("type") == "transfer":
                    info = parsed.get("info", {})
                    # This might be the transfer
                    if info.get("destination"):
                        source = info.get("source") or info.get("authority")
                        if source:
                            return source
        
        # Fallback: look at account keys
        message = tx.get("transaction", {}).get("message", {})
        account_keys = message.get("accountKeys", [])
        
        # Usually the first non-program account is the signer/sender
        for key in account_keys:
            if isinstance(key, dict):
                pubkey = key.get("pubkey")
                if key.get("signer") and not key.get("writable") == False:
                    return pubkey
            elif isinstance(key, str):
                return key
        
        return None
    
    def generate_funding_tree(self) -> str:
        """Generate ASCII visualization of funding tree"""
        tree = "\n[FUNDING TREE]\n"
        
        def print_branch(address: str, indent: int = 0):
            nonlocal tree
            prefix = "  " * indent + ("└── " if indent > 0 else "")
            addr_type = self.tracer.identify_address_type(address)
            tree += f"{prefix}{address[:16]}... ({addr_type})\n"
            
            for funding in self.funding_graph.get(address, []):
                tree += f"{'  ' * (indent + 1)}├── ${funding['amount']:,.2f} {funding['token']}\n"
                if funding["from"] not in self.visited or indent < 3:
                    print_branch(funding["from"], indent + 2)
        
        # Start from addresses that have incoming funding
        roots = set(self.funding_graph.keys())
        for root in list(roots)[:5]:
            print_branch(root)
        
        return tree


# ============================================================================
# WORMHOLE BRIDGE TRACER
# ============================================================================

class WormholeTracer:
    """Traces transactions through Wormhole bridge"""
    
    def __init__(self):
        self.api_base = "https://api.wormholescan.io/api/v1"
        self.session = requests.Session()
    
    def get_vaa_by_tx(self, tx_hash: str, chain: str = "polygon") -> Optional[Dict]:
        """Get VAA (Verified Action Approval) by transaction hash"""
        try:
            # Try to find the VAA
            url = f"{self.api_base}/vaas"
            params = {"txHash": tx_hash}
            
            resp = self.session.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("data"):
                    return data["data"][0]
        except Exception as e:
            print(f"  [Wormhole API Error] {e}")
        
        return None
    
    def trace_to_source_chain(self, vaa: Dict) -> Optional[Dict]:
        """Trace a VAA back to its source chain"""
        if not vaa:
            return None
        
        source_chain = vaa.get("emitterChain")
        
        # Chain IDs: 1=Solana, 2=Ethereum, 5=Polygon, etc.
        chain_names = {
            1: "Solana",
            2: "Ethereum",
            4: "BSC",
            5: "Polygon",
            6: "Avalanche",
            7: "Oasis",
            10: "Fantom",
            13: "Klaytn",
            14: "Celo",
            16: "Moonbeam",
            21: "Sui",
            22: "Aptos",
            23: "Arbitrum",
            24: "Optimism",
            30: "Base",
        }
        
        return {
            "source_chain": chain_names.get(source_chain, f"Unknown ({source_chain})"),
            "source_chain_id": source_chain,
            "emitter_address": vaa.get("emitterAddr"),
            "sequence": vaa.get("sequence"),
            "timestamp": vaa.get("timestamp"),
            "payload": vaa.get("payload"),
        }
    
    def get_recent_transfers(self, address: str = None, limit: int = 20) -> List[Dict]:
        """Get recent Wormhole transfers"""
        try:
            url = f"{self.api_base}/operations"
            params = {"limit": limit}
            if address:
                params["address"] = address
            
            resp = self.session.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("operations", [])
        except Exception as e:
            print(f"  [Wormhole API Error] {e}")
        
        return []


# ============================================================================
# POLYGON -> SOLANA TRACE
# ============================================================================

def trace_polygon_to_solana(polygon_address: str, polygon_tx: str = None) -> Dict:
    """
    Complete trace from Polygon Polymarket wallet back to Solana source.
    """
    print(f"\n{'='*70}")
    print("POLYGON -> SOLANA BRIDGE TRACE")
    print(f"{'='*70}")
    print(f"Target: {polygon_address}")
    
    result = {
        "polygon_address": polygon_address,
        "bridge_transactions": [],
        "solana_sources": [],
        "complete_path": []
    }
    
    # Initialize tracers
    wormhole = WormholeTracer()
    solana_analyzer = FiveHopAnalyzer()
    
    # Step 1: Find bridge transactions on Polygon side
    print("\n[Step 1] Searching for bridge deposits to this address...")
    
    # If we have a specific tx, trace it
    if polygon_tx:
        vaa = wormhole.get_vaa_by_tx(polygon_tx)
        if vaa:
            source_info = wormhole.trace_to_source_chain(vaa)
            result["bridge_transactions"].append({
                "polygon_tx": polygon_tx,
                "vaa": vaa,
                "source": source_info
            })
            
            if source_info and source_info["source_chain"] == "Solana":
                print(f"\n[Step 2] Found Solana source! Tracing back...")
                
                # Trace on Solana side
                solana_result = solana_analyzer.trace_address(
                    source_info["emitter_address"],
                    max_hops=5
                )
                result["solana_sources"].append(solana_result)
    
    # Step 2: Get recent Wormhole operations
    print("\n[Step 2] Checking recent Wormhole transfers...")
    recent_ops = wormhole.get_recent_transfers(limit=50)
    
    for op in recent_ops:
        target = op.get("targetChain", {})
        if target.get("chainId") == 5:  # Polygon
            # Check if destination matches our address
            dest = op.get("data", {}).get("tokenTransferPayload", {}).get("toAddress")
            if dest and dest.lower() == polygon_address.lower():
                print(f"  [!] Found matching transfer!")
                
                source_chain = op.get("sourceChain", {})
                if source_chain.get("chainId") == 1:  # Solana
                    source_addr = op.get("data", {}).get("tokenTransferPayload", {}).get("fromAddress")
                    if source_addr:
                        print(f"\n[Step 3] Tracing Solana source: {source_addr[:20]}...")
                        
                        solana_result = solana_analyzer.trace_address(
                            source_addr,
                            max_hops=5
                        )
                        result["solana_sources"].append(solana_result)
    
    # Generate funding tree visualization
    if result["solana_sources"]:
        result["funding_tree"] = solana_analyzer.generate_funding_tree()
    
    return result


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Solana 5-Hop Bridge Tracer")
    parser.add_argument("--polygon-address", type=str,
                       help="Polygon address to trace back")
    parser.add_argument("--solana-address", type=str,
                       help="Direct Solana address to trace")
    parser.add_argument("--tx-hash", type=str,
                       help="Specific transaction to trace")
    parser.add_argument("--hops", type=int, default=5,
                       help="Number of hops to trace")
    parser.add_argument("--output", type=str, default="solana_trace_report.json",
                       help="Output file")
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    SOLANA 5-HOP BRIDGE TRACER                                 ║
║              Trace Polymarket deposits back to original source                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    result = {}
    
    if args.polygon_address:
        result = trace_polygon_to_solana(args.polygon_address, args.tx_hash)
    
    elif args.solana_address:
        analyzer = FiveHopAnalyzer()
        result = analyzer.trace_address(args.solana_address, max_hops=args.hops)
        result["funding_tree"] = analyzer.generate_funding_tree()
    
    else:
        # Demo mode - trace a known whale address
        print("[Demo Mode] Using example whale address...")
        analyzer = FiveHopAnalyzer()
        
        # Example: Trace a random active Solana USDC holder
        demo_address = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"  # Binance
        result = analyzer.trace_address(demo_address, max_hops=3)
        result["funding_tree"] = analyzer.generate_funding_tree()
    
    # Generate report
    print("\n" + "="*70)
    print("TRACE RESULTS")
    print("="*70)
    
    if result.get("cex_sources"):
        print("\n[CEX SOURCES IDENTIFIED]")
        for src in result["cex_sources"]:
            print(f"  • {src['type']} - {src['address'][:20]}... (hop {src['hop']})")
    
    if result.get("bridge_sources"):
        print("\n[BRIDGE SOURCES IDENTIFIED]")
        for src in result["bridge_sources"]:
            print(f"  • {src['type']} - {src['address'][:20]}... (hop {src['hop']})")
    
    if result.get("defi_sources"):
        print("\n[DEFI INTERACTIONS]")
        for src in result["defi_sources"][:5]:
            print(f"  • {src['type']} - {src['address'][:20]}...")
    
    if result.get("funding_tree"):
        print(result["funding_tree"])
    
    print(f"\n[SUMMARY]")
    print(f"  Total USDC Traced: ${result.get('total_usdc_traced', 0):,.2f}")
    print(f"  Total SOL Traced: {result.get('total_sol_traced', 0):,.2f} SOL")
    print(f"  Hops Completed: {len(result.get('hops', []))}")
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n[+] Results saved to: {args.output}")


if __name__ == "__main__":
    main()
