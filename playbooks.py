#!/usr/bin/env python3
"""
APOLLO EDGE - PLAYBOOKS & PLAYLISTS
====================================
Pre-configured trading strategies that auto-execute based on conditions.

PLAYLIST TYPES:
1. Playbooks - Conditional strategies ("if X then Y")
2. Watchlists - Curated wallets/markets to monitor
3. Signal Queues - Prioritized trading opportunities
4. Arbitrage Routes - Cross-platform execution paths

USAGE:
    python playbooks.py --list
    python playbooks.py --run patriots_playbook
    python playbooks.py --create
"""

import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('Playbooks')


# ============================================================================
# ENUMS & TYPES
# ============================================================================

class PlaybookType(Enum):
    """Types of playbooks"""
    WHALE_FOLLOW = "whale_follow"           # Follow whale trades
    MARKET_CONDITION = "market_condition"   # Based on market state
    ARBITRAGE = "arbitrage"                 # Cross-platform arb
    CLUSTER = "cluster"                     # Coordinated wallet activity
    TIME_BASED = "time_based"               # Time-triggered
    COMBO = "combo"                         # Multiple conditions


class ConditionOperator(Enum):
    """Comparison operators"""
    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    CONTAINS = "contains"
    IN = "in"


class ActionType(Enum):
    """Types of actions"""
    BUY = "buy"
    SELL = "sell"
    ALERT = "alert"
    WAIT = "wait"
    CANCEL = "cancel"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Condition:
    """A single condition to check"""
    field: str                      # What to check (e.g., "whale_size", "market_price")
    operator: ConditionOperator     # How to compare
    value: Any                      # Value to compare against
    
    def evaluate(self, data: Dict) -> bool:
        """Evaluate if condition is met"""
        if self.field not in data:
            return False
        
        actual = data[self.field]
        target = self.value
        
        if self.operator == ConditionOperator.GREATER_THAN:
            return actual > target
        elif self.operator == ConditionOperator.LESS_THAN:
            return actual < target
        elif self.operator == ConditionOperator.EQUAL:
            return actual == target
        elif self.operator == ConditionOperator.NOT_EQUAL:
            return actual != target
        elif self.operator == ConditionOperator.GREATER_EQUAL:
            return actual >= target
        elif self.operator == ConditionOperator.LESS_EQUAL:
            return actual <= target
        elif self.operator == ConditionOperator.CONTAINS:
            return str(target).lower() in str(actual).lower()
        elif self.operator == ConditionOperator.IN:
            return actual in target
        
        return False


@dataclass
class Action:
    """An action to execute"""
    action_type: ActionType
    params: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "action_type": self.action_type.value,
            "params": self.params
        }


