"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    APOLLO EDGE - PRODUCTION CONFIGURATION                     ║
║                                                                               ║
║  🚀 Ready for Trading with Polymarket Builder Relayer (Gasless Trading)      ║
║                                                                               ║
║  ⚠️  SECURITY WARNING: This file contains sensitive credentials!              ║
║      - NEVER commit this file to git (already in .gitignore)                 ║
║      - NEVER share this file with anyone                                      ║
║      - Keep secure backups of private keys offline                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

STATUS: 
✅ API Keys configured
✅ Wallet address set
✅ Builder Relayer enabled (gasless trading!)
📝 ADD: Your private key below (line 40)

SETUP: See POLYMARKET_BUILDER_GUIDE.md for full details
"""

# ============================================================================
# 🔑 API KEYS - ALL CONFIGURED
# ============================================================================

# Etherscan V2 API Key (embedded - works for 60+ chains)
ETHERSCAN_API_KEY = "I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ"

# TheOddsAPI - Your key for sportsbook data (50+ books)
# Free tier: 500 requests/month
ODDS_API_KEY = "31c44bdb909ce897b097756c9bb52eec"


# ============================================================================
# 💰 YOUR TRADING WALLET - POLYGON NETWORK
# ============================================================================

# Your main Polygon wallet address
TRADING_WALLET_ADDRESS = "0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc"

# 🔑 YOUR PRIVATE KEY - ADD THIS FOR LIVE TRADING
# Format: "0x" followed by 64 hexadecimal characters
# ⚠️  CRITICAL: Never share this! Back it up securely!
TRADING_WALLET_PRIVATE_KEY = "0xce98b80c2734c5a0da55990d83b960fa126cbc7c8e7496399b10d08fbe530f60"

# How to get your private key:
# MetaMask: Account Details → Export Private Key → Copy
# Other wallets: Check wallet settings for "Export Private Key"


# ============================================================================
# 🏗️ POLYMARKET BUILDER RELAYER - GASLESS TRADING
# ============================================================================

# Enable gasless trading (Relayer pays gas fees for you!)
# True = No MATIC needed, relayer sponsors transactions
# False = You pay gas with MATIC (traditional method)
USE_BUILDER_RELAYER = True  # ✅ RECOMMENDED

# Relayer API endpoint
POLYMARKET_RELAYER_URL = "https://relayer.polymarket.com"

# Wallet type for gasless trading
# "PROXY" = Simple proxy contract (RECOMMENDED for individuals)
# "SAFE" = Gnosis Safe multisig (for institutions/teams)
POLYMARKET_WALLET_TYPE = "PROXY"

# Your proxy wallet address (auto-generated on first use)
# System will fill this in after deploying your proxy
# Leave empty initially - system handles deployment
POLYMARKET_PROXY_ADDRESS = ""

# Advanced: Custom relayer config (usually not needed)
RELAYER_GAS_LIMIT = 500000
RELAYER_MAX_FEE_PER_GAS = "auto"


# ============================================================================
# 🔐 POLYMARKET API CREDENTIALS (Optional - Higher Rate Limits)
# ============================================================================
# Get these from: https://docs.polymarket.com
# Only needed if you want higher API rate limits
# Not required for trading - Builder Relayer works without these

POLYMARKET_API_KEY = ""
POLYMARKET_API_SECRET = ""
POLYMARKET_API_PASSPHRASE = ""

# If you get these, add them above
# They provide: Faster market data, higher rate limits, priority access


# ============================================================================
# 💵 FUNDING & CAPITAL MANAGEMENT - AUTO-SCALING MODE
# ============================================================================

# IMPORTANT FOR BUILDER RELAYER:
# You need USDC in TWO places:
# 1. Your main wallet (TRADING_WALLET_ADDRESS) - initial funding
# 2. Your proxy wallet (auto-generated) - transfer USDC there for trading

# ============================================================================
# AUTO-SCALING FEATURE - System adjusts based on your balance!
# ============================================================================

# Enable auto-scaling (adjusts limits based on wallet balance)
ENABLE_AUTO_SCALING = True  # ✅ RECOMMENDED - No manual updates needed!

# Manual capital limit (only used if AUTO_SCALING = False)
MAX_TRADING_CAPITAL = 100  # Starting with $100

# Auto-scaling multipliers (used when AUTO_SCALING = True)
# These adjust based on your actual USDC balance
CAPITAL_USAGE_PCT = 90  # Use 90% of balance (keep 10% reserve)
POSITION_SIZE_PCT = 50  # Each trade = 50% of available capital per position
MAX_POSITIONS_AUTO = 2  # Max positions = balance / position size

# Minimum USDC balance to maintain (safety reserve)
MIN_USDC_RESERVE = 10  # Keep at least $10 reserve always


# ============================================================================
# 🐋 WHALE DETECTION & SNIPING SETTINGS
# ============================================================================

# Minimum whale position size to detect and track
MIN_WHALE_SIZE_USD = 5000  # Track whales trading $5K+ (lowered for $100 capital)

# Minimum whale size to auto-snipe (trigger automatic following)
SNIPE_THRESHOLD_USD = 10000  # Auto-follow whales trading $10K+ (lowered for $100 capital)

# Minimum confidence score to execute trade (0-100)
# Higher = more selective, Lower = more trades
MIN_CONFIDENCE_SCORE = 70  # 70% confidence required

# How much of whale's position to copy
# 0.01 = Follow with 1% of whale's size (conservative for small capital)
# 0.02 = Follow with 2% of whale's size
FOLLOW_PERCENTAGE = 0.01  # 1% follow for $100 capital


# ============================================================================
# ⚡ TRADE EXECUTION SETTINGS
# ============================================================================

# Maximum size per individual trade
MAX_POSITION_SIZE_USD = 50  # Max $50 per trade (with $100 capital, allows 2 positions)

# Maximum slippage tolerance (percentage)
# 1.0 = Accept up to 1% price movement
MAX_SLIPPAGE_PCT = 1.0

# Order type preference
DEFAULT_ORDER_TYPE = "market"  # MARKET = instant fills (best for arbitrage!)

# For limit orders: how far from current price (percentage)
LIMIT_ORDER_OFFSET_PCT = 0.5  # 0.5% better than market


# ============================================================================
# 📊 RISK MANAGEMENT - PROTECT YOUR CAPITAL
# ============================================================================

# Maximum trades per day (prevents overtrading)
MAX_DAILY_SNIPES = 5  # Limited to 5 trades/day with $100 capital

# Maximum concurrent open positions
MAX_CONCURRENT_POSITIONS = 2  # Max 2 positions at once with $100 capital

# Stop loss: close position if down this much (percentage)
STOP_LOSS_PCT = 15.0  # Exit at -15%

# Take profit: close position if up this much (percentage)
TAKE_PROFIT_PCT = 50.0  # Exit at +50%

# Maximum portfolio allocation per position (percentage)
MAX_POSITION_PCT = 20.0  # No more than 20% in single position

# Maximum daily loss before stopping all trading (USD)
MAX_DAILY_LOSS_USD = 30  # Stop if lose $30 in one day (30% of $100 capital)

# Time-based exit: close positions after this many hours
MAX_HOLD_HOURS = 168  # 1 week maximum hold time


# ============================================================================
# 🔔 ALERTS & NOTIFICATIONS (Optional but Recommended)
# ============================================================================

# Telegram Bot Alerts
# Create bot: https://t.me/BotFather
# Get chat ID: https://t.me/userinfobot
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Discord Webhook Alerts
# Server Settings → Integrations → Webhooks → New Webhook
DISCORD_WEBHOOK_URL = ""

# Email Alerts
EMAIL_SMTP_SERVER = ""  # e.g., "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = ""
EMAIL_PASSWORD = ""
EMAIL_TO = ""


# ============================================================================
# 🌐 NETWORK & RPC SETTINGS
# ============================================================================

# Polygon RPC endpoints (for blockchain interaction)
# Using public RPCs - consider getting your own for better speed
POLYGON_RPC_URL = "https://polygon-rpc.com"
POLYGON_RPC_BACKUP = "https://rpc-mainnet.matic.quiknode.pro"

# Optional: Use your own RPC for better performance
# Get free RPC: https://www.alchemy.com or https://infura.io
# POLYGON_RPC_URL = "https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"

# Gas settings (only used if not using Builder Relayer)
GAS_PRICE_GWEI = "auto"  # Let system determine gas price
MAX_GAS_PRICE_GWEI = 500  # Max gas willing to pay (safety limit)

# Polling interval: how often to check for new data (milliseconds)
POLL_INTERVAL_MS = 250  # Check every 0.25 seconds (2x faster for arbitrage!)


# ============================================================================
# 🎯 MARKET & WALLET FILTERS
# ============================================================================

# Only trade these specific markets (empty list = trade all markets)
WHITELIST_MARKETS = [
    # "super-bowl-champion",
    # "patriots-win-super-bowl",
    # "chiefs-win-super-bowl",
]

# Never trade these markets
BLACKLIST_MARKETS = [
    # "low-liquidity-market",
]

# Only follow these specific whale wallets (empty = follow all whales)
WHITELIST_WHALES = [
    # "0x1234567890abcdef...",  # Known successful whale
]

# Never follow these wallets (known bots, market makers, etc.)
BLACKLIST_WHALES = [
    # "0xabcdef1234567890...",  # Known market maker
]


# ============================================================================
# 📋 PLAYBOOKS & AUTOMATED STRATEGIES
# ============================================================================

# Enable automatic playbook execution
# Playbooks = pre-configured "if-then" trading strategies
ENABLE_PLAYBOOKS = True

# Where to store playbook data
PLAYBOOKS_FILE = "playbooks.json"

# Auto-load these preset playbooks on startup
# Focused on core features: Whale Detection, Cluster Analysis, Value Detection, NFL Props

AUTO_LOAD_PLAYBOOKS = [
    # WHALE DETECTION & SNIPING
    "whale_snipe_10k",         # Auto-detect whales > $10K
    "whale_snipe_25k",         # Auto-snipe whales > $25K (fast execution)
    
    # 5-HOP CLUSTER ANALYSIS
    "whale_cluster_alert",     # Coordinated wallet clusters (Théo-style)
    "cex_whale_detector",      # CEX-funded whales (Binance, Coinbase, OKX)
    
    # SPORTSBOOK VALUE DETECTION
    "sportsbook_value_mvp",    # MVP value vs 50+ sportsbooks
    "sportsbook_value_superbowl",  # Super Bowl value detection
    
    # NFL PROPS COVERAGE
    "superbowl_momentum",      # Super Bowl rapid movements
    "afc_nfc_champion_value",  # Conference champions
    "player_props_whale",      # Player props whale following
    
    # Optional - uncomment to enable
    # "game_props_value",      # Spreads, totals, moneylines
    # "division_winner_early", # Division winners
    # "superbowl_props_whale", # SB props (first TD, etc.)
    # "patriots_whale_follow", # Team-specific
    # "chiefs_value",          # Team-specific
    # "fade_the_public",       # Contrarian
]

# Auto-load these watchlists on startup
AUTO_LOAD_WATCHLISTS = [
    "top_whales",         # Most successful whale wallets
    "superbowl_markets",  # All Super Bowl markets
    "mvp_candidates",     # MVP contenders
    # "high_volume_markets",
]

# Signal queue settings
SIGNAL_QUEUE_MAX_SIZE = 100  # Max signals to queue
SIGNAL_QUEUE_AUTO_EXECUTE = True  # Auto-execute top signals
SIGNAL_QUEUE_EXECUTION_INTERVAL = 5  # Execute every 5 seconds


# ============================================================================
# 🔧 SYSTEM SETTINGS
# ============================================================================

# Trading mode
# True = Paper trading (simulated, no real money)
# False = Live trading (REAL MONEY, requires private key)
PAPER_TRADING_MODE = True  # ✅ START IN PAPER MODE, SET TO False WHEN READY

# Logging verbosity
DEBUG_MODE = True  # Detailed logs (recommended for testing)

# Log file location
LOG_FILE = "apollo_edge.log"

# Database for trade history (SQLite)
DATABASE_FILE = "apollo_edge.db"

# Auto-restart on errors
AUTO_RESTART = False

# Performance tracking
ENABLE_PERFORMANCE_TRACKING = True
PERFORMANCE_LOG_INTERVAL = 3600  # Log stats every hour


# ============================================================================
# ⚡ SPEED OPTIMIZATIONS - LIVE GAME ARBITRAGE
# ============================================================================

# Enable live game event detection (THE REAL EDGE!)
ENABLE_LIVE_GAME_DETECTION = True

# Live game polling (check ESPN every second for TDs, injuries, etc.)
LIVE_GAME_POLL_MS = 1000  # Check every second

# Minimum edge to execute live arbitrage
LIVE_GAME_MIN_EDGE_PCT = 5.0  # 5% minimum edge

# Event detection timeout (aggressive for speed)
EVENT_DETECTION_TIMEOUT_MS = 2000  # 2 second max

# Execution speed targets
TARGET_EXECUTION_MS = 100  # Sub-100ms execution goal
MAX_TOTAL_LATENCY_MS = 1000  # Event-to-fill in <1 second

# Network optimizations
USE_CONNECTION_POOL = True
CONNECTION_POOL_SIZE = 50
ENABLE_DNS_CACHE = True
DNS_CACHE_TTL_SECONDS = 300

# Aggressive execution (for arbitrage windows)
ARBITRAGE_MODE_RETRIES = 1  # Only 1 retry (speed over reliability)
ARBITRAGE_TIMEOUT_MS = 2000  # 2 second total timeout

# Twitter/X API for fastest updates (optional)
TWITTER_API_KEY = ""  # Add your Twitter API key for sub-1s detection
TWITTER_BEARER_TOKEN = ""

# Premium WebSocket feeds (optional - fastest but paid)
ENABLE_WEBSOCKET_FEEDS = False  # Set True if you have premium feed
WEBSOCKET_FEED_URL = ""


# ============================================================================
# 📊 ADVANCED: BUILDER RELAYER TRANSACTION SETTINGS
# ============================================================================

# Batch multiple transactions together (more efficient)
ENABLE_TRANSACTION_BATCHING = True
MAX_BATCH_SIZE = 5  # Max transactions per batch

# Retry failed transactions
MAX_TRANSACTION_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# Transaction timeout
TRANSACTION_TIMEOUT_SECONDS = 60

# Nonce management for concurrent transactions
ENABLE_NONCE_MANAGER = True


# ============================================================================
# 🎯 TRADING PROFILES (Quick Presets)
# ============================================================================

# Uncomment one profile to use, or customize your own

# ===== CONSERVATIVE PROFILE (Safest) =====
# MIN_WHALE_SIZE_USD = 50000
# SNIPE_THRESHOLD_USD = 100000
# MIN_CONFIDENCE_SCORE = 85
# MAX_POSITION_SIZE_USD = 1000
# FOLLOW_PERCENTAGE = 0.05
# MAX_DAILY_SNIPES = 5
# STOP_LOSS_PCT = 10.0
# TAKE_PROFIT_PCT = 30.0

# ===== BALANCED PROFILE (Default - Currently Active) =====
# Settings already configured above

# ===== AGGRESSIVE PROFILE (More Trades, Higher Risk) =====
# MIN_WHALE_SIZE_USD = 5000
# SNIPE_THRESHOLD_USD = 10000
# MIN_CONFIDENCE_SCORE = 60
# MAX_POSITION_SIZE_USD = 10000
# FOLLOW_PERCENTAGE = 0.20
# MAX_DAILY_SNIPES = 50
# STOP_LOSS_PCT = 20.0
# TAKE_PROFIT_PCT = 100.0


# ============================================================================
# ✅ CONFIGURATION VALIDATION
# ============================================================================

# System will validate these on startup:
# - Wallet address format (0x + 40 hex chars)
# - Private key format (0x + 64 hex chars)
# - API key validity
# - Network connectivity
# - Builder Relayer availability

# Check startup logs for validation results


# ============================================================================
# 📚 QUICK START GUIDE
# ============================================================================

"""
CURRENT STATUS:
===============
✅ API Keys: Configured (Etherscan, TheOddsAPI)
✅ Wallet Address: Set (0x7F4c4646e78Cb88021879C4C5AaaCaD627E9924B)
✅ Builder Relayer: Enabled (gasless trading)
✅ Paper Trading: Active (safe testing mode)

