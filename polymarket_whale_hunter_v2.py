#!/usr/bin/env python3
"""
POLYMARKET WHALE HUNTER v2 - Multi-Chain Edition
=================================================
Enhanced with Etherscan V2 API for 60+ chain support.

USAGE:
python polymarket_whale_hunter_v2.py --market "super-bowl" --min-position 10000
python polymarket_whale_hunter_v2.py --whale-address 0x123... --trace
"""

import requests
import json
import time
import argparse
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional

# Import multi-chain tracer
try:
    from multichain_whale_tracer import (
        MultiChainTracer, PolymarketWhaleAnalyzer, EtherscanV2Client,
        SUPPORTED_CHAINS, CEX_ADDRESSES, BRIDGE_CONTRACTS, ETHERSCAN_API_KEY
    )
except ImportError:
    print("[!] Run this from same directory as multichain_whale_tracer.py")
    ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

POLYMARKET_GAMMA_API = "https://gamma-api.polymarket.com"
POLYMARKET_CLOB_API = "https://clob.polymarket.com"

class PolymarketClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "WhaleHunter/2.0"})
    
    def search_markets(self, query: str, limit: int = 50) -> List[Dict]:
        try:
            resp = self.session.get(f"{POLYMARKET_GAMMA_API}/markets", 
                params={"_q": query, "closed": False, "limit": limit})
            return resp.json() if resp.status_code == 200 else []
        except: return []
    
    def get_events(self, tag: str = "nfl", limit: int = 50) -> List[Dict]:
        try:
            resp = self.session.get(f"{POLYMARKET_GAMMA_API}/events",
                params={"tag": tag, "closed": False, "limit": limit})
            return resp.json() if resp.status_code == 200 else []
        except: return []
    
    def get_market_trades(self, market_id: str = None, limit: int = 500) -> List[Dict]:
        params = {"limit": limit}
        if market_id: params["market"] = market_id
        try:
            resp = self.session.get(f"{POLYMARKET_CLOB_API}/trades", params=params)
            return resp.json() if resp.status_code == 200 else []
        except: return []

class WhaleHunterV2:
    def __init__(self, etherscan_key: str = ETHERSCAN_API_KEY):
        self.polymarket = PolymarketClient()
        self.tracer = MultiChainTracer(etherscan_key)
        self.analyzer = PolymarketWhaleAnalyzer(etherscan_key)
        self.whale_wallets = set()
        self.large_trades = []
    
    def find_super_bowl_markets(self) -> List[Dict]:
        print("[*] Searching for Super Bowl markets...")
        markets = []
        for term in ["super bowl", "nfl champion", "afc champion", "nfc champion"]:
            markets.extend(self.polymarket.search_markets(term))
        events = self.polymarket.get_events("nfl")
        for event in events:
            if any(kw in event.get("title", "").lower() for kw in ["super", "champion"]):
                markets.extend(event.get("markets", []))
        seen = set()
        unique = [m for m in markets if (mid := m.get("id") or m.get("conditionId")) and mid not in seen and not seen.add(mid)]
        print(f"[+] Found {len(unique)} Super Bowl markets")
        return unique
    
    def find_whale_trades(self, min_value: float = 10000) -> List[Dict]:
        print(f"[*] Scanning for trades >= ${min_value:,.0f}...")
        for trade in self.polymarket.get_market_trades(limit=1000):
            try:
                value = float(trade.get("size", 0)) * float(trade.get("price", 0))
                if value >= min_value:
                    self.large_trades.append({"value_usd": value, "maker": trade.get("maker"),
                        "taker": trade.get("taker"), "side": trade.get("side")})
                    if trade.get("maker"): self.whale_wallets.add(trade["maker"])
                    if trade.get("taker"): self.whale_wallets.add(trade["taker"])
            except: continue
        self.large_trades.sort(key=lambda x: x["value_usd"], reverse=True)
        print(f"[+] Found {len(self.large_trades)} whale trades, {len(self.whale_wallets)} wallets")
        return self.large_trades
    
    def analyze_whale_wallets(self, max_wallets: int = 10, chains: List[str] = None) -> List[Dict]:
        chains = chains or ["polygon", "ethereum", "arbitrum"]
        print(f"[*] Analyzing top {max_wallets} wallets across {chains}...")
        analyses = []
        for i, wallet in enumerate(list(self.whale_wallets)[:max_wallets]):
            print(f"[{i+1}/{max_wallets}] {wallet[:20]}...")
            try:
                analyses.append(self.analyzer.analyze_polymarket_wallet(wallet))
                time.sleep(1)
            except Exception as e:
                print(f"  [!] Failed: {e}")
        return analyses

def main():
    parser = argparse.ArgumentParser(description="Polymarket Whale Hunter v2")
    parser.add_argument("--market", type=str, default="super-bowl")
    parser.add_argument("--min-position", type=int, default=10000)
    parser.add_argument("--max-wallets", type=int, default=10)
    parser.add_argument("--chains", type=str, default="polygon,ethereum,arbitrum")
    parser.add_argument("--whale-address", type=str)
    parser.add_argument("--output", type=str, default="whale_hunt_v2.json")
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("POLYMARKET WHALE HUNTER v2 - MULTI-CHAIN EDITION")
    print("="*70 + "\n")
    
    chains = [c.strip() for c in args.chains.split(",")]
    hunter = WhaleHunterV2()
    results = {"timestamp": datetime.now().isoformat()}
    
    if args.whale_address:
        results["analysis"] = hunter.analyzer.analyze_polymarket_wallet(args.whale_address)
    else:
        hunter.find_super_bowl_markets()
        hunter.find_whale_trades(args.min_position)
        if hunter.whale_wallets:
            results["analyses"] = hunter.analyze_whale_wallets(args.max_wallets, chains)
        results["trades"] = hunter.large_trades[:50]
        results["wallets"] = list(hunter.whale_wallets)[:100]
    
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[+] Saved to: {args.output}")

if __name__ == "__main__":
    main()
