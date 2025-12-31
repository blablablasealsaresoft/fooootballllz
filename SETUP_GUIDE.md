# 📁 APOLLO EDGE - Folder Structure & Setup Guide

## 📂 FOLDER ARCHITECTURE

```
apollo-edge/
│
├── 🚀 LAUNCHERS
│   ├── launch.py                    # Main entry point - START HERE
│   └── config.py                    # ⚠️ YOUR CREDENTIALS GO HERE
│
├── 🐋 WHALE DETECTION
│   ├── whale_finder.py              # Simple whale detection
│   ├── whale_sniper.py              # Real-time sniping engine
│   └── polymarket_whale_hunter_v2.py # Advanced cluster analysis
│
├── 📊 MARKET SCANNERS
│   ├── nfl_props_scanner.py         # Full NFL props coverage
│   └── solana_bridge_tracer.py      # Cross-chain funding trace
│
├── 🎯 CORE SYSTEM
│   ├── apollo_edge.py               # Full trading system
│   └── multichain_whale_tracer.py   # Multi-chain analysis
│
├── 📋 DOCUMENTATION
│   ├── APOLLO_EDGE_README.md        # Full documentation
│   ├── README.md                    # Quick start guide
│   └── README_V2.md                 # Etherscan V2 guide
│
├── 📦 DEPENDENCIES
│   └── requirements.txt             # Python packages
│
├── 📈 DATA (auto-generated)
│   ├── whale_report.json            # Whale detection results
│   ├── nfl_props_data.json          # Props market data
│   ├── apollo_edge.log              # System logs
│   └── apollo_edge.db               # Trade history database
│
└── 🔒 SECURITY (add to .gitignore)
    └── config.py                    # Your private keys
```

---

## ⚡ QUICK SETUP (5 MINUTES)

### Step 1: Create Your Folder
```bash
mkdir apollo-edge
cd apollo-edge
```

### Step 2: Download All Files
Copy all the Python files into this folder.

### Step 3: Install Dependencies
```bash
pip install requests aiohttp websocket-client
```

### Step 4: Configure Your Wallet
```bash
# Rename the template
cp config_template.py config.py

# Edit with your credentials
nano config.py
```

### Step 5: Add Your Wallet Details
Open `config.py` and fill in:

```python
# Your Polygon wallet address
TRADING_WALLET_ADDRESS = "0xYourActualWalletAddress"

# Your private key (KEEP SECRET!)
TRADING_WALLET_PRIVATE_KEY = "0xYourPrivateKeyHere"
```

### Step 6: Start Paper Trading First
```bash
# Keep PAPER_TRADING_MODE = True in config.py
python launch.py
```

### Step 7: Go Live
```python
# In config.py, change:
PAPER_TRADING_MODE = False
```

---

## 🔑 WHERE TO INPUT YOUR WALLET

### Location: `config.py` (create from config_template.py)

```python
# ============================================================================
# 💰 YOUR TRADING WALLET - POLYMARKET (POLYGON NETWORK)
# ============================================================================

# Your Polygon wallet address (starts with 0x)
TRADING_WALLET_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc9e7595f5e432"

# Your private key
TRADING_WALLET_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
```

### ⚠️ SECURITY CHECKLIST

- [ ] Never commit `config.py` to git
- [ ] Add `config.py` to `.gitignore`
- [ ] Use a dedicated trading wallet (not your main wallet)
- [ ] Only fund with what you're willing to lose
- [ ] Keep private key backup in secure location
- [ ] Start with `PAPER_TRADING_MODE = True`

---

## 🎮 HOW THE AUTO-TRADING WORKS

### Signal Flow:
```
1. Whale Detector scans Polymarket
         ↓
2. Large position detected ($25K+)
         ↓
3. Signal generated with confidence score
         ↓
4. If confidence > 70%, auto-snipe triggered
         ↓
5. Order submitted using YOUR wallet
         ↓
6. Position tracked with stop-loss/take-profit
```

### Your Wallet's Role:
```
YOUR WALLET (config.py)
    │
    ├── Holds USDC on Polygon
    │
    ├── Signs transactions to Polymarket
    │
    └── Receives profits / absorbs losses
```

---

## 💰 FUNDING YOUR WALLET

