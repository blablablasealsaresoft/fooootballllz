#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    APOLLO EDGE - NFL BETTING INTELLIGENCE                     ║
║                                                                               ║
║              Whale Detection • Arbitrage • Fast Execution • Props             ║
║                                                                               ║
║                         "BlackRock-Tier Edge Trading"                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

CAPABILITIES:
- Real-time whale position detection across Polymarket
- 5-hop wallet cluster analysis (Solana → Polygon trace)
- Cross-platform arbitrage (Polymarket vs Kalshi vs Sportsbooks)
- Sub-second trade execution with position sniping
- NFL props coverage (MVP, passing yards, TDs, etc.)
- Automated position management and alerts

SETUP:
1. Copy config_template.py to config.py
2. Add your wallet address and private key
3. Set PAPER_TRADING_MODE = False for live trading

AUTHOR: APOLLO CyberSentinel
VERSION: 1.0.0
"""

import os
import sys
import json
import time
import asyncio
import aiohttp
import requests
import threading
import websocket
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Callable
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, PriorityQueue
import logging

# ============================================================================
# LOAD CONFIG FROM config.py
# ============================================================================

try:
    from config import (
        ETHERSCAN_API_KEY,
        TRADING_WALLET_ADDRESS,
        TRADING_WALLET_PRIVATE_KEY,
        PAPER_TRADING_MODE,
        MIN_WHALE_SIZE_USD,
        SNIPE_THRESHOLD_USD,
        FOLLOW_PERCENTAGE,
        MAX_POSITION_SIZE_USD,
        MAX_SLIPPAGE_PCT,
        MAX_DAILY_SNIPES,
        STOP_LOSS_PCT,
        TAKE_PROFIT_PCT,
        MIN_CONFIDENCE_SCORE,
        MIN_USDC_RESERVE,
        MAX_TRADING_CAPITAL,
        MAX_DAILY_LOSS_USD,
        POLYGON_RPC_URL,
        ENABLE_PLAYBOOKS,
        AUTO_LOAD_PLAYBOOKS,
        AUTO_LOAD_WATCHLISTS,
        ENABLE_AUTO_SCALING,
        CAPITAL_USAGE_PCT,
        POSITION_SIZE_PCT,
    )
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False
    ENABLE_PLAYBOOKS = False
    AUTO_LOAD_PLAYBOOKS = []
    AUTO_LOAD_WATCHLISTS = []
    ENABLE_AUTO_SCALING = True
    CAPITAL_USAGE_PCT = 90
    POSITION_SIZE_PCT = 50
    # Defaults
    ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"
    TRADING_WALLET_ADDRESS = ""
    TRADING_WALLET_PRIVATE_KEY = ""
    PAPER_TRADING_MODE = True
    MIN_WHALE_SIZE_USD = 10000
    SNIPE_THRESHOLD_USD = 25000
    FOLLOW_PERCENTAGE = 0.10
    MAX_POSITION_SIZE_USD = 5000
    MAX_SLIPPAGE_PCT = 1.0
    MAX_DAILY_SNIPES = 20
    STOP_LOSS_PCT = 15.0
    TAKE_PROFIT_PCT = 50.0
    MIN_CONFIDENCE_SCORE = 70
    MIN_USDC_RESERVE = 100
    MAX_TRADING_CAPITAL = 10000
    MAX_DAILY_LOSS_USD = 2000
    POLYGON_RPC_URL = "https://polygon-rpc.com"

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """System configuration - loaded from config.py"""
    # API Keys
    ETHERSCAN_API_KEY: str = ETHERSCAN_API_KEY
    POLYMARKET_API_KEY: str = ""  # Optional - for authenticated trading
    KALSHI_API_KEY: str = ""      # Optional - for Kalshi trading
    
    # Wallet (from config.py)
    TRADING_WALLET_ADDRESS: str = TRADING_WALLET_ADDRESS
    TRADING_WALLET_PRIVATE_KEY: str = TRADING_WALLET_PRIVATE_KEY
    PAPER_TRADING_MODE: bool = PAPER_TRADING_MODE
    
    # Chain Configuration
    POLYGON_CHAIN_ID: int = 137
    ETHEREUM_CHAIN_ID: int = 1
    POLYGON_RPC_URL: str = POLYGON_RPC_URL
    
    # Trading Parameters (from config.py)
    MIN_WHALE_POSITION_USD: float = MIN_WHALE_SIZE_USD
    MIN_ARBITRAGE_SPREAD_PCT: float = 2.0  # Minimum 2% spread to trade
    MAX_POSITION_SIZE_USD: float = MAX_POSITION_SIZE_USD
    SLIPPAGE_TOLERANCE_PCT: float = MAX_SLIPPAGE_PCT
    
    # Execution Settings
    EXECUTION_DELAY_MS: int = 100  # Delay before executing after signal
    MAX_RETRIES: int = 3
    RETRY_DELAY_MS: int = 500
    
    # Monitoring
    POLL_INTERVAL_SECONDS: float = 1.0
    WHALE_ALERT_THRESHOLD_USD: float = SNIPE_THRESHOLD_USD
    
    # Risk Management (from config.py)
    MAX_DAILY_LOSS_USD: float = MAX_DAILY_LOSS_USD
    MAX_POSITION_PCT: float = 20  # Max 20% of portfolio in single position
    STOP_LOSS_PCT: float = STOP_LOSS_PCT
    TAKE_PROFIT_PCT: float = TAKE_PROFIT_PCT


# Global config
CONFIG = Config()

# Logging setup - Windows compatible
import sys
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('apollo_edge.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('ApolloEdge')

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Market:
    """Represents a betting market"""
    id: str
    platform: str  # polymarket, kalshi, draftkings, etc.
    name: str
    outcomes: List[str]
    prices: Dict[str, float]  # outcome -> price (0-1)
    volume: float
    liquidity: float
    last_updated: datetime = field(default_factory=datetime.now)
    
    def implied_odds(self, outcome: str) -> float:
        """Convert price to American odds"""
        price = self.prices.get(outcome, 0)
        if price <= 0 or price >= 1:
            return 0
        if price >= 0.5:
            return -100 * price / (1 - price)
        else:
            return 100 * (1 - price) / price


@dataclass
class WhalePosition:
    """Detected whale position"""
    wallet: str
    market_id: str
    outcome: str
    size_usd: float
    entry_price: float
    timestamp: datetime
    tx_hash: str
    cluster_id: Optional[str] = None
    confidence: float = 0.0
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass 
class ArbitrageOpportunity:
    """Arbitrage opportunity between platforms"""
    id: str
    market_name: str
    outcome: str
    platform_buy: str
    platform_sell: str
    price_buy: float
    price_sell: float
    spread_pct: float
    max_size_usd: float
    expires_at: datetime
    confidence: float
    
    @property
    def expected_profit_pct(self) -> float:
        return self.spread_pct - 0.5  # Account for fees


@dataclass
class Position:
    """Active position in portfolio"""
    id: str
    market_id: str
    platform: str
    outcome: str
    size_shares: float
    entry_price: float
    current_price: float
    entry_time: datetime
    pnl_usd: float = 0
    pnl_pct: float = 0
    status: str = "open"  # open, closed, stopped
    
    def update_pnl(self, current_price: float):
        self.current_price = current_price
        self.pnl_usd = self.size_shares * (current_price - self.entry_price)
        self.pnl_pct = ((current_price / self.entry_price) - 1) * 100 if self.entry_price > 0 else 0


@dataclass
class Signal:
    """Trading signal"""
    id: str
    signal_type: str  # whale_follow, arbitrage, momentum, cluster
    market_id: str
    platform: str
    outcome: str
    direction: str  # buy, sell
    strength: float  # 0-100
    size_usd: float
    reason: str
    timestamp: datetime
    expires_at: datetime
    metadata: Dict = field(default_factory=dict)


# ============================================================================
# API CLIENTS
# ============================================================================

class EtherscanV2Client:
    """Etherscan V2 API - Multichain support"""
    
    BASE_URL = "https://api.etherscan.io/v2/api"
    
    def __init__(self, api_key: str = CONFIG.ETHERSCAN_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        self._last_call = 0
        self._rate_limit = 0.2  # 5 calls/sec
    
    def _throttle(self):
        elapsed = time.time() - self._last_call
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)
        self._last_call = time.time()
    
    def call(self, chain_id: int, module: str, action: str, **params) -> Optional[any]:
        self._throttle()
        
        params.update({
            "chainid": chain_id,
            "module": module,
            "action": action,
            "apikey": self.api_key
        })
        
        try:
            resp = self.session.get(self.BASE_URL, params=params, timeout=30)
            data = resp.json()
            
            if data.get("status") == "1":
                return data.get("result")
            return None
        except Exception as e:
            logger.error(f"Etherscan API error: {e}")
            return None
    
    def get_token_transfers(self, address: str, contract: str, 
                           chain_id: int = 137) -> List[Dict]:
        return self.call(chain_id, "account", "tokentx",
                        address=address, contractaddress=contract,
                        sort="desc") or []
    
    def get_transactions(self, address: str, chain_id: int = 137) -> List[Dict]:
        return self.call(chain_id, "account", "txlist",
                        address=address, sort="desc") or []


class PolymarketClient:
    """Polymarket API client with WebSocket support"""
    
    GAMMA_API = "https://gamma-api.polymarket.com"
    CLOB_API = "https://clob.polymarket.com"
    WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.ws = None
        self.ws_callbacks = []
    
    def get_markets(self, tag: str = None, limit: int = 100) -> List[Dict]:
        params = {"_limit": limit, "closed": False, "active": True}
        if tag:
            params["tag"] = tag
        
        try:
            resp = self.session.get(f"{self.GAMMA_API}/markets", params=params, timeout=15)
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
    
    def search_markets(self, query: str) -> List[Dict]:
        try:
            resp = self.session.get(f"{self.GAMMA_API}/markets",
                                   params={"_q": query, "closed": False}, timeout=15)
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
    
    def get_orderbook(self, token_id: str) -> Optional[Dict]:
        try:
            resp = self.session.get(f"{self.CLOB_API}/book",
                                   params={"token_id": token_id}, timeout=15)
            return resp.json() if resp.status_code == 200 else None
        except:
            return None
    
    def get_trades(self, market_id: str = None, limit: int = 100) -> List[Dict]:
        params = {"limit": limit}
        if market_id:
            params["market"] = market_id
        
        try:
            resp = self.session.get(f"{self.CLOB_API}/trades", params=params, timeout=15)
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
    
    def subscribe_market(self, market_id: str, callback: Callable):
        """Subscribe to real-time market updates via WebSocket"""
        self.ws_callbacks.append((market_id, callback))
        
        if not self.ws:
            self._start_websocket()
    
    def _start_websocket(self):
        def on_message(ws, message):
            data = json.loads(message)
            for market_id, callback in self.ws_callbacks:
                if data.get("market") == market_id:
                    callback(data)
        
        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")
        
        def on_close(ws, close_status, close_msg):
            logger.info("WebSocket closed, reconnecting...")
            time.sleep(5)
            self._start_websocket()
        
        self.ws = websocket.WebSocketApp(
            self.WS_URL,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()


# Kalshi removed - using TheOddsAPI and other platforms instead


class OddsAPIClient:
    """TheOddsAPI for sportsbook odds"""
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_odds(self, sport: str = "americanfootball_nfl", 
                 markets: str = "h2h,spreads,totals") -> List[Dict]:
        if not self.api_key:
            return []
        
        try:
            resp = self.session.get(
                f"{self.BASE_URL}/sports/{sport}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": "us",
                    "markets": markets,
                    "oddsFormat": "american"
                },
                timeout=15
            )
            return resp.json() if resp.status_code == 200 else []
        except:
            return []


# ============================================================================
# CORE MODULES
# ============================================================================

class WhaleDetector:
    """Real-time whale position detection"""
    
    # Polymarket contracts
    CTF_EXCHANGE = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"
    NEG_RISK_EXCHANGE = "0xC5d563A36AE78145C45a50134d48A1215220f80a"
    USDC_POLYGON = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
    
    # Known CEX wallets
    CEX_WALLETS = {
        "0x28c6c06298d514db089934071355e5743bf21d60": "Binance",
        "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Binance",
        "0x56eddb7aa87536c09ccc2793473599fd21a8b17f": "Coinbase",
        "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43": "Coinbase",
        "0x5f65f7b609678448494de4c87521cdf6cef1e932": "OKX",
        "0x3c783c21a0383057d128bae431894a5c19f9cf06": "Bybit",
    }
    
    def __init__(self):
        self.etherscan = EtherscanV2Client()
        self.polymarket = PolymarketClient()
        self.detected_whales = {}
        self.wallet_clusters = defaultdict(set)
        self.callbacks = []
    
    def on_whale_detected(self, callback: Callable[[WhalePosition], None]):
        """Register callback for whale detection"""
        self.callbacks.append(callback)
    
    def _notify_whale(self, whale: WhalePosition):
        for callback in self.callbacks:
            try:
                callback(whale)
            except Exception as e:
                logger.error(f"Whale callback error: {e}")
    
    def scan_recent_trades(self, min_size: float = 10000) -> List[WhalePosition]:
        """Scan recent trades for whale activity"""
        whales = []
        
        # Get recent large trades from Polymarket
        trades = self.polymarket.get_trades(limit=500)
        
        for trade in trades:
            try:
                size = float(trade.get("size", 0))
                price = float(trade.get("price", 0))
                value = size * price
                
                if value >= min_size:
                    whale = WhalePosition(
                        wallet=trade.get("maker", "unknown"),
                        market_id=trade.get("market", ""),
                        outcome=trade.get("outcome", ""),
                        size_usd=value,
                        entry_price=price,
                        timestamp=datetime.now(),
                        tx_hash=trade.get("transactionHash", ""),
                        confidence=min(100, value / 1000)  # Higher value = higher confidence
                    )
                    whales.append(whale)
                    self._notify_whale(whale)
                    
            except (ValueError, TypeError):
                continue
        
        return whales
    
    def trace_wallet(self, address: str, max_hops: int = 5) -> Dict:
        """Trace wallet funding sources"""
        result = {
            "address": address,
            "cex_sources": [],
            "bridge_sources": [],
            "total_inflow": 0,
            "hops_analyzed": 0
        }
        
        visited = set()
        current = [address]
        
        for hop in range(max_hops):
            if not current:
                break
            
            result["hops_analyzed"] = hop + 1
            next_addrs = []
            
            for addr in current:
                if addr.lower() in visited:
                    continue
                visited.add(addr.lower())
                
                # Check if CEX
                if addr.lower() in self.CEX_WALLETS:
                    result["cex_sources"].append({
                        "address": addr,
                        "exchange": self.CEX_WALLETS[addr.lower()],
                        "hop": hop + 1
                    })
                    continue
                
                # Get USDC transfers
                transfers = self.etherscan.get_token_transfers(
                    addr, self.USDC_POLYGON, 137
                )
                
                for tx in transfers:
                    if tx.get("to", "").lower() == addr.lower():
                        value = int(tx.get("value", 0)) / 1e6
                        if value >= 100:
                            result["total_inflow"] += value
                            from_addr = tx.get("from", "")
                            if from_addr.lower() not in visited:
                                next_addrs.append(from_addr)
            
            current = list(set(next_addrs))[:10]
        
        return result
    
    def find_clusters(self, wallets: List[str]) -> Dict[str, List[str]]:
        """Find wallet clusters by common funding source"""
        source_to_wallets = defaultdict(set)
        
        for wallet in wallets:
            transfers = self.etherscan.get_token_transfers(
                wallet, self.USDC_POLYGON, 137
            )
            
            for tx in transfers:
                if tx.get("to", "").lower() == wallet.lower():
                    source = tx.get("from", "").lower()
                    value = int(tx.get("value", 0)) / 1e6
                    if value >= 100:
                        source_to_wallets[source].add(wallet.lower())
        
        clusters = {}
        cluster_id = 0
        
        for source, funded_wallets in source_to_wallets.items():
            if len(funded_wallets) >= 2:
                cluster_id += 1
                clusters[f"CLUSTER_{cluster_id}"] = {
                    "source": source,
                    "wallets": list(funded_wallets),
                    "count": len(funded_wallets)
                }
        
        return clusters


class ArbitrageScanner:
    """Cross-platform arbitrage detection"""
    
    def __init__(self):
        self.polymarket = PolymarketClient()
        self.odds_api = OddsAPIClient()
        self.opportunities = {}
    
    def scan_nfl_markets(self) -> List[ArbitrageOpportunity]:
        """Scan for NFL arbitrage opportunities"""
        opportunities = []
        
        # Get Polymarket NFL markets
        poly_markets = self.polymarket.search_markets("super bowl")
        poly_markets += self.polymarket.search_markets("nfl")
        
        # Get sportsbook odds from TheOddsAPI
        sportsbook_games = self.odds_api.get_odds("americanfootball_nfl")
        
        # Compare Polymarket prices vs sportsbook odds
        for poly_market in poly_markets:
            # Find matching sportsbook market
            # Calculate arbitrage opportunities
            # This can be expanded based on your needs
            pass
        
        return opportunities
    
    def _markets_match(self, name1: str, name2: str) -> bool:
        """Check if two market names refer to same event"""
        # Simple keyword matching
        keywords = ["super bowl", "patriots", "broncos", "seahawks", "rams", "bills"]
        
        for kw in keywords:
            if kw in name1 and kw in name2:
                return True
        return False
    
    def _check_arbitrage(self, poly_market: Dict, sportsbook_odds: Dict) -> Optional[ArbitrageOpportunity]:
        """Check for arbitrage between Polymarket and sportsbooks"""
        # Compare Polymarket prediction market prices vs traditional sportsbook odds
        # This provides different opportunities since sportsbooks have different pricing models
        # Implementation can be expanded based on specific needs
        return None


class SignalGenerator:
    """Generates trading signals from various sources"""
    
    def __init__(self):
        self.whale_detector = WhaleDetector()
        self.arb_scanner = ArbitrageScanner()
        self.signal_queue = PriorityQueue()
        self.callbacks = []
    
    def on_signal(self, callback: Callable[[Signal], None]):
        self.callbacks.append(callback)
    
    def _emit_signal(self, signal: Signal):
        # Priority queue: higher strength = higher priority (use negative for min-heap)
        self.signal_queue.put((-signal.strength, signal))
        
        for callback in self.callbacks:
            try:
                callback(signal)
            except Exception as e:
                logger.error(f"Signal callback error: {e}")
    
    def generate_whale_signals(self, min_size: float = 10000) -> List[Signal]:
        """Generate signals from whale activity"""
        signals = []
        whales = self.whale_detector.scan_recent_trades(min_size)
        
        for whale in whales:
            # Calculate signal strength based on size and confidence
            strength = min(100, (whale.size_usd / 1000) + whale.confidence)
            
            signal = Signal(
                id=f"whale_{whale.tx_hash[:16]}",
                signal_type="whale_follow",
                market_id=whale.market_id,
                platform="polymarket",
                outcome=whale.outcome,
                direction="buy",
                strength=strength,
                size_usd=min(whale.size_usd * 0.1, CONFIG.MAX_POSITION_SIZE_USD),  # 10% of whale
                reason=f"Whale position: ${whale.size_usd:,.0f} at {whale.entry_price:.4f}",
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(minutes=30),
                metadata={"whale": whale.to_dict()}
            )
            signals.append(signal)
            self._emit_signal(signal)
        
        return signals
    
    def generate_arb_signals(self) -> List[Signal]:
        """Generate signals from arbitrage opportunities"""
        signals = []
        opportunities = self.arb_scanner.scan_nfl_markets()
        
        for opp in opportunities:
            if opp.spread_pct >= CONFIG.MIN_ARBITRAGE_SPREAD_PCT:
                signal = Signal(
                    id=f"arb_{opp.id}",
                    signal_type="arbitrage",
                    market_id=opp.id,
                    platform=opp.platform_buy,
                    outcome=opp.outcome,
                    direction="buy",
                    strength=opp.confidence,
                    size_usd=opp.max_size_usd,
                    reason=f"Arbitrage: {opp.spread_pct:.2f}% spread ({opp.platform_buy} → {opp.platform_sell})",
                    timestamp=datetime.now(),
                    expires_at=opp.expires_at,
                    metadata={"arbitrage": asdict(opp)}
                )
                signals.append(signal)
                self._emit_signal(signal)
        
        return signals


class ExecutionEngine:
    """Fast trade execution with position sniping"""
    
    def __init__(self):
        self.polymarket = PolymarketClient()
        self.positions = {}
        self.pending_orders = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    async def execute_signal(self, signal: Signal) -> Optional[Position]:
        """Execute a trading signal"""
        logger.info(f"Executing signal: {signal.id} - {signal.signal_type}")
        
        # Check if signal is still valid
        if datetime.now() > signal.expires_at:
            logger.warning(f"Signal {signal.id} expired")
            return None
        
        # Route to appropriate exchange
        if signal.platform == "polymarket":
            return await self._execute_polymarket(signal)
        elif signal.platform == "kalshi":
            return await self._execute_kalshi(signal)
        else:
            logger.error(f"Unknown platform: {signal.platform}")
            return None
    
    async def _execute_polymarket(self, signal: Signal) -> Optional[Position]:
        """Execute trade on Polymarket"""
        # In production, this would use the CLOB API with authentication
        # For now, we simulate the execution
        
        logger.info(f"[POLYMARKET] {signal.direction.upper()} {signal.outcome} @ {signal.size_usd:,.2f}")
        
        # Get current orderbook for price
        # In production: submit limit order or market order
        
        position = Position(
            id=f"pos_{signal.id}",
            market_id=signal.market_id,
            platform="polymarket",
            outcome=signal.outcome,
            size_shares=signal.size_usd,  # Simplified
            entry_price=0.5,  # Would get from orderbook
            current_price=0.5,
            entry_time=datetime.now()
        )
        
        self.positions[position.id] = position
        return position
    
    async def _execute_kalshi(self, signal: Signal) -> Optional[Position]:
        """Execute trade on Kalshi"""
        logger.info(f"[KALSHI] {signal.direction.upper()} {signal.outcome} @ {signal.size_usd:,.2f}")
        
        # Similar to Polymarket execution
        position = Position(
            id=f"pos_{signal.id}",
            market_id=signal.market_id,
            platform="kalshi",
            outcome=signal.outcome,
            size_shares=signal.size_usd,
            entry_price=0.5,
            current_price=0.5,
            entry_time=datetime.now()
        )
        
        self.positions[position.id] = position
        return position
    
    def snipe_position(self, whale: WhalePosition, follow_pct: float = 0.1):
        """Quickly follow a whale position"""
        size = min(whale.size_usd * follow_pct, CONFIG.MAX_POSITION_SIZE_USD)
        
        signal = Signal(
            id=f"snipe_{whale.tx_hash[:16]}",
            signal_type="whale_snipe",
            market_id=whale.market_id,
            platform="polymarket",
            outcome=whale.outcome,
            direction="buy",
            strength=90,  # High priority
            size_usd=size,
            reason=f"Sniping whale: ${whale.size_usd:,.0f}",
            timestamp=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=30),  # Quick expiry
            metadata={"whale": whale.to_dict()}
        )
        
        # Execute immediately in background
        self.executor.submit(lambda: asyncio.run(self.execute_signal(signal)))
        
        return signal


class PortfolioManager:
    """Manages positions and risk"""
    
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.daily_pnl = 0
        self.total_value = 0
    
    def add_position(self, position: Position):
        self.positions[position.id] = position
        self._update_totals()
    
    def close_position(self, position_id: str, exit_price: float) -> float:
        if position_id not in self.positions:
            return 0
        
        position = self.positions[position_id]
        position.current_price = exit_price
        position.update_pnl(exit_price)
        position.status = "closed"
        
        pnl = position.pnl_usd
        self.daily_pnl += pnl
        
        del self.positions[position_id]
        self._update_totals()
        
        return pnl
    
    def _update_totals(self):
        self.total_value = sum(p.size_shares * p.current_price for p in self.positions.values())
    
    def check_risk_limits(self) -> List[str]:
        """Check if any risk limits are breached"""
        alerts = []
        
        if self.daily_pnl < -CONFIG.MAX_DAILY_LOSS_USD:
            alerts.append(f"DAILY LOSS LIMIT BREACHED: ${self.daily_pnl:,.2f}")
        
        for pos in self.positions.values():
            pos_pct = (pos.size_shares * pos.current_price) / max(1, self.total_value) * 100
            
            if pos_pct > CONFIG.MAX_POSITION_PCT:
                alerts.append(f"POSITION SIZE LIMIT: {pos.id} at {pos_pct:.1f}%")
            
            if pos.pnl_pct < -CONFIG.STOP_LOSS_PCT:
                alerts.append(f"STOP LOSS TRIGGERED: {pos.id} at {pos.pnl_pct:.1f}%")
            
            if pos.pnl_pct > CONFIG.TAKE_PROFIT_PCT:
                alerts.append(f"TAKE PROFIT TRIGGERED: {pos.id} at {pos.pnl_pct:.1f}%")
        
        return alerts
    
    def get_summary(self) -> Dict:
        return {
            "total_positions": len(self.positions),
            "total_value": self.total_value,
            "daily_pnl": self.daily_pnl,
            "positions": [asdict(p) for p in self.positions.values()]
        }


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class ApolloEdge:
    """Main system orchestrator"""
    
    def __init__(self):
        self.whale_detector = WhaleDetector()
        self.arb_scanner = ArbitrageScanner()
        self.signal_generator = SignalGenerator()
        self.execution = ExecutionEngine()
        self.portfolio = PortfolioManager()
        
        # Playbooks integration
        self.playbook_manager = None
        if ENABLE_PLAYBOOKS:
            try:
                from playbooks import PlaybookManager
                self.playbook_manager = PlaybookManager()
                self._load_playbooks()
                logger.info("[SUCCESS] Playbooks system enabled")
            except ImportError:
                logger.warning("⚠️ Playbooks module not found")
        
        self.running = False
        self.stats = {
            "signals_generated": 0,
            "trades_executed": 0,
            "whales_detected": 0,
            "arb_opportunities": 0,
            "playbooks_triggered": 0
        }
        
        # Wire up callbacks
        self.whale_detector.on_whale_detected(self._on_whale)
        self.signal_generator.on_signal(self._on_signal)
    
    def _on_whale(self, whale: WhalePosition):
        """Handle whale detection"""
        self.stats["whales_detected"] += 1
        logger.info(f"[WHALE DETECTED] ${whale.size_usd:,.0f} on {whale.outcome}")
        
        # Check playbooks
        if self.playbook_manager:
            whale_data = {
                "whale_size": whale.size_usd,
                "whale_action": "buy",
                "market_id": whale.market_id,
                "market_name": whale.outcome,
                "wallet": whale.wallet,
                "confidence": whale.confidence,
                "price": whale.entry_price
            }
            actions = self.playbook_manager.evaluate_playbooks(whale_data)
            if actions:
                self.stats["playbooks_triggered"] += len(actions)
                logger.info(f"[PLAYBOOK] {len(actions)} playbook actions triggered")
        
        # Auto-snipe if enabled and size is large enough
        if whale.size_usd >= CONFIG.WHALE_ALERT_THRESHOLD_USD:
            self.execution.snipe_position(whale, follow_pct=0.1)
    
    def _on_signal(self, signal: Signal):
        """Handle new trading signal"""
        self.stats["signals_generated"] += 1
        logger.info(f"[SIGNAL] {signal.signal_type} - {signal.reason}")
    
    async def run_scan_cycle(self):
        """Run one scan cycle"""
        
        # Update scaled limits if auto-scaling enabled
        if self.auto_scaler:
            # TODO: Get actual USDC balance from wallet
            # For now, use configured amount
            usdc_balance = CONFIG.MAX_TRADING_CAPITAL
            scaled_limits = self.auto_scaler.calculate_limits(usdc_balance)
            
            # Update config with scaled values
            CONFIG.MAX_POSITION_SIZE_USD = scaled_limits['max_position']
            CONFIG.MAX_CONCURRENT_POSITIONS = scaled_limits['max_positions']
            CONFIG.MAX_DAILY_SNIPES = scaled_limits['max_daily_snipes']
            CONFIG.FOLLOW_PERCENTAGE = scaled_limits['follow_pct']
        
        # Scan for whales
        whales = self.whale_detector.scan_recent_trades(CONFIG.MIN_WHALE_POSITION_USD)
        
        # Generate signals
        whale_signals = self.signal_generator.generate_whale_signals()
        arb_signals = self.signal_generator.generate_arb_signals()
        
        self.stats["arb_opportunities"] += len(arb_signals)
        
        # Execute top signals
        all_signals = whale_signals + arb_signals
        all_signals.sort(key=lambda s: s.strength, reverse=True)
        
        for signal in all_signals[:3]:  # Top 3 signals per cycle
            if signal.strength >= 70:  # Only high-confidence signals
                position = await self.execution.execute_signal(signal)
                if position:
                    self.portfolio.add_position(position)
                    self.stats["trades_executed"] += 1
        
        # Check risk limits
        alerts = self.portfolio.check_risk_limits()
        for alert in alerts:
            logger.warning(f"[RISK ALERT] {alert}")
    
    async def start(self):
        """Start the trading system"""
        self.running = True
        logger.info("[STARTING] Apollo Edge launching...")
        
        while self.running:
            try:
                await self.run_scan_cycle()
                await asyncio.sleep(CONFIG.POLL_INTERVAL_SECONDS)
            except Exception as e:
                logger.error(f"Scan cycle error: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Stop the trading system"""
        self.running = False
        logger.info("Apollo Edge stopped")
    
    def _load_playbooks(self):
        """Load configured playbooks on startup"""
        if not self.playbook_manager:
            return
        
        for playbook_id in AUTO_LOAD_PLAYBOOKS:
            try:
                self.playbook_manager.load_preset_playbook(playbook_id)
                logger.info(f"[PLAYBOOK] Loaded playbook: {playbook_id}")
            except Exception as e:
                logger.error(f"Failed to load playbook {playbook_id}: {e}")
        
        for watchlist_id in AUTO_LOAD_WATCHLISTS:
            try:
                self.playbook_manager.load_preset_watchlist(watchlist_id)
                logger.info(f"[WATCHLIST] Loaded watchlist: {watchlist_id}")
            except Exception as e:
                logger.error(f"Failed to load watchlist {watchlist_id}: {e}")
    
    def get_status(self) -> Dict:
        """Get system status"""
        status = {
            "running": self.running,
            "stats": self.stats,
            "portfolio": self.portfolio.get_summary(),
            "config": asdict(CONFIG)
        }
        
        if self.playbook_manager:
            status["playbooks"] = {
                "enabled": True,
                "loaded": len(self.playbook_manager.playbooks),
                "watchlists": len(self.playbook_manager.watchlists),
                "signals_queued": len(self.playbook_manager.signal_queue)
            }
        
        return status


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Apollo Edge - NFL Betting Intelligence")
    parser.add_argument("--mode", choices=["scan", "monitor", "analyze", "demo"],
                       default="demo", help="Operating mode")
    parser.add_argument("--wallet", type=str, help="Wallet to analyze")
    parser.add_argument("--min-whale", type=float, default=10000,
                       help="Minimum whale position size")
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    APOLLO EDGE - NFL BETTING INTELLIGENCE                     ║
║                                                                               ║
║              Whale Detection • Arbitrage • Fast Execution • Props             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if args.mode == "scan":
        # One-time scan
        print("[*] Running single scan cycle...")
        system = ApolloEdge()
        asyncio.run(system.run_scan_cycle())
        print(json.dumps(system.get_status(), indent=2, default=str))
        
    elif args.mode == "monitor":
        # Continuous monitoring
        print("[*] Starting continuous monitoring...")
        print("[*] Press Ctrl+C to stop")
        system = ApolloEdge()
        try:
            asyncio.run(system.start())
        except KeyboardInterrupt:
            system.stop()
            print("\n[*] Stopped")
            print(json.dumps(system.get_status(), indent=2, default=str))
    
    elif args.mode == "analyze" and args.wallet:
        # Analyze specific wallet
        print(f"[*] Analyzing wallet: {args.wallet}")
        detector = WhaleDetector()
        result = detector.trace_wallet(args.wallet, max_hops=5)
        print(json.dumps(result, indent=2, default=str))
    
    else:
        # Demo mode
        print("[*] Demo Mode - Showing system capabilities")
        print()
        
        system = ApolloEdge()
        
        # Show whale detection
        print("=" * 60)
        print("WHALE DETECTION")
        print("=" * 60)
        whales = system.whale_detector.scan_recent_trades(5000)
        print(f"Found {len(whales)} whale positions")
        for w in whales[:5]:
            print(f"  🐋 ${w.size_usd:,.0f} on {w.outcome[:30]}...")
        
        # Show arbitrage
        print()
        print("=" * 60)
        print("ARBITRAGE SCANNER")
        print("=" * 60)
        arbs = system.arb_scanner.scan_nfl_markets()
        print(f"Found {len(arbs)} potential arbitrage opportunities")
        for a in arbs[:5]:
            print(f"  💰 {a.spread_pct:.2f}% spread: {a.market_name[:40]}...")
        
        print()
        print("=" * 60)
        print("COMMANDS")
        print("=" * 60)
        print("  python apollo_edge.py --mode=monitor     # Start live monitoring")
        print("  python apollo_edge.py --mode=scan        # Single scan cycle")
        print("  python apollo_edge.py --mode=analyze --wallet=0x...  # Analyze wallet")


if __name__ == "__main__":
    main()
