#!/usr/bin/env python3
"""
POLYMARKET WHALE FINDER - SIMPLE VERSION
=========================================
Uses YOUR Etherscan V2 API key to find whale positions.

JUST RUN:
    python whale_finder.py

Or with a specific wallet:
    python whale_finder.py 0xYourWalletAddress
"""

import requests
import json
import time
import sys
from datetime import datetime
from collections import defaultdict

# ============================================================================
# YOUR API KEY - ALREADY CONFIGURED
# ============================================================================
ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

# Etherscan V2 = ONE KEY FOR ALL CHAINS
# Chain IDs: Polygon=137, Ethereum=1, Arbitrum=42161, Base=8453, Optimism=10
ETHERSCAN_V2 = "https://api.etherscan.io/v2/api"

# Polymarket = Polygon (Chain ID 137)
POLYGON = 137

# Contracts
POLYMARKET_CTF = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"
POLYMARKET_NEG_RISK = "0xC5d563A36AE78145C45a50134d48A1215220f80a"
USDC_POLYGON = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
USDC_BRIDGED = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# Known CEX wallets on Polygon
CEX_WALLETS = {
    "0x28c6c06298d514db089934071355e5743bf21d60": "Binance 14",
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Binance 15",
    "0xf89d7b9c864f589bbf53a82105107622b35eaa40": "Binance 16",
    "0x56eddb7aa87536c09ccc2793473599fd21a8b17f": "Coinbase 4",
    "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43": "Coinbase 10",
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3": "Coinbase 3",
    "0x0d0707963952f2fba59dd06f2b425ace40b492fe": "Gate.io",
    "0x6262998ced04146fa42253a5c0af90ca02dfd2a3": "Crypto.com 1",
    "0x46340b20830761efd32832a74d7169b29feb9758": "Crypto.com 2",
    "0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98": "Bitget",
    "0x5f65f7b609678448494de4c87521cdf6cef1e932": "OKX",
    "0x3c783c21a0383057d128bae431894a5c19f9cf06": "Bybit",
    "0xf977814e90da44bfa03b6295a0616a897441acec": "Binance 8",
    "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf": "Polygon Bridge",
    "0x5a58505a96d1dbf8df91cb21b54419fc36e93fde": "Wormhole Bridge",
}

# ============================================================================
# API FUNCTIONS
# ============================================================================

def api_call(chain_id, module, action, **kwargs):
    """Make Etherscan V2 API call"""
    params = {
        "chainid": chain_id,
        "module": module,
        "action": action,
        "apikey": ETHERSCAN_API_KEY,
        **kwargs
    }
    
    try:
        time.sleep(0.25)  # Rate limit: 5/sec
        resp = requests.get(ETHERSCAN_V2, params=params, timeout=30)
        data = resp.json()
        
        if data.get("status") == "1":
            return data.get("result")
        else:
            print(f"  [!] API: {data.get('message', 'Error')}")
            return None
    except Exception as e:
        print(f"  [!] Request failed: {e}")
        return None


def get_usdc_balance(address):
    """Get USDC balance on Polygon"""
    result = api_call(POLYGON, "account", "tokenbalance",
                     contractaddress=USDC_POLYGON,
                     address=address,
                     tag="latest")
    if result:
        return int(result) / 1e6
    return 0


def get_matic_balance(address):
    """Get MATIC balance"""
    result = api_call(POLYGON, "account", "balance",
                     address=address,
                     tag="latest")
    if result:
        return int(result) / 1e18
    return 0


def get_token_transfers(address, contract=USDC_POLYGON):
    """Get ERC20 token transfers"""
    return api_call(POLYGON, "account", "tokentx",
                   address=address,
                   contractaddress=contract,
                   startblock=0,
                   endblock=99999999,
                   sort="desc") or []


def get_transactions(address):
    """Get normal transactions"""
    return api_call(POLYGON, "account", "txlist",
                   address=address,
                   startblock=0,
                   endblock=99999999,
                   sort="desc") or []


def identify_address(address):
    """Identify if address is CEX/Bridge/EOA"""
    addr = address.lower()
    if addr in CEX_WALLETS:
        return CEX_WALLETS[addr]
    return "EOA"


# ============================================================================
# WHALE ANALYSIS
# ============================================================================