### Requirements:
1. **USDC on Polygon** - For trading
2. **MATIC on Polygon** - For gas fees (~$1-5 worth)

### How to Fund:
```
1. Get USDC on any chain (Coinbase, Binance, etc.)
2. Bridge to Polygon using:
   - https://wallet.polygon.technology/bridge
   - https://app.across.to/
   - https://portalbridge.com/
3. Send some MATIC for gas
```

### Recommended Starting Capital:
- **Minimum**: $500 USDC + $5 MATIC
- **Recommended**: $2,000 USDC + $10 MATIC
- **Serious**: $10,000 USDC + $20 MATIC

---

## 🎯 CONFIGURATION QUICK REFERENCE

### Conservative Settings (Recommended to Start):
```python
PAPER_TRADING_MODE = True           # Simulate first!
MIN_WHALE_SIZE_USD = 25000          # Higher threshold
SNIPE_THRESHOLD_USD = 50000         # Only biggest whales
FOLLOW_PERCENTAGE = 0.05            # 5% of whale
MAX_POSITION_SIZE_USD = 1000        # Small positions
MAX_DAILY_SNIPES = 5                # Limited trades
STOP_LOSS_PCT = 10.0                # Tight stop
```

### Aggressive Settings (After Testing):
```python
PAPER_TRADING_MODE = False          # Real trading
MIN_WHALE_SIZE_USD = 10000          # Track more whales
SNIPE_THRESHOLD_USD = 25000         # Snipe medium+ whales
FOLLOW_PERCENTAGE = 0.15            # 15% of whale
MAX_POSITION_SIZE_USD = 5000        # Larger positions
MAX_DAILY_SNIPES = 20               # More trades
STOP_LOSS_PCT = 20.0                # Wider stop
```

---

## 🚀 LAUNCH COMMANDS

```bash
# Interactive menu (recommended)
python launch.py

# Passive monitoring (watch whales, no trades)
python launch.py --monitor

# Active sniping (auto-trades)
python launch.py --snipe

# Whale scanning only
python launch.py --whales

# NFL props scanner
python launch.py --props

# Full system
python launch.py --full

# Analyze specific wallet
python launch.py --wallet 0xSuspiciousAddress
```

---

## 📊 MONITORING YOUR TRADES

### Real-Time Output:
```
🐋 [14:32:15] WHALE DETECTED: $45,000 BUY
   Wallet: 0x1234567890ab...
   Confidence: 85%
   ⚡ SNIPING: $4,500 (10% follow)

✅ [14:32:16] ORDER FILLED @ 0.1234
   Position ID: pos_whale_abc123
   Stop Loss: 0.1050 (-15%)
   Take Profit: 0.1851 (+50%)

📊 [14:45:00] POSITION UPDATE
   Current: 0.1456 (+18%)
   Status: OPEN
```

### Log Files:
- `apollo_edge.log` - All system events
- `whale_report.json` - Detected whales
- `nfl_props_data.json` - Market data

---

## ⚠️ RISK WARNINGS

1. **Start with Paper Trading** - Always test first
2. **Use Dedicated Wallet** - Don't use your main wallet
3. **Fund Conservatively** - Only risk what you can lose
4. **Monitor Actively** - Check positions regularly
5. **Understand the Markets** - Prediction markets can go to zero

---

## 🆘 TROUBLESHOOTING

### "Config not found"
```bash
cp config_template.py config.py
# Then edit config.py with your details
```

### "Insufficient funds"
- Add more USDC to your wallet
- Add MATIC for gas fees

### "Transaction failed"
- Check gas price settings
- Ensure wallet has MATIC for gas
- Try increasing `MAX_GAS_PRICE_GWEI`

### "Rate limited"
- Etherscan free tier: 5 calls/sec
- Built-in delays handle this
- Wait and retry

---

## 📞 FILE-BY-FILE PURPOSE

| File | What It Does | When to Use |
|------|--------------|-------------|
| `launch.py` | Interactive menu | Always start here |
| `config.py` | Your credentials | Set up once |
| `whale_sniper.py` | Auto-trading engine | For live sniping |
| `whale_finder.py` | Manual whale search | Research mode |
| `apollo_edge.py` | Full combined system | Production |
| `nfl_props_scanner.py` | Market overview | Daily scanning |

---

**Ready to trade? Start with `python launch.py`! 🚀**
