"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     APOLLO EDGE - EXAMPLE FULL CONFIGURATION                  ║
║                                                                               ║
║  This is a COMPLETE example showing ALL possible settings.                   ║
║  Copy sections you need to your config.py                                    ║
║                                                                               ║
║  ⚠️  DO NOT rename this file to config.py - it's just an example!            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# 🔑 API KEYS
# ============================================================================

# Etherscan V2 API Key (ALREADY PROVIDED - works for all chains)
ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

# ============================================================================
# 🔐 KALSHI API (Optional - for cross-platform arbitrage)
# ============================================================================
# Get your key at: https://kalshi.com/account/profile
# See: KALSHI_INTEGRATION.md for full guide

# Kalshi Key ID (UUID format from Kalshi)
KALSHI_API_KEY = ""  # Example: "a952bcbe-ec3b-4b5b-b8f9-11dae589608c"

# Option 1: Path to private key file (RECOMMENDED)
KALSHI_PRIVATE_KEY_PATH = "kalshi_private_key.pem"

# Option 2: Paste key directly (less secure)
KALSHI_PRIVATE_KEY = ""  # Leave empty if using file path

# Kalshi API URL
KALSHI_API_URL = "https://trading-api.kalshi.com"  # Production
# KALSHI_API_URL = "https://demo-api.kalshi.co"    # Demo/Testing


# ============================================================================
# 🏗️ POLYMARKET BUILDER RELAYER (Optional - for gasless trading)
# ============================================================================
# See: POLYMARKET_BUILDER_GUIDE.md for full guide

# Enable gasless trading (relayer pays gas)
USE_BUILDER_RELAYER = True  # Set False to use direct wallet (requires MATIC)

# Relayer URL
POLYMARKET_RELAYER_URL = "https://relayer.polymarket.com"

# Wallet type: "SAFE" or "PROXY"
# PROXY = Simpler, faster, recommended for individuals
# SAFE = More secure, multi-sig, good for institutions
POLYMARKET_WALLET_TYPE = "PROXY"

# Your proxy wallet address (system fills this in after first deployment)
POLYMARKET_PROXY_ADDRESS = ""  # Leave empty initially


# ============================================================================
# 💰 YOUR TRADING WALLET - POLYMARKET (POLYGON NETWORK)
# ============================================================================

# Your Polygon wallet address (starts with 0x)
# This is the wallet that will execute trades on Polymarket
TRADING_WALLET_ADDRESS = "0xYOUR_WALLET_ADDRESS_HERE"

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
# 🔔 ALERTS & NOTIFICATIONS (Optional)
# ============================================================================

# Telegram alerts
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Discord webhook
DISCORD_WEBHOOK_URL = ""

# Email alerts
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

# Gas settings (only if not using Builder Relayer)
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
# 📝 CONFIGURATION PROFILES
# ============================================================================

# You can create multiple profiles for different strategies

# CONSERVATIVE PROFILE
"""
MIN_WHALE_SIZE_USD = 50000
SNIPE_THRESHOLD_USD = 100000
MIN_CONFIDENCE_SCORE = 85
MAX_POSITION_SIZE_USD = 1000
FOLLOW_PERCENTAGE = 0.05
MAX_DAILY_SNIPES = 5
"""

# AGGRESSIVE PROFILE
"""
MIN_WHALE_SIZE_USD = 5000
SNIPE_THRESHOLD_USD = 10000
MIN_CONFIDENCE_SCORE = 60
MAX_POSITION_SIZE_USD = 10000
FOLLOW_PERCENTAGE = 0.20
MAX_DAILY_SNIPES = 50
"""

# BALANCED PROFILE (default)
"""
MIN_WHALE_SIZE_USD = 10000
SNIPE_THRESHOLD_USD = 25000
MIN_CONFIDENCE_SCORE = 70
MAX_POSITION_SIZE_USD = 5000
FOLLOW_PERCENTAGE = 0.10
MAX_DAILY_SNIPES = 20
"""


# ============================================================================
# 🎯 QUICK START CONFIGURATIONS
# ============================================================================

# MONITORING ONLY (no trading, just watch)
"""
PAPER_TRADING_MODE = True
ENABLE_PLAYBOOKS = False
# Don't need wallet configured
"""

# PAPER TRADING (testing strategies)
"""
PAPER_TRADING_MODE = True
TRADING_WALLET_ADDRESS = "0xYourAddressHere"  # Optional
ENABLE_PLAYBOOKS = True
AUTO_LOAD_PLAYBOOKS = ["patriots_whale_follow"]
"""

# LIVE TRADING (real money - start small!)
"""
PAPER_TRADING_MODE = False
TRADING_WALLET_ADDRESS = "0xYourAddressHere"
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"
MAX_POSITION_SIZE_USD = 100  # START TINY!
MAX_DAILY_SNIPES = 5
USE_BUILDER_RELAYER = True  # Gasless trading
"""

# ADVANCED: WITH KALSHI ARBITRAGE
"""
PAPER_TRADING_MODE = False
TRADING_WALLET_ADDRESS = "0xYourAddressHere"
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"
KALSHI_API_KEY = "your-kalshi-key"
KALSHI_PRIVATE_KEY_PATH = "kalshi_private_key.pem"
AUTO_LOAD_PLAYBOOKS = ["mvp_arb", "chiefs_value"]
"""


# ============================================================================
# ✅ VALIDATION
# ============================================================================

# The system will validate your configuration on startup
# Check logs for any warnings or errors

# Common issues:
# - Wallet address format (must start with 0x, 42 chars)
# - Private key format (must start with 0x, 66 chars)
# - File paths (kalshi_private_key.pem must exist)
# - API keys (check format and validity)


# ============================================================================
# 🚨 SECURITY REMINDERS
# ============================================================================

# ⚠️  NEVER commit config.py to git (it's in .gitignore)
# ⚠️  NEVER share your private key
# ⚠️  NEVER screenshot or email this file
# ⚠️  Use a dedicated trading wallet
# ⚠️  Only fund with what you can afford to lose
# ⚠️  Start with paper trading mode
# ⚠️  Test with small amounts first
# ⚠️  Keep backups of private keys offline


# ============================================================================
# 📚 DOCUMENTATION REFERENCES
# ============================================================================

# README.md - Main overview
# QUICK_START.md - Setup guide
# KALSHI_INTEGRATION.md - Kalshi API guide
# POLYMARKET_BUILDER_GUIDE.md - Builder Relayer guide
# PLAYBOOKS_GUIDE.md - Playbooks documentation
# FEATURES.md - Complete feature list

