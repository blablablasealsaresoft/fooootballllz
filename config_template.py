"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        APOLLO EDGE - CONFIGURATION                            ║
║                                                                               ║
║  ⚠️  SECURITY WARNING: This file contains sensitive credentials!              ║
║      - NEVER commit this file to git                                          ║
║      - NEVER share this file with anyone                                      ║
║      - Add to .gitignore immediately                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

SETUP INSTRUCTIONS:
1. Fill in your credentials below
2. Rename this file to: config.py
3. The system will auto-load your credentials

"""

# ============================================================================
# 🔑 API KEYS
# ============================================================================

# Etherscan V2 API Key (already provided - works for all chains)
ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

# TheOddsAPI (optional - for sportsbook odds)
# Get free key at: https://the-odds-api.com/
ODDS_API_KEY = "31c44bdb909ce897b097756c9bb52eec"

# Kalshi API (optional - for Kalshi trading)
# Get at: https://kalshi.com/api
KALSHI_API_KEY = ""
KALSHI_API_SECRET = ""


# ============================================================================
# 💰 YOUR TRADING WALLET - POLYMARKET (POLYGON NETWORK)
# ============================================================================

# Your Polygon wallet address (starts with 0x)
# This is the wallet that will execute trades on Polymarket
TRADING_WALLET_ADDRESS = "0x7F4c4646e78Cb88021879C4C5AaaCaD627E9924B"

# Your private key (starts with 0x, 64 hex characters after 0x)
# ⚠️  NEVER SHARE THIS WITH ANYONE
# ⚠️  KEEP A BACKUP - LOSING THIS = LOSING ALL FUNDS
TRADING_WALLET_PRIVATE_KEY = "0xYOUR_PRIVATE_KEY_HERE"

# Polymarket API credentials (optional - for higher rate limits)
# Get at: https://docs.polymarket.com
POLYMARKET_API_KEY = ""
POLYMARKET_API_SECRET = ""
POLYMARKET_PASSPHRASE = ""


# ============================================================================
# 💵 FUNDING SETTINGS
# ============================================================================

# USDC balance reserved (won't trade below this amount)
MIN_USDC_RESERVE = 100  # Keep at least $100 in wallet

# Maximum USDC to use for trading (safety limit)
MAX_TRADING_CAPITAL = 10000  # Max $10K active in trades


# ============================================================================
# 🐋 WHALE DETECTION SETTINGS
# ============================================================================

# Minimum whale position size to track
MIN_WHALE_SIZE_USD = 10000

# Minimum whale size to auto-snipe (set higher for safety)
SNIPE_THRESHOLD_USD = 25000

# Minimum confidence score to auto-trade (0-100)
MIN_CONFIDENCE_SCORE = 70


# ============================================================================
# ⚡ EXECUTION SETTINGS
# ============================================================================

# Follow percentage (how much of whale position to copy)
# 0.10 = 10% of whale size
FOLLOW_PERCENTAGE = 0.10

# Maximum size per trade in USD
MAX_POSITION_SIZE_USD = 5000

# Maximum slippage tolerance (percentage)
MAX_SLIPPAGE_PCT = 1.0

# Order type: "market" or "limit"
DEFAULT_ORDER_TYPE = "limit"

# For limit orders: how far from market price (percentage)
LIMIT_ORDER_OFFSET_PCT = 0.5


# ============================================================================
# 📊 RISK MANAGEMENT
# ============================================================================

# Maximum number of snipes per day
MAX_DAILY_SNIPES = 20

# Maximum concurrent open positions
MAX_CONCURRENT_POSITIONS = 10

# Stop loss percentage (close position if down this much)
STOP_LOSS_PCT = 15.0

# Take profit percentage (close position if up this much)
TAKE_PROFIT_PCT = 50.0

# Maximum portfolio allocation per position (percentage)
MAX_POSITION_PCT = 20.0

# Maximum daily loss before stopping (USD)
MAX_DAILY_LOSS_USD = 2000

# Time-based stop: close position after X hours regardless
MAX_HOLD_HOURS = 168  # 1 week


# ============================================================================
# 🔔 ALERTS & NOTIFICATIONS
# ============================================================================

# Telegram alerts (optional)
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Discord webhook (optional)
DISCORD_WEBHOOK_URL = ""

# Email alerts (optional)
EMAIL_SMTP_SERVER = ""
EMAIL_USERNAME = ""
EMAIL_PASSWORD = ""
EMAIL_TO = ""


# ============================================================================
# 🌐 NETWORK SETTINGS
# ============================================================================

# Polygon RPC endpoints (use your own for better speed)
POLYGON_RPC_URL = "https://polygon-rpc.com"
POLYGON_RPC_BACKUP = "https://rpc-mainnet.matic.quiknode.pro"

# Gas settings
GAS_PRICE_GWEI = "auto"  # "auto" or specific number like 50
MAX_GAS_PRICE_GWEI = 500  # Won't submit if gas exceeds this

# Polling interval (milliseconds)
POLL_INTERVAL_MS = 500


# ============================================================================
# 🎯 MARKET FILTERS
# ============================================================================

# Only trade these markets (empty = all markets)
WHITELIST_MARKETS = [
    # "super-bowl-champion",
    # "afc-champion",
    # "nfc-champion",
]

# Never trade these markets
BLACKLIST_MARKETS = []

# Only follow these whale wallets (empty = follow all)
WHITELIST_WHALES = []

# Never follow these wallets
BLACKLIST_WHALES = [
    # Known bots, market makers, etc.
]


# ============================================================================
# 🔧 ADVANCED SETTINGS
# ============================================================================

# Enable paper trading (simulated trades, no real execution)
PAPER_TRADING_MODE = True  # SET TO False FOR REAL TRADING

# Enable detailed logging
DEBUG_MODE = True

# Log file location
LOG_FILE = "apollo_edge.log"

# Database for trade history (SQLite)
DATABASE_FILE = "apollo_edge.db"


# ============================================================================
# 📋 PLAYBOOKS & PLAYLISTS
# ============================================================================

# Enable automatic playbook execution
ENABLE_PLAYBOOKS = True

# Playbooks storage file
PLAYBOOKS_FILE = "playbooks.json"

# Auto-load these preset playbooks on startup
AUTO_LOAD_PLAYBOOKS = [
    "patriots_whale_follow",
    "chiefs_value",
    "mvp_arb",
    # "whale_cluster_alert",
    # "superbowl_momentum",
    # "fade_the_public",
]

# Auto-load these watchlists
AUTO_LOAD_WATCHLISTS = [
    "top_whales",
    "superbowl_markets",
    "mvp_candidates",
]

# Signal queue settings
SIGNAL_QUEUE_MAX_SIZE = 100
SIGNAL_QUEUE_AUTO_EXECUTE = True  # Auto-execute top signals
SIGNAL_QUEUE_EXECUTION_INTERVAL = 5  # Execute top signal every N seconds
