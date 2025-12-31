#!/usr/bin/env python3
"""
NFL PROPS SCANNER - Full Market Coverage
=========================================
Scans all NFL prop markets across Polymarket, Kalshi, and sportsbooks.

PROPS COVERED:
- Super Bowl Winner
- Conference Champions (AFC/NFC)
- MVP Awards
- Player Props (Passing Yards, TDs, Rushing, Receiving)
- Game Props (Totals, Spreads, Moneylines)
- Season Props (Division Winners, Playoff Teams)
- Super Bowl Props (First TD, Halftime Score, etc.)
"""

import requests
import json
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

# Market Categories
PROP_CATEGORIES = {
    "championship": ["super bowl", "champion", "win super bowl"],
    "conference": ["afc champion", "nfc champion", "conference"],
    "mvp": ["mvp", "most valuable player", "offensive player", "defensive player"],
    "division": ["division winner", "afc east", "afc west", "afc north", "afc south",
                 "nfc east", "nfc west", "nfc north", "nfc south"],
    "player_passing": ["passing yards", "passing touchdowns", "completions", "interceptions"],
    "player_rushing": ["rushing yards", "rushing touchdowns", "carries"],
    "player_receiving": ["receiving yards", "receptions", "receiving touchdowns"],
    "game_props": ["total points", "spread", "moneyline", "over under"],
    "super_bowl_props": ["first touchdown", "halftime", "coin toss", "national anthem",
                        "gatorade color", "first score", "longest touchdown"]
}

# NFL Teams
NFL_TEAMS = {
    "AFC": {
        "East": ["Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets"],
        "North": ["Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers"],
        "South": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
        "West": ["Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers"]
    },
    "NFC": {
        "East": ["Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders"],
        "North": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
        "South": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
        "West": ["Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"]
    }
}


@dataclass
class PropMarket:
    """NFL Prop Market"""
    id: str
    platform: str
    category: str
    name: str
    outcomes: List[str]
    prices: Dict[str, float]
    volume: float
    liquidity: float
    expires_at: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)
    
    def best_value(self) -> Tuple[str, float]:
        """Find best value outcome"""
        if not self.prices:
            return ("", 0)
        best = min(self.prices.items(), key=lambda x: x[1])
        return best
    
    def implied_probability(self, outcome: str) -> float:
        return self.prices.get(outcome, 0)
    
    def american_odds(self, outcome: str) -> float:
        price = self.prices.get(outcome, 0.5)
        if price <= 0 or price >= 1:
            return 0
        if price >= 0.5:
            return -100 * price / (1 - price)
        return 100 * (1 - price) / price


# ============================================================================
# MARKET SCANNERS
# ============================================================================