WHAT YOU NEED:
==============
1. 🔑 ADD PRIVATE KEY (line 40 above)
2. 💰 FUND WALLET with USDC on Polygon
3. 📝 OPTIONAL: Add notification webhooks

TESTING:
========
# Step 1: Test in paper mode (no money needed)
python launch.py --monitor

# Step 2: Watch the system work
python launch.py --props

# Step 3: Load strategies
python launch.py --load-playbook patriots_whale_follow

GOING LIVE:
===========
# Step 1: Add your private key above (line 40)

# Step 2: Fund your main wallet with USDC
# Get USDC on Polygon via:
# - Polymarket.com bridge
# - Exchange withdrawal (Polygon network)
# - Polygon bridge from Ethereum

# Step 3: Deploy your proxy wallet (automatic on first trade)
# System will:
# - Deploy proxy contract (one-time, relayer pays gas)
# - Show you proxy address
# - You transfer USDC to proxy for trading

# Step 4: Set paper mode to False
PAPER_TRADING_MODE = False

# Step 5: Start small!
MAX_POSITION_SIZE_USD = 100  # Start with $100 trades
MAX_DAILY_SNIPES = 3         # Limit to 3 trades per day

# Step 6: Launch
python launch.py --snipe

BUILDER RELAYER FLOW:
====================
1. You sign transaction with private key (off-chain)
2. Relayer receives signed message
3. Relayer submits transaction to Polygon
4. Relayer pays gas in MATIC
5. Your trade executes (you only spent USDC, not MATIC!)