def trace_funding(address, max_hops=5, min_amount=100):
    """Trace wallet funding sources through N hops"""
    print(f"\n{'='*60}")
    print(f"TRACING: {address}")
    print(f"{'='*60}")
    
    results = {
        "address": address,
        "cex_sources": [],
        "bridge_sources": [],
        "total_inflow": 0,
        "funding_path": []
    }
    
    visited = set()
    current = [(address, 0)]  # (address, depth)
    
    for hop in range(max_hops):
        if not current:
            break
            
        print(f"\n[HOP {hop+1}] Analyzing {len(current)} addresses...")
        next_addrs = []
        
        for addr, depth in current:
            if addr.lower() in visited:
                continue
            visited.add(addr.lower())
            
            addr_type = identify_address(addr)
            print(f"  → {addr[:16]}... ({addr_type})")
            
            # Check if we hit a source
            if "Binance" in addr_type or "Coinbase" in addr_type or "OKX" in addr_type:
                results["cex_sources"].append({"address": addr, "exchange": addr_type, "hop": hop+1})
                print(f"    [!] CEX FOUND: {addr_type}")
                continue
            
            if "Bridge" in addr_type:
                results["bridge_sources"].append({"address": addr, "bridge": addr_type, "hop": hop+1})
                print(f"    [!] BRIDGE FOUND: {addr_type}")
                continue
            
            # Get incoming USDC transfers
            transfers = get_token_transfers(addr, USDC_POLYGON)
            transfers += get_token_transfers(addr, USDC_BRIDGED)
            
            incoming = 0
            for tx in transfers:
                if tx.get("to", "").lower() == addr.lower():
                    value = int(tx.get("value", 0)) / 1e6
                    if value >= min_amount:
                        incoming += value
                        from_addr = tx.get("from", "")
                        
                        results["funding_path"].append({
                            "from": from_addr,
                            "to": addr,
                            "amount": value,
                            "tx": tx.get("hash"),
                            "hop": hop + 1
                        })
                        
                        if from_addr.lower() not in visited:
                            next_addrs.append((from_addr, depth+1))
            
            results["total_inflow"] += incoming
            print(f"    Incoming USDC: ${incoming:,.2f}")
        
        current = list(set(next_addrs))[:15]  # Limit branching
    
    return results


def find_polymarket_whales(min_balance=10000):
    """Find active Polymarket traders with high balances"""
    print("\n" + "="*60)
    print("FINDING POLYMARKET WHALES")
    print("="*60)
    
    # Get recent transactions to Polymarket
    print("\n[1] Fetching recent Polymarket activity...")
    txs = api_call(POLYGON, "account", "txlist",
                  address=POLYMARKET_CTF,
                  page=1, offset=200, sort="desc")
    
    if not txs:
        print("  Failed to fetch transactions")
        return []
    
    print(f"  Found {len(txs)} recent transactions")
    
    # Extract unique traders
    traders = set()
    for tx in txs:
        from_addr = tx.get("from", "")
        if from_addr.lower() != POLYMARKET_CTF.lower():
            traders.add(from_addr)
    
    print(f"  Found {len(traders)} unique traders")
    
    # Check balances
    print(f"\n[2] Checking USDC balances (threshold: ${min_balance:,})...")
    
    whales = []
    for i, trader in enumerate(list(traders)[:50]):  # Check top 50
        balance = get_usdc_balance(trader)
        
        if balance >= min_balance:
            whales.append({
                "address": trader,
                "usdc_balance": balance
            })
            print(f"  🐋 WHALE: {trader[:16]}... = ${balance:,.2f}")
        
        if (i+1) % 10 == 0:
            print(f"  Checked {i+1}/{min(50, len(traders))}...")
    
    print(f"\n[3] Found {len(whales)} whales with >= ${min_balance:,} USDC")
    return whales