class PolymarketPropsScanner:
    """Scan Polymarket for NFL props"""
    
    GAMMA_API = "https://gamma-api.polymarket.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.markets_cache = {}
        self.last_scan = None
    
    def scan_all_nfl_props(self) -> List[PropMarket]:
        """Scan all NFL prop markets"""
        markets = []
        
        # Search by category
        for category, keywords in PROP_CATEGORIES.items():
            for keyword in keywords:
                found = self._search_markets(keyword)
                for m in found:
                    prop = self._convert_to_prop(m, category)
                    if prop:
                        markets.append(prop)
        
        # Also search by team
        all_teams = []
        for conf in NFL_TEAMS.values():
            for div_teams in conf.values():
                all_teams.extend(div_teams)
        
        for team in all_teams[:10]:  # Limit to avoid rate limits
            found = self._search_markets(team)
            for m in found:
                prop = self._convert_to_prop(m, "team")
                if prop:
                    markets.append(prop)
            time.sleep(0.2)
        
        # Deduplicate
        seen = set()
        unique = []
        for m in markets:
            if m.id not in seen:
                seen.add(m.id)
                unique.append(m)
        
        self.last_scan = datetime.now()
        return unique
    
    def _search_markets(self, query: str) -> List[Dict]:
        try:
            resp = self.session.get(
                f"{self.GAMMA_API}/markets",
                params={"_q": query, "closed": False, "_limit": 50},
                timeout=15
            )
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
    
    def _convert_to_prop(self, market: Dict, category: str) -> Optional[PropMarket]:
        try:
            # Extract prices
            prices = {}
            outcomes = market.get("outcomes", [])
            outcome_prices = market.get("outcomePrices", [])
            
            for i, outcome in enumerate(outcomes):
                if i < len(outcome_prices):
                    prices[outcome] = float(outcome_prices[i])
            
            return PropMarket(
                id=market.get("id", ""),
                platform="polymarket",
                category=category,
                name=market.get("question", ""),
                outcomes=outcomes,
                prices=prices,
                volume=float(market.get("volume", 0)),
                liquidity=float(market.get("liquidity", 0)),
                metadata={
                    "slug": market.get("slug"),
                    "condition_id": market.get("conditionId"),
                    "end_date": market.get("endDate")
                }
            )
        except Exception as e:
            return None
    
    def get_super_bowl_markets(self) -> List[PropMarket]:
        """Get all Super Bowl related markets"""
        markets = []
        
        # Main Super Bowl winner
        sb_markets = self._search_markets("super bowl champion")
        sb_markets += self._search_markets("super bowl winner")
        sb_markets += self._search_markets("win super bowl")
        
        for m in sb_markets:
            prop = self._convert_to_prop(m, "championship")
            if prop:
                markets.append(prop)
        
        return markets
    
    def get_conference_markets(self) -> List[PropMarket]:
        """Get conference championship markets"""
        markets = []
        
        afc = self._search_markets("afc champion")
        nfc = self._search_markets("nfc champion")
        
        for m in afc + nfc:
            prop = self._convert_to_prop(m, "conference")
            if prop:
                markets.append(prop)
        
        return markets
    
    def get_mvp_markets(self) -> List[PropMarket]:
        """Get MVP and award markets"""
        markets = []
        
        mvp = self._search_markets("nfl mvp")
        mvp += self._search_markets("super bowl mvp")
        
        for m in mvp:
            prop = self._convert_to_prop(m, "mvp")
            if prop:
                markets.append(prop)
        
        return markets