BENEFITS:
=========
✅ No MATIC needed in wallet
✅ Faster execution (batched)
✅ Lower costs (optimized gas)
✅ Simpler UX

DOCUMENTATION:
==============
- POLYMARKET_BUILDER_GUIDE.md - Full Builder Relayer guide
- READY_TO_TRADE.md - Step-by-step launch guide
- PLAYBOOKS_GUIDE.md - Strategy documentation
- ALTERNATIVES_TO_KALSHI.md - Why we use sportsbooks

SUPPORT:
========
Check logs if issues: apollo_edge.log
System validates config on startup
All errors logged with solutions
"""


# ============================================================================
# 🚨 SECURITY REMINDERS
# ============================================================================

"""
⚠️  CRITICAL SECURITY RULES:
============================
1. NEVER commit config.py to git (it's in .gitignore)
2. NEVER share your private key with anyone
3. NEVER screenshot or email this file
4. ALWAYS keep backup of private keys offline
5. ALWAYS use a dedicated trading wallet (not your main wallet)
6. ALWAYS start in paper trading mode
7. ALWAYS test with small amounts first ($50-100)
8. ALWAYS monitor your first few trades closely

WHAT TO DO IF COMPROMISED:
==========================
1. Immediately transfer all funds to new wallet
2. Revoke all approvals on compromised wallet
3. Generate new private key
4. Never reuse compromised wallet

BEST PRACTICES:
===============
- Use hardware wallet for storing backup keys
- Use separate wallet for trading (not main holdings)
- Start with small capital ($500-1000)
- Scale up gradually based on performance
- Monitor daily P&L and adjust thresholds
- Review trade logs regularly
"""


# ============================================================================
# 🎉 YOU'RE READY TO LAUNCH!
# ============================================================================

"""
Your configuration is complete and production-ready!

NEXT STEP:
Add your private key on line 40 above, then run:

    python launch.py

Happy trading! 🚀
"""