def analyze_whale(address):
    """Complete analysis of a single whale"""
    print("\n" + "="*60)
    print(f"WHALE ANALYSIS: {address}")
    print("="*60)
    
    result = {
        "address": address,
        "timestamp": datetime.now().isoformat(),
        "balances": {},
        "funding": {},
        "risk_flags": [],
        "risk_score": 0
    }
    
    # Balances
    print("\n[1] Checking balances...")
    usdc = get_usdc_balance(address)
    matic = get_matic_balance(address)
    
    result["balances"]["usdc"] = usdc
    result["balances"]["matic"] = matic
    
    print(f"  USDC: ${usdc:,.2f}")
    print(f"  MATIC: {matic:.4f}")
    
    if usdc > 50000:
        result["risk_flags"].append("HIGH_BALANCE")
        result["risk_score"] += 25
    
    # Polymarket activity
    print("\n[2] Checking Polymarket activity...")
    txs = get_transactions(address)
    
    poly_txs = [t for t in txs if t.get("to", "").lower() in [
        POLYMARKET_CTF.lower(),
        POLYMARKET_NEG_RISK.lower()
    ]]
    
    print(f"  Polymarket transactions: {len(poly_txs)}")
    
    if len(poly_txs) > 100:
        result["risk_flags"].append("HIGH_ACTIVITY")
        result["risk_score"] += 15
    
    # Trace funding
    print("\n[3] Tracing funding (5 hops)...")
    funding = trace_funding(address, max_hops=5)
    result["funding"] = funding
    
    if funding["cex_sources"]:
        exchanges = [s["exchange"] for s in funding["cex_sources"]]
        result["risk_flags"].append(f"CEX_FUNDED: {', '.join(set(exchanges))}")
        result["risk_score"] += 10
    
    if funding["bridge_sources"]:
        result["risk_flags"].append("BRIDGE_FUNDED")
        result["risk_score"] += 30  # Harder to trace = higher risk
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Risk Score: {result['risk_score']}/100")
    print(f"  Flags: {result['risk_flags']}")
    print(f"  Total USDC Inflow: ${funding['total_inflow']:,.2f}")
    print(f"  CEX Sources: {len(funding['cex_sources'])}")
    print(f"  Bridge Sources: {len(funding['bridge_sources'])}")
    
    return result


def find_clusters(wallets):
    """Find wallet clusters by common funding source"""
    print("\n" + "="*60)
    print(f"CLUSTER ANALYSIS: {len(wallets)} wallets")
    print("="*60)
    
    source_to_wallets = defaultdict(set)
    
    for wallet in wallets:
        print(f"\n  Analyzing {wallet[:16]}...")
        transfers = get_token_transfers(wallet, USDC_POLYGON)
        
        for tx in transfers:
            if tx.get("to", "").lower() == wallet.lower():
                source = tx.get("from", "").lower()
                value = int(tx.get("value", 0)) / 1e6
                if value >= 100:
                    source_to_wallets[source].add(wallet)
    
    # Find clusters
    clusters = []
    for source, funded_wallets in source_to_wallets.items():
        if len(funded_wallets) >= 2:
            source_type = identify_address(source)
            clusters.append({
                "source": source,
                "source_type": source_type,
                "wallets": list(funded_wallets),
                "count": len(funded_wallets)
            })
            print(f"\n  [!] CLUSTER: {len(funded_wallets)} wallets from {source_type}")
            print(f"      Source: {source[:20]}...")
    
    return clusters


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              POLYMARKET WHALE FINDER - ETHERSCAN V2                           ║
║                   Your API Key: I47C92D1...YEPJ                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if wallet address provided
    if len(sys.argv) > 1:
        wallet = sys.argv[1]
        print(f"Analyzing specific wallet: {wallet}")
        result = analyze_whale(wallet)
        
        # Save result
        with open("whale_analysis.json", "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n[+] Results saved to whale_analysis.json")
        
    else:
        # Find whales
        print("Mode: Find all whales")
        print("(Pass a wallet address as argument to analyze specific wallet)")
        
        whales = find_polymarket_whales(min_balance=10000)
        
        if whales:
            print(f"\n\nFound {len(whales)} whales. Analyzing top 5...")
            
            results = []
            for whale in whales[:5]:
                result = analyze_whale(whale["address"])
                results.append(result)
            
            # Find clusters
            if len(whales) >= 3:
                clusters = find_clusters([w["address"] for w in whales[:20]])
            else:
                clusters = []
            
            # Save results
            output = {
                "timestamp": datetime.now().isoformat(),
                "whales": results,
                "clusters": clusters
            }
            
            with open("whale_report.json", "w") as f:
                json.dump(output, f, indent=2, default=str)
            
            print(f"\n[+] Results saved to whale_report.json")
            
            # Print summary
            print("\n" + "="*60)
            print("FINAL SUMMARY")
            print("="*60)
            print(f"Whales Found: {len(whales)}")
            print(f"Analyzed: {len(results)}")
            print(f"Clusters Found: {len(clusters)}")
            
            if clusters:
                print("\nCLUSTERS:")
                for c in clusters:
                    print(f"  • {c['count']} wallets from {c['source_type']}")


if __name__ == "__main__":
    main()