class KalshiPropsScanner:
    """Scan Kalshi for NFL props"""
    
    BASE_URL = "https://trading-api.kalshi.com/trade-api/v2"
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.session = requests.Session()
    
    def scan_nfl_markets(self) -> List[PropMarket]:
        """Scan Kalshi NFL markets"""
        markets = []
        
        try:
            resp = self.session.get(
                f"{self.BASE_URL}/markets",
                params={"status": "open", "series_ticker": "NFL"},
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                for m in data.get("markets", []):
                    prop = self._convert_to_prop(m)
                    if prop:
                        markets.append(prop)
        except:
            pass
        
        return markets
    
    def _convert_to_prop(self, market: Dict) -> Optional[PropMarket]:
        try:
            # Determine category
            title = market.get("title", "").lower()
            category = "other"
            
            for cat, keywords in PROP_CATEGORIES.items():
                if any(kw in title for kw in keywords):
                    category = cat
                    break
            
            return PropMarket(
                id=market.get("ticker", ""),
                platform="kalshi",
                category=category,
                name=market.get("title", ""),
                outcomes=["Yes", "No"],
                prices={
                    "Yes": market.get("yes_ask", 50) / 100,
                    "No": market.get("no_ask", 50) / 100
                },
                volume=market.get("volume", 0),
                liquidity=market.get("open_interest", 0),
                expires_at=datetime.fromisoformat(market.get("expiration_time", "2025-12-31").replace("Z", "+00:00")),
                metadata={
                    "ticker": market.get("ticker"),
                    "status": market.get("status")
                }
            )
        except:
            return None


class SportsBookScanner:
    """Scan traditional sportsbooks for odds"""
    
    # Public odds endpoints (no API key needed)
    ESPN_API = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
    
    def __init__(self, odds_api_key: str = ""):
        self.odds_api_key = odds_api_key
        self.session = requests.Session()
    
    def get_game_odds(self) -> List[PropMarket]:
        """Get upcoming game odds"""
        markets = []
        
        # Get from ESPN (free)
        try:
            resp = self.session.get(
                f"{self.ESPN_API}/scoreboard",
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                
                for event in data.get("events", []):
                    competition = event.get("competitions", [{}])[0]
                    odds = competition.get("odds", [{}])[0] if competition.get("odds") else {}
                    
                    if odds:
                        # Home team
                        home = competition.get("competitors", [{}])[0]
                        away = competition.get("competitors", [{}])[1] if len(competition.get("competitors", [])) > 1 else {}
                        
                        home_name = home.get("team", {}).get("displayName", "Home")
                        away_name = away.get("team", {}).get("displayName", "Away")
                        
                        # Moneyline
                        home_ml = odds.get("homeTeamOdds", {}).get("moneyLine", 0)
                        away_ml = odds.get("awayTeamOdds", {}).get("moneyLine", 0)
                        
                        if home_ml and away_ml:
                            markets.append(PropMarket(
                                id=f"espn_{event.get('id')}_ml",
                                platform="espn",
                                category="game_props",
                                name=f"{away_name} @ {home_name} - Moneyline",
                                outcomes=[home_name, away_name],
                                prices={
                                    home_name: self._american_to_implied(home_ml),
                                    away_name: self._american_to_implied(away_ml)
                                },
                                volume=0,
                                liquidity=0,
                                expires_at=datetime.fromisoformat(event.get("date", "2025-12-31").replace("Z", "+00:00")),
                                metadata={"event_id": event.get("id")}
                            ))
                        
                        # Spread
                        spread = odds.get("spread", 0)
                        if spread:
                            markets.append(PropMarket(
                                id=f"espn_{event.get('id')}_spread",
                                platform="espn",
                                category="game_props",
                                name=f"{away_name} @ {home_name} - Spread ({spread})",
                                outcomes=[f"{home_name} {spread}", f"{away_name} {-spread}"],
                                prices={
                                    f"{home_name} {spread}": 0.5,
                                    f"{away_name} {-spread}": 0.5
                                },
                                volume=0,
                                liquidity=0,
                                metadata={"event_id": event.get("id"), "spread": spread}
                            ))
                        
                        # Total
                        total = odds.get("overUnder", 0)
                        if total:
                            markets.append(PropMarket(
                                id=f"espn_{event.get('id')}_total",
                                platform="espn",
                                category="game_props",
                                name=f"{away_name} @ {home_name} - Total ({total})",
                                outcomes=[f"Over {total}", f"Under {total}"],
                                prices={
                                    f"Over {total}": 0.5,
                                    f"Under {total}": 0.5
                                },
                                volume=0,
                                liquidity=0,
                                metadata={"event_id": event.get("id"), "total": total}
                            ))
                            
        except Exception as e:
            print(f"ESPN API error: {e}")
        
        return markets
    
    def get_futures_odds(self) -> List[PropMarket]:
        """Get futures odds (Super Bowl, Conference, etc.)"""
        markets = []
        
        # ESPN futures
        try:
            resp = self.session.get(
                f"{self.ESPN_API}/futures",
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                
                for future in data.get("futures", []):
                    name = future.get("name", "")
                    
                    outcomes = []
                    prices = {}
                    
                    for outcome in future.get("outcomes", []):
                        team = outcome.get("name", "")
                        odds = outcome.get("odds", 0)
                        
                        if team and odds:
                            outcomes.append(team)
                            prices[team] = self._american_to_implied(odds)
                    
                    if outcomes:
                        # Determine category
                        category = "championship"
                        if "afc" in name.lower():
                            category = "conference"
                        elif "nfc" in name.lower():
                            category = "conference"
                        elif "division" in name.lower():
                            category = "division"
                        elif "mvp" in name.lower():
                            category = "mvp"
                        
                        markets.append(PropMarket(
                            id=f"espn_futures_{future.get('id', '')}",
                            platform="espn_futures",
                            category=category,
                            name=name,
                            outcomes=outcomes,
                            prices=prices,
                            volume=0,
                            liquidity=0
                        ))
                        
        except Exception as e:
            print(f"ESPN Futures API error: {e}")
        
        return markets
    
    def _american_to_implied(self, odds: float) -> float:
        """Convert American odds to implied probability"""
        if odds == 0:
            return 0.5
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return abs(odds) / (abs(odds) + 100)


# ============================================================================
# UNIFIED PROPS AGGREGATOR
# ============================================================================

class NFLPropsAggregator:
    """Aggregates all NFL props across platforms"""
    
    def __init__(self):
        self.polymarket = PolymarketPropsScanner()
        self.kalshi = KalshiPropsScanner()
        self.sportsbooks = SportsBookScanner()
        
        self.all_markets: Dict[str, List[PropMarket]] = defaultdict(list)
        self.last_refresh = None
    
    def refresh_all(self) -> Dict[str, List[PropMarket]]:
        """Refresh all markets from all platforms"""
        print("[*] Refreshing NFL props from all platforms...")
        
        self.all_markets.clear()
        
        # Polymarket
        print("  [*] Scanning Polymarket...")
        poly_markets = self.polymarket.scan_all_nfl_props()
        for m in poly_markets:
            self.all_markets[m.category].append(m)
        print(f"      Found {len(poly_markets)} markets")
        
        # Kalshi
        print("  [*] Scanning Kalshi...")
        kalshi_markets = self.kalshi.scan_nfl_markets()
        for m in kalshi_markets:
            self.all_markets[m.category].append(m)
        print(f"      Found {len(kalshi_markets)} markets")
        
        # Sportsbooks
        print("  [*] Scanning Sportsbooks...")
        game_odds = self.sportsbooks.get_game_odds()
        futures_odds = self.sportsbooks.get_futures_odds()
        
        for m in game_odds + futures_odds:
            self.all_markets[m.category].append(m)
        print(f"      Found {len(game_odds) + len(futures_odds)} markets")
        
        self.last_refresh = datetime.now()
        
        total = sum(len(markets) for markets in self.all_markets.values())
        print(f"[+] Total: {total} NFL prop markets across {len(self.all_markets)} categories")
        
        return self.all_markets
    
    def get_by_category(self, category: str) -> List[PropMarket]:
        """Get markets by category"""
        return self.all_markets.get(category, [])
    
    def get_by_team(self, team: str) -> List[PropMarket]:
        """Get all markets involving a team"""
        team_lower = team.lower()
        results = []
        
        for markets in self.all_markets.values():
            for m in markets:
                if team_lower in m.name.lower():
                    results.append(m)
                for outcome in m.outcomes:
                    if team_lower in outcome.lower():
                        results.append(m)
                        break
        
        return results
    
    def find_arbitrage(self, min_spread: float = 2.0) -> List[Dict]:
        """Find arbitrage opportunities across platforms"""
        opportunities = []
        
        # Group markets by similar names
        market_groups = defaultdict(list)
        
        for markets in self.all_markets.values():
            for m in markets:
                # Normalize name for grouping
                normalized = m.name.lower()
                normalized = normalized.replace("super bowl", "sb")
                normalized = normalized.replace("championship", "champ")
                
                market_groups[normalized[:50]].append(m)
        
        # Check for arbitrage within groups
        for group_name, markets in market_groups.items():
            if len(markets) < 2:
                continue
            
            # Compare prices across platforms
            for i, m1 in enumerate(markets):
                for m2 in markets[i+1:]:
                    if m1.platform == m2.platform:
                        continue
                    
                    # Find common outcomes
                    common = set(m1.outcomes) & set(m2.outcomes)
                    
                    for outcome in common:
                        p1 = m1.prices.get(outcome, 0)
                        p2 = m2.prices.get(outcome, 0)
                        
                        if p1 > 0 and p2 > 0:
                            spread = abs(p1 - p2) * 100
                            
                            if spread >= min_spread:
                                opportunities.append({
                                    "market_name": group_name,
                                    "outcome": outcome,
                                    "platform_1": m1.platform,
                                    "price_1": p1,
                                    "platform_2": m2.platform,
                                    "price_2": p2,
                                    "spread_pct": spread,
                                    "buy_platform": m1.platform if p1 < p2 else m2.platform,
                                    "sell_platform": m2.platform if p1 < p2 else m1.platform
                                })
        
        return sorted(opportunities, key=lambda x: x["spread_pct"], reverse=True)
    
    def find_value_bets(self, threshold: float = 0.10) -> List[Dict]:
        """Find value bets where prediction markets diverge from sportsbooks"""
        value_bets = []
        
        # Compare Polymarket vs Sportsbooks
        poly_markets = [m for markets in self.all_markets.values() 
                       for m in markets if m.platform == "polymarket"]
        
        book_markets = [m for markets in self.all_markets.values()
                       for m in markets if m.platform in ["espn", "espn_futures"]]
        
        for poly in poly_markets:
            for book in book_markets:
                # Match by team name
                for outcome in poly.outcomes:
                    if outcome.lower() in book.name.lower():
                        poly_price = poly.prices.get(outcome, 0)
                        book_price = book.prices.get(outcome, 0)
                        
                        if poly_price > 0 and book_price > 0:
                            diff = book_price - poly_price
                            
                            if abs(diff) >= threshold:
                                value_bets.append({
                                    "team": outcome,
                                    "polymarket_price": poly_price,
                                    "sportsbook_price": book_price,
                                    "difference": diff,
                                    "recommendation": "BUY on Polymarket" if diff > 0 else "SELL on Polymarket",
                                    "polymarket_market": poly.name,
                                    "sportsbook_market": book.name
                                })
        
        return sorted(value_bets, key=lambda x: abs(x["difference"]), reverse=True)
    
    def get_summary(self) -> Dict:
        """Get summary of all markets"""
        summary = {
            "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
            "total_markets": sum(len(m) for m in self.all_markets.values()),
            "by_category": {cat: len(markets) for cat, markets in self.all_markets.items()},
            "by_platform": defaultdict(int)
        }
        
        for markets in self.all_markets.values():
            for m in markets:
                summary["by_platform"][m.platform] += 1
        
        return summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     NFL PROPS SCANNER - FULL MARKET COVERAGE                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    aggregator = NFLPropsAggregator()
    
    # Refresh all markets
    markets = aggregator.refresh_all()
    
    # Show summary
    print("\n" + "="*60)
    print("MARKET SUMMARY")
    print("="*60)
    summary = aggregator.get_summary()
    print(f"Total Markets: {summary['total_markets']}")
    print(f"\nBy Category:")
    for cat, count in sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    print(f"\nBy Platform:")
    for platform, count in sorted(summary['by_platform'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {platform}: {count}")
    
    # Show championship markets
    print("\n" + "="*60)
    print("SUPER BOWL MARKETS")
    print("="*60)
    sb_markets = aggregator.get_by_category("championship")
    for m in sb_markets[:10]:
        print(f"\n[{m.platform.upper()}] {m.name[:60]}")
        for outcome, price in sorted(m.prices.items(), key=lambda x: x[1])[:5]:
            odds = m.american_odds(outcome)
            print(f"  {outcome}: {price:.1%} ({odds:+.0f})")
    
    # Find arbitrage
    print("\n" + "="*60)
    print("ARBITRAGE OPPORTUNITIES")
    print("="*60)
    arbs = aggregator.find_arbitrage(min_spread=2.0)
    if arbs:
        for arb in arbs[:10]:
            print(f"\n{arb['market_name'][:40]}...")
            print(f"  Outcome: {arb['outcome']}")
            print(f"  {arb['platform_1']}: {arb['price_1']:.1%}")
            print(f"  {arb['platform_2']}: {arb['price_2']:.1%}")
            print(f"  Spread: {arb['spread_pct']:.2f}%")
            print(f"  Action: BUY on {arb['buy_platform']}, SELL on {arb['sell_platform']}")
    else:
        print("  No arbitrage opportunities found")
    
    # Find value bets
    print("\n" + "="*60)
    print("VALUE BETS (Polymarket vs Sportsbooks)")
    print("="*60)
    value_bets = aggregator.find_value_bets(threshold=0.05)
    if value_bets:
        for vb in value_bets[:10]:
            print(f"\n{vb['team']}")
            print(f"  Polymarket: {vb['polymarket_price']:.1%}")
            print(f"  Sportsbook: {vb['sportsbook_price']:.1%}")
            print(f"  Difference: {vb['difference']:+.1%}")
            print(f"  Recommendation: {vb['recommendation']}")
    else:
        print("  No significant value bets found")
    
    # Save data
    output = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "arbitrage": arbs,
        "value_bets": value_bets,
        "markets": {cat: [m.__dict__ for m in markets] 
                   for cat, markets in aggregator.all_markets.items()}
    }
    
    with open("nfl_props_data.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n[+] Data saved to nfl_props_data.json")


if __name__ == "__main__":
    main()