@dataclass
class Playbook:
    """A pre-configured trading strategy"""
    id: str
    name: str
    description: str
    playbook_type: PlaybookType
    enabled: bool = True
    
    # Conditions (ALL must be true)
    conditions: List[Condition] = field(default_factory=list)
    
    # Actions to execute when conditions met
    actions: List[Action] = field(default_factory=list)
    
    # Settings
    cooldown_seconds: int = 60      # Min time between executions
    max_executions: int = 100       # Max times to execute
    expire_at: Optional[datetime] = None
    
    # Tracking
    execution_count: int = 0
    last_execution: Optional[datetime] = None
    total_pnl: float = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def can_execute(self) -> bool:
        """Check if playbook can be executed"""
        if not self.enabled:
            return False
        
        if self.execution_count >= self.max_executions:
            return False
        
        if self.expire_at and datetime.now() > self.expire_at:
            return False
        
        if self.last_execution:
            elapsed = (datetime.now() - self.last_execution).total_seconds()
            if elapsed < self.cooldown_seconds:
                return False
        
        return True
    
    def evaluate(self, data: Dict) -> bool:
        """Check if all conditions are met"""
        if not self.can_execute():
            return False
        
        return all(condition.evaluate(data) for condition in self.conditions)
    
    def execute(self) -> List[Action]:
        """Mark as executed and return actions"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        return self.actions
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.playbook_type.value,
            "enabled": self.enabled,
            "execution_count": self.execution_count,
            "total_pnl": self.total_pnl,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class Watchlist:
    """Curated list of items to monitor"""
    id: str
    name: str
    description: str
    watch_type: str  # "wallets", "markets", "tokens"
    items: List[str] = field(default_factory=list)
    
    # Associated playbooks (auto-trigger when items match)
    playbooks: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None
    activity_count: int = 0
    
    def contains(self, item: str) -> bool:
        """Check if item is in watchlist"""
        return item.lower() in [i.lower() for i in self.items]
    
    def add(self, item: str):
        """Add item to watchlist"""
        if not self.contains(item):
            self.items.append(item)
            logger.info(f"Added {item} to watchlist '{self.name}'")
    
    def remove(self, item: str):
        """Remove item from watchlist"""
        self.items = [i for i in self.items if i.lower() != item.lower()]
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.watch_type,
            "items": self.items,
            "playbooks": self.playbooks,
            "activity_count": self.activity_count
        }


@dataclass
class SignalQueueItem:
    """Prioritized trading signal"""
    id: str
    signal_type: str
    priority: int  # 0-100, higher = more urgent
    confidence: float  # 0-100
    expected_edge: float  # Expected profit %
    
    # Trade details
    market_id: str
    outcome: str
    direction: str  # buy/sell
    size_usd: float
    target_price: float
    
    # Metadata
    reason: str
    expires_at: datetime
    created_at: datetime = field(default_factory=datetime.now)
    source_playbook: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    @property
    def score(self) -> float:
        """Calculate overall score for prioritization"""
        # Weight: priority 40%, confidence 30%, edge 30%
        return (self.priority * 0.4 + self.confidence * 0.3 + 
                min(100, self.expected_edge * 10) * 0.3)
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


@dataclass
class ArbitrageRoute:
    """Cross-platform arbitrage execution path"""
    id: str
    name: str
    
    # Platforms in order
    buy_platform: str
    sell_platform: str
    
    # Optional: intermediate steps for complex arb
    intermediate_steps: List[Dict] = field(default_factory=list)
    
    # Constraints
    min_spread_pct: float = 2.0
    max_size_usd: float = 10000
    max_slippage_pct: float = 1.0
    
    # Performance tracking
    execution_count: int = 0
    total_profit: float = 0
    avg_spread: float = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "buy_platform": self.buy_platform,
            "sell_platform": self.sell_platform,
            "execution_count": self.execution_count,
            "total_profit": self.total_profit,
            "avg_spread": self.avg_spread
        }


# ============================================================================
# PRE-BUILT PLAYBOOKS
# ============================================================================

PRESET_PLAYBOOKS = {
    # ========================================================================
    # WHALE DETECTION & SNIPING PLAYBOOKS
    # ========================================================================
    
    "whale_snipe_10k": {
        "name": "Whale Snipe $10K+",
        "description": "Auto-detect and follow whales trading > $10K",
        "type": PlaybookType.WHALE_FOLLOW,
        "conditions": [
            {"field": "whale_size", "operator": ">", "value": 10000},
            {"field": "whale_confidence", "operator": ">", "value": 70},
            {"field": "whale_action", "operator": "==", "value": "buy"}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 1000, "follow_pct": 0.10}}
        ],
        "cooldown": 300,
        "max_executions": 20
    },
    
    "whale_snipe_25k": {
        "name": "Whale Snipe $25K+ (Auto)",
        "description": "Auto-snipe whales > $25K with sub-second execution",
        "type": PlaybookType.WHALE_FOLLOW,
        "conditions": [
            {"field": "whale_size", "operator": ">", "value": 25000},
            {"field": "whale_confidence", "operator": ">", "value": 75},
            {"field": "whale_action", "operator": "==", "value": "buy"}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 2500, "follow_pct": 0.10, "fast_execution": True}}
        ],
        "cooldown": 180,  # 3 minutes
        "max_executions": 20
    },
    
    "patriots_whale_follow": {
        "name": "Patriots Whale Follow",
        "description": "Follow Patriots whales > $50K",
        "type": PlaybookType.WHALE_FOLLOW,
        "conditions": [
            {"field": "whale_size", "operator": ">", "value": 50000},
            {"field": "market_name", "operator": "contains", "value": "patriots"},
            {"field": "whale_action", "operator": "==", "value": "buy"}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 5000, "follow_pct": 0.10}}
        ],
        "cooldown": 300,
        "max_executions": 10
    },
    
    "chiefs_value": {
        "name": "Chiefs Value Play",
        "description": "Buy Chiefs when odds drop below 30%",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "market_name", "operator": "contains", "value": "chiefs"},
            {"field": "price", "operator": "<", "value": 0.30},
            {"field": "volume", "operator": ">", "value": 100000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 2000, "limit_price": 0.30}}
        ],
        "cooldown": 3600,  # 1 hour
        "max_executions": 3
    },
    
    # ========================================================================
    # SPORTSBOOK VALUE DETECTION (ARBITRAGE REPLACEMENT)
    # ========================================================================
    
    "sportsbook_value_mvp": {
        "name": "MVP Value vs Sportsbooks",
        "description": "Find undervalued MVP markets vs 50+ sportsbooks",
        "type": PlaybookType.ARBITRAGE,
        "conditions": [
            {"field": "market_category", "operator": "==", "value": "mvp"},
            {"field": "sportsbook_avg_prob", "operator": ">", "value": 0.65},
            {"field": "polymarket_price", "operator": "<", "value": 0.55},
            {"field": "liquidity", "operator": ">", "value": 50000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 2000, "reason": "Undervalued vs sportsbooks"}}
        ],
        "cooldown": 300,
        "max_executions": 30
    },
    
    "sportsbook_value_superbowl": {
        "name": "Super Bowl Value Detector",
        "description": "Find Super Bowl value vs sportsbook consensus",
        "type": PlaybookType.ARBITRAGE,
        "conditions": [
            {"field": "market_name", "operator": "contains", "value": "super bowl"},
            {"field": "sportsbook_avg_prob", "operator": ">", "value": 0.70},
            {"field": "polymarket_price", "operator": "<", "value": 0.60},
            {"field": "volume", "operator": ">", "value": 100000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 3000}}
        ],
        "cooldown": 600,
        "max_executions": 15
    },
    
    # ========================================================================
    # 5-HOP CLUSTER ANALYSIS PLAYBOOKS
    # ========================================================================
    
    "whale_cluster_alert": {
        "name": "Coordinated Whale Cluster",
        "description": "Detect 3+ coordinated wallets (like Théo's 11-wallet pattern)",
        "type": PlaybookType.CLUSTER,
        "conditions": [
            {"field": "cluster_wallets_active", "operator": ">=", "value": 3},
            {"field": "total_cluster_size", "operator": ">", "value": 75000},
            {"field": "cluster_confidence", "operator": ">", "value": 80}
        ],
        "actions": [
            {"type": "alert", "params": {"priority": "high", "message": "Coordinated whale activity detected"}},
            {"type": "buy", "params": {"size": 5000, "wait_seconds": 30}}
        ],
        "cooldown": 600,
        "max_executions": 15
    },
    
    "cex_whale_detector": {
        "name": "CEX Whale Tracker",
        "description": "Track whales funded from Binance, Coinbase, OKX",
        "type": PlaybookType.CLUSTER,
        "conditions": [
            {"field": "funding_source", "operator": "in", "value": ["binance", "coinbase", "okx"]},
            {"field": "whale_size", "operator": ">", "value": 50000},
            {"field": "hops_to_cex", "operator": "<=", "value": 3}
        ],
        "actions": [
            {"type": "alert", "params": {"priority": "medium"}},
            {"type": "buy", "params": {"size": 2500, "follow_pct": 0.05}}
        ],
        "cooldown": 300,
        "max_executions": 20
    },
    
    "bridge_whale_tracker": {
        "name": "Bridge Whale Tracker",
        "description": "Track large deposits via Wormhole/Polygon Bridge",
        "type": PlaybookType.CLUSTER,
        "conditions": [
            {"field": "bridge_source", "operator": "in", "value": ["wormhole", "polygon_bridge"]},
            {"field": "transfer_size", "operator": ">", "value": 100000},
            {"field": "time_since_bridge", "operator": "<", "value": 3600}  # Within 1 hour
        ],
        "actions": [
            {"type": "alert", "params": {"priority": "high", "message": "Large bridge deposit detected"}},
        ],
        "cooldown": 600,
        "max_executions": 10
    },
    
    # ========================================================================
    # NFL PROPS COVERAGE PLAYBOOKS
    # ========================================================================
    
    "superbowl_momentum": {
        "name": "Super Bowl Momentum",
        "description": "Follow rapid price movements on SB Champion markets",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "market_name", "operator": "contains", "value": "super bowl"},
            {"field": "price_change_5m", "operator": ">", "value": 0.05},  # 5% in 5 min
            {"field": "volume_5m", "operator": ">", "value": 50000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 1500, "follow_momentum": True}}
        ],
        "cooldown": 300,
        "max_executions": 15
    },
    
    "afc_nfc_champion_value": {
        "name": "Conference Champion Value",
        "description": "AFC/NFC champion markets with whale activity",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "market_category", "operator": "in", "value": ["afc_champion", "nfc_champion"]},
            {"field": "whale_size", "operator": ">", "value": 20000},
            {"field": "sportsbook_confirmation", "operator": "==", "value": True}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 2000}}
        ],
        "cooldown": 600,
        "max_executions": 10
    },
    
    "player_props_whale": {
        "name": "Player Props Whale Follow",
        "description": "Follow whales on player props (yards, TDs, receptions)",
        "type": PlaybookType.WHALE_FOLLOW,
        "conditions": [
            {"field": "market_category", "operator": "in", "value": ["passing_yards", "rushing_yards", "receiving_yards", "touchdowns"]},
            {"field": "whale_size", "operator": ">", "value": 15000},
            {"field": "whale_confidence", "operator": ">", "value": 75}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 1500, "follow_pct": 0.10}}
        ],
        "cooldown": 180,
        "max_executions": 25
    },
    
    "game_props_value": {
        "name": "Game Props Value",
        "description": "Spreads, totals, moneylines with sportsbook edge",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "market_category", "operator": "in", "value": ["spread", "total", "moneyline"]},
            {"field": "sportsbook_edge", "operator": ">", "value": 0.10},  # 10% edge
            {"field": "liquidity", "operator": ">", "value": 25000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 1000}}
        ],
        "cooldown": 300,
        "max_executions": 30
    },
    
    "division_winner_early": {
        "name": "Division Winner Early Bird",
        "description": "Division winners with whale + sportsbook consensus",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "market_category", "operator": "==", "value": "division_winner"},
            {"field": "whale_size", "operator": ">", "value": 30000},
            {"field": "sportsbook_avg_prob", "operator": ">", "value": 0.60},
            {"field": "polymarket_price", "operator": "<", "value": 0.50}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 2500}}
        ],
        "cooldown": 3600,  # 1 hour
        "max_executions": 8
    },
    
    "superbowl_props_whale": {
        "name": "Super Bowl Props Whale",
        "description": "SB props (first TD, halftime, etc.) with whale activity",
        "type": PlaybookType.WHALE_FOLLOW,
        "conditions": [
            {"field": "market_name", "operator": "contains", "value": "super bowl"},
            {"field": "market_category", "operator": "in", "value": ["first_td", "halftime", "gatorade_color"]},
            {"field": "whale_size", "operator": ">", "value": 10000}
        ],
        "actions": [
            {"type": "buy", "params": {"size": 1000, "follow_pct": 0.10}}
        ],
        "cooldown": 300,
        "max_executions": 15
    },
    
    "fade_the_public": {
        "name": "Fade The Public",
        "description": "Contrarian: Sell when public heavily buys",
        "type": PlaybookType.MARKET_CONDITION,
        "conditions": [
            {"field": "public_buy_volume", "operator": ">", "value": 0.80},  # 80% buys
            {"field": "price", "operator": ">", "value": 0.70},
            {"field": "whale_participation", "operator": "<", "value": 0.20}  # No whales
        ],
        "actions": [
            {"type": "sell", "params": {"size": 1500}}
        ],
        "cooldown": 1800,
        "max_executions": 10
    }
}


PRESET_WATCHLISTS = {
    "top_whales": {
        "name": "Top 10 Whales",
        "description": "Most successful whale wallets",
        "type": "wallets",
        "items": [
            "0x0000000000000000000000000000000000000001",  # Placeholder - add real whales
            "0x0000000000000000000000000000000000000002",
        ]
    },
    
    "superbowl_markets": {
        "name": "Super Bowl Markets",
        "description": "All Super Bowl related markets",
        "type": "markets",
        "items": ["super bowl", "sb59", "championship"]
    },
    
    "mvp_candidates": {
        "name": "MVP Candidates",
        "description": "Top MVP contenders",
        "type": "markets",
        "items": ["mahomes", "allen", "lamar", "purdy", "stroud"]
    },
    
    "high_volume_markets": {
        "name": "High Volume Markets",
        "description": "Markets with > $1M volume",
        "type": "markets",
        "items": []  # Dynamically populated
    }
}


# ============================================================================
# PLAYBOOK MANAGER
# ============================================================================

class PlaybookManager:
    """Manages all playbooks and playlists"""
    
    def __init__(self, storage_file: str = "playbooks.json"):
        self.storage_file = storage_file
        self.playbooks: Dict[str, Playbook] = {}
        self.watchlists: Dict[str, Watchlist] = {}
        self.signal_queue: List[SignalQueueItem] = []
        self.arb_routes: Dict[str, ArbitrageRoute] = {}
        
        self.callbacks = []
        
        self.load()
    
    # ========================================================================
    # PLAYBOOK METHODS
    # ========================================================================
    
    def add_playbook(self, playbook: Playbook):
        """Add playbook to manager"""
        self.playbooks[playbook.id] = playbook
        logger.info(f"Added playbook: {playbook.name}")
        self.save()
    
    def load_preset_playbook(self, preset_id: str) -> Optional[Playbook]:
        """Load a preset playbook"""
        if preset_id not in PRESET_PLAYBOOKS:
            logger.error(f"Unknown preset: {preset_id}")
            return None
        
        preset = PRESET_PLAYBOOKS[preset_id]
        
        # Build conditions
        conditions = []
        for cond in preset["conditions"]:
            conditions.append(Condition(
                field=cond["field"],
                operator=ConditionOperator(cond["operator"]),
                value=cond["value"]
            ))
        
        # Build actions
        actions = []
        for act in preset["actions"]:
            actions.append(Action(
                action_type=ActionType(act["type"]),
                params=act["params"]
            ))
        
        playbook = Playbook(
            id=preset_id,
            name=preset["name"],
            description=preset["description"],
            playbook_type=preset["type"],
            conditions=conditions,
            actions=actions,
            cooldown_seconds=preset.get("cooldown", 60),
            max_executions=preset.get("max_executions", 100)
        )
        
        self.add_playbook(playbook)
        return playbook
    
    def evaluate_playbooks(self, data: Dict) -> List[Action]:
        """Evaluate all playbooks against data"""
        actions_to_execute = []
        
        for playbook in self.playbooks.values():
            if playbook.evaluate(data):
                logger.info(f"✅ Playbook triggered: {playbook.name}")
                actions = playbook.execute()
                actions_to_execute.extend(actions)
                
                # Emit callback
                self._emit_playbook_triggered(playbook, data)
        
        return actions_to_execute
    
    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        return self.playbooks.get(playbook_id)
    
    def list_playbooks(self) -> List[Dict]:
        """Get list of all playbooks"""
        return [pb.to_dict() for pb in self.playbooks.values()]
    
    # ========================================================================
    # WATCHLIST METHODS
    # ========================================================================
    
    def add_watchlist(self, watchlist: Watchlist):
        """Add watchlist"""
        self.watchlists[watchlist.id] = watchlist
        logger.info(f"Added watchlist: {watchlist.name}")
        self.save()
    
    def load_preset_watchlist(self, preset_id: str) -> Optional[Watchlist]:
        """Load preset watchlist"""
        if preset_id not in PRESET_WATCHLISTS:
            logger.error(f"Unknown watchlist preset: {preset_id}")
            return None
        
        preset = PRESET_WATCHLISTS[preset_id]
        
        watchlist = Watchlist(
            id=preset_id,
            name=preset["name"],
            description=preset["description"],
            watch_type=preset["type"],
            items=preset["items"]
        )
        
        self.add_watchlist(watchlist)
        return watchlist
    
    def check_watchlists(self, item_type: str, item_value: str) -> List[Watchlist]:
        """Check if item is in any watchlists"""
        matches = []
        for wl in self.watchlists.values():
            if wl.watch_type == item_type and wl.contains(item_value):
                wl.activity_count += 1
                wl.last_activity = datetime.now()
                matches.append(wl)
        return matches
    
    def list_watchlists(self) -> List[Dict]:
        """Get list of all watchlists"""
        return [wl.to_dict() for wl in self.watchlists.values()]
    
    # ========================================================================
    # SIGNAL QUEUE METHODS
    # ========================================================================
    
    def add_signal(self, signal: SignalQueueItem):
        """Add signal to priority queue"""
        # Remove expired signals
        self.signal_queue = [s for s in self.signal_queue if not s.is_expired()]
        
        # Add new signal
        self.signal_queue.append(signal)
        
        # Sort by score (highest first)
        self.signal_queue.sort(key=lambda s: s.score, reverse=True)
        
        logger.info(f"Added signal to queue: {signal.id} (score: {signal.score:.1f})")
    
    def get_top_signals(self, limit: int = 10) -> List[SignalQueueItem]:
        """Get top N signals from queue"""
        # Remove expired
        self.signal_queue = [s for s in self.signal_queue if not s.is_expired()]
        return self.signal_queue[:limit]
    
    def pop_signal(self) -> Optional[SignalQueueItem]:
        """Get and remove top signal"""
        if not self.signal_queue:
            return None
        return self.signal_queue.pop(0)
    
    def clear_queue(self):
        """Clear all signals"""
        self.signal_queue.clear()
    
    # ========================================================================
    # ARBITRAGE ROUTE METHODS
    # ========================================================================
    
    def add_arb_route(self, route: ArbitrageRoute):
        """Add arbitrage route"""
        self.arb_routes[route.id] = route
        logger.info(f"Added arb route: {route.name}")
        self.save()
    
    def get_route(self, route_id: str) -> Optional[ArbitrageRoute]:
        return self.arb_routes.get(route_id)
    
    def list_arb_routes(self) -> List[Dict]:
        """Get list of all arbitrage routes"""
        return [route.to_dict() for route in self.arb_routes.values()]
    
    # ========================================================================
    # CALLBACKS
    # ========================================================================
    
    def on_playbook_triggered(self, callback: Callable):
        """Register callback for playbook triggers"""
        self.callbacks.append(callback)
    
    def _emit_playbook_triggered(self, playbook: Playbook, data: Dict):
        for callback in self.callbacks:
            try:
                callback(playbook, data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    # ========================================================================
    # PERSISTENCE
    # ========================================================================
    
    def save(self):
        """Save all data to file"""
        try:
            data = {
                "playbooks": [
                    {
                        **pb.to_dict(),
                        "conditions": [asdict(c) for c in pb.conditions],
                        "actions": [a.to_dict() for a in pb.actions]
                    }
                    for pb in self.playbooks.values()
                ],
                "watchlists": [wl.to_dict() for wl in self.watchlists.values()],
                "arb_routes": [route.to_dict() for route in self.arb_routes.values()]
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
            logger.debug(f"Saved playbooks to {self.storage_file}")
        except Exception as e:
            logger.error(f"Save error: {e}")
    
    def load(self):
        """Load data from file"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Load playbooks (simplified - full reconstruction needed)
            logger.info(f"Loaded {len(data.get('playbooks', []))} playbooks")
            logger.info(f"Loaded {len(data.get('watchlists', []))} watchlists")
            logger.info(f"Loaded {len(data.get('arb_routes', []))} arb routes")
            
        except FileNotFoundError:
            logger.info("No saved playbooks found, starting fresh")
        except Exception as e:
            logger.error(f"Load error: {e}")


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Apollo Edge Playbooks")
    parser.add_argument("--list", action="store_true", help="List all playbooks")
    parser.add_argument("--list-watchlists", action="store_true", help="List watchlists")
    parser.add_argument("--list-signals", action="store_true", help="List signal queue")
    parser.add_argument("--load-preset", type=str, help="Load preset playbook")
    parser.add_argument("--create", action="store_true", help="Interactive playbook creator")
    
    args = parser.parse_args()
    
    manager = PlaybookManager()
    
    if args.list:
        print("\n" + "="*60)
        print("PLAYBOOKS")
        print("="*60)
        playbooks = manager.list_playbooks()
        if not playbooks:
            print("No playbooks loaded. Try: --load-preset patriots_whale_follow")
        for pb in playbooks:
            print(f"\n{pb['name']}")
            print(f"  Type: {pb['type']}")
            print(f"  Executions: {pb['execution_count']}")
            print(f"  P&L: ${pb['total_pnl']:,.2f}")
            print(f"  Enabled: {'✅' if pb['enabled'] else '❌'}")
    
    elif args.list_watchlists:
        print("\n" + "="*60)
        print("WATCHLISTS")
        print("="*60)
        for wl in manager.list_watchlists():
            print(f"\n{wl['name']} ({wl['type']})")
            print(f"  Items: {len(wl['items'])}")
            print(f"  Activity: {wl['activity_count']}")
    
    elif args.list_signals:
        print("\n" + "="*60)
        print("SIGNAL QUEUE")
        print("="*60)
        signals = manager.get_top_signals(20)
        for i, sig in enumerate(signals, 1):
            print(f"\n{i}. {sig.signal_type} (Score: {sig.score:.1f})")
            print(f"   Market: {sig.market_id}")
            print(f"   Direction: {sig.direction} ${sig.size_usd:,.0f}")
            print(f"   Confidence: {sig.confidence:.0f}% | Edge: {sig.expected_edge:.1f}%")
    
    elif args.load_preset:
        print(f"\n[*] Loading preset: {args.load_preset}")
        playbook = manager.load_preset_playbook(args.load_preset)
        if playbook:
            print(f"[SUCCESS] Loaded: {playbook.name}")
            print(f"          {playbook.description}")
    
    elif args.create:
        print("\n" + "="*60)
        print("INTERACTIVE PLAYBOOK CREATOR")
        print("="*60)
        print("\nAvailable presets:")
        for i, (key, preset) in enumerate(PRESET_PLAYBOOKS.items(), 1):
            print(f"  {i}. {preset['name']}")
            print(f"     {preset['description']}")
        print("\nUse: --load-preset <preset_id>")
    
    else:
        print("\n" + "="*60)
        print("APOLLO EDGE PLAYBOOKS")
        print("="*60)
        print("\nAvailable Presets:")
        for key, preset in PRESET_PLAYBOOKS.items():
            print(f"\n  • {preset['name']}")
            print(f"    {preset['description']}")
            print(f"    Load: --load-preset {key}")
        
        print("\n" + "="*60)
        print("COMMANDS")
        print("="*60)
        print("  --list                 List all playbooks")
        print("  --list-watchlists      List all watchlists")
        print("  --list-signals         Show signal queue")
        print("  --load-preset <id>     Load preset playbook")
        print("  --create               Create custom playbook")


if __name__ == "__main__":
    main()

