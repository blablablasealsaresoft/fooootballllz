# 🚀 APOLLO EDGE - QUICK START GUIDE

## ⚡ 60-Second Setup

```bash
# 1. Install minimum dependencies
pip install requests aiohttp websocket-client

# 2. Create your config file
cp config_template.py config.py

# 3. Edit config.py - add your wallet (or leave for paper trading)

# 4. Launch!
python launch.py
```

---

## 🎯 WHAT IT DOES

Apollo Edge is a **BlackRock-tier NFL betting intelligence system** that:

### 🐋 Whale Detection & Auto-Sniping
- **Real-time monitoring** of Polymarket for large positions ($10K+)
- **Auto-detection** of whale trades with sub-second alerts
- **Auto-execution** follows 10% of whale position size
- **5-hop trace** tracks funding sources back through blockchain
- **Cluster analysis** identifies coordinated wallet groups

### 💰 Arbitrage Scanner
- **Cross-platform** spread detection (Polymarket vs Kalshi)
- **Minimum 2% spread** threshold for profitable trades
- **Liquidity analysis** calculates max safe position size
- **Real-time alerts** when opportunities emerge

### 🏈 Full NFL Props Coverage
- **Super Bowl Champion** - All 32 teams
- **Conference Champions** - AFC/NFC
- **MVP Awards** - Regular season, playoffs, Super Bowl
- **Player Props** - Passing yards, TDs, rushing, receiving
- **Game Props** - Spreads, totals, moneylines
- **Division Winners** - All 8 divisions
- **Super Bowl Props** - First TD, halftime score, Gatorade color, etc.

### 📊 Risk Management
- **Stop-loss**: 15% (configurable)
- **Take-profit**: 50% (configurable)  
- **Position limits**: Max $5K per trade (configurable)
- **Daily limits**: Max 20 snipes per day
- **Auto-exit**: Closes losing positions automatically

---

## 🎮 COMMAND REFERENCE

### Interactive Menu (Recommended for Beginners)
```bash
python launch.py
```
Then select from menu:
- **[1]** 🐋 Find Whales - Scan for large positions
- **[2]** ⚡ Whale Sniper - Auto-follow whale trades
- **[3]** 📊 Cluster Analysis - 5-hop wallet trace
- **[4]** 💰 Arbitrage Scanner - Cross-platform opportunities
- **[5]** 🏈 NFL Props - Full market coverage
- **[6]** 🚀 Full System - Everything combined

### Direct Commands (For Advanced Users)
```bash
# Find current whale positions
python launch.py --whales

# Active auto-sniping (follows whales automatically)
python launch.py --snipe

# Passive monitoring (watch only, no trades)
python launch.py --monitor

# Arbitrage opportunities
python launch.py --arb

# Scan all NFL props
python launch.py --props

# Full system (all modules)
python launch.py --full

# Analyze specific wallet
python launch.py --wallet 0x1234567890abcdef...

# Cluster analysis
python launch.py --clusters
```

### Individual Module Commands
```bash
# Whale detection only
python whale_sniper.py --mode=monitor

# Active sniping
python whale_sniper.py --mode=snipe

# Find specific whale
python whale_finder.py 0x1234567890abcdef...

# NFL props scan
python nfl_props_scanner.py

# Full trading system
python apollo_edge.py --mode=monitor
```

---

## 🔑 WALLET SETUP (REQUIRED FOR TRADING)

### Step 1: Get Your Wallet Ready
You need a **Polygon wallet** with:
- ✅ Your **wallet address** (starts with `0x`, 42 characters)
- ✅ Your **private key** (starts with `0x`, 66 characters total)
- ✅ **USDC on Polygon** for trading

**Where to get:**
- MetaMask, Rainbow, Rabby, or any Polygon-compatible wallet
- Bridge USDC to Polygon via [Polymarket's bridge](https://polymarket.com/wallet)

### Step 2: Configure Your Wallet
```bash
# Create config file
cp config_template.py config.py

# Edit config.py with your editor
nano config.py   # or: code config.py, vim config.py, notepad config.py
```

Find these lines and fill in:
```python
# YOUR WALLET GOES HERE
TRADING_WALLET_ADDRESS = "0xYourWalletAddressHere"
TRADING_WALLET_PRIVATE_KEY = "0xYourPrivateKeyHere"

# For testing (no real money):
PAPER_TRADING_MODE = True

# For live trading (REAL MONEY):
PAPER_TRADING_MODE = False
```

### Step 3: Security Checklist
- ✅ Never share your private key
- ✅ Never commit `config.py` to git (already in .gitignore)
- ✅ Use a dedicated trading wallet (don't use your main wallet)
- ✅ Only fund with what you can afford to lose
- ✅ Start with paper trading mode first

---

## 🔄 TRADING FLOW

### Passive Monitoring (Safe)
```bash
python launch.py --monitor
```
- ✅ Watches whale activity in real-time
- ✅ Shows alerts when big trades happen
- ✅ No trades executed
- ✅ No wallet needed

### Paper Trading (Practice)
```bash
# In config.py, set:
PAPER_TRADING_MODE = True

# Then run:
python launch.py --snipe
```
- ✅ Simulates real trades
- ✅ No real money used
- ✅ Good for testing strategy
- ✅ Wallet address needed (but no actual trading)

### Live Trading (Real Money)
```bash
# In config.py, set:
PAPER_TRADING_MODE = False

# Then run:
python launch.py --snipe
```
- ⚠️ **REAL TRADES** with your wallet
- ⚠️ **REAL MONEY** at risk
- ⚠️ Requires wallet + private key + USDC balance
- ⚠️ Start small to test

---

## 📈 EXAMPLE SESSION

```bash
$ python launch.py --snipe

╔═══════════════════════════════════════════════════════════════════════════════╗
║                          WHALE SNIPER - Active Mode                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

[+] Config loaded from config.py
[*] Wallet: 0x742d35Cc... (Paper Trading Mode)
[*] Min whale size: $10,000
[*] Snipe threshold: $25,000
[*] Follow percentage: 10%
[*] Poll interval: 500ms

🚀 Whale Sniper starting...

[11:23:45] 🐋 WHALE ALERT: $32,500 BUY (confidence: 85%)
           Wallet: 0x8f9a2b3c...
           Market: Chiefs win Super Bowl
           ⚡ SNIPEABLE - Creating order...

[11:23:45] ⚡ EXECUTING SNIPE: snipe_whale_8f9a... - $3,250
[11:23:46] 📝 PAPER TRADE: Would buy $3,250 @ 0.4250
[11:23:46] ✅ SNIPE FILLED: snipe_whale_8f9a... @ 0.4261

[11:24:12] 🐋 WHALE ALERT: $15,000 BUY (confidence: 72%)
           (Below snipe threshold, monitoring only)

[11:25:33] 📊 Position pos_snipe_whale_8f9a...: profit_taken @ +52.3%
           ✅ Take profit triggered!

Statistics:
- Runtime: 2m 48s
- Whales detected: 8
- Snipeable alerts: 2
- Snipes executed: 2
- Fill rate: 100%
- Active positions: 0
- Total P&L: +$1,698 (+52.2%)
```

---

## ⚙️ KEY CONFIGURATION OPTIONS

Open `config.py` to customize:

### Detection Settings
```python
MIN_WHALE_SIZE_USD = 10000        # Minimum to track
SNIPE_THRESHOLD_USD = 25000       # Minimum to auto-trade
MIN_CONFIDENCE_SCORE = 70         # 0-100 confidence filter
```

### Position Sizing
```python
FOLLOW_PERCENTAGE = 0.10          # Follow 10% of whale size
MAX_POSITION_SIZE_USD = 5000      # Max per trade
MAX_TRADING_CAPITAL = 10000       # Max total capital deployed
```

### Risk Management
```python
STOP_LOSS_PCT = 15.0              # Exit if down 15%
TAKE_PROFIT_PCT = 50.0            # Exit if up 50%
MAX_DAILY_SNIPES = 20             # Max trades per day
MAX_DAILY_LOSS_USD = 2000         # Stop if lose $2K in a day
```

### Execution
```python
MAX_SLIPPAGE_PCT = 1.0            # Max acceptable slippage
POLL_INTERVAL_MS = 500            # How often to check (ms)
```

---

## 🔍 FEATURES BREAKDOWN

### 1. Whale Detection Engine
**File:** `whale_sniper.py`

Monitors Polymarket's CTF Exchange for large trades:
- Scans recent transactions every 500ms
- Filters by minimum size ($10K+)
- Calculates confidence score (50-100)
- Identifies known whales vs new wallets
- Tracks CEX deposit sources

**Confidence Factors:**
- **Size**: Larger trades = higher confidence
- **History**: Repeat traders get boost
- **Win rate**: Past success increases score
- **Source**: CEX sources get penalty (noise)

### 2. 5-Hop Cluster Analysis
**File:** `polymarket_whale_hunter_v2.py`

Traces wallet funding backwards through blockchain:
- **Hop 1**: Direct deposits to whale wallet
- **Hop 2**: Where those deposits came from
- **Hop 3-5**: Continue tracing backwards
- **Identifies**: Binance, Coinbase, OKX, bridges
- **Clusters**: Groups wallets with same funding source

**Example Use Case:**
Théo's network (11 coordinated wallets) would be detected as they all trace back to same source.

### 3. Arbitrage Scanner
**File:** `apollo_edge.py` (ArbitrageScanner class)

Compares prices across platforms:
- **Polymarket** - Get live orderbook prices
- **Kalshi** - Get bid/ask spreads
- **Match markets** - Find same event on both
- **Calculate spread** - Buy low, sell high
- **Filter by minimum** - Only show 2%+ spreads

### 4. NFL Props Scanner
**File:** `nfl_props_scanner.py`

Comprehensive NFL market coverage:
- **Championship Markets**: Super Bowl, AFC/NFC
- **Player Props**: Yards, TDs, receptions
- **Game Props**: Spreads, totals, moneylines
- **Division Winners**: All 8 divisions
- **Super Bowl Props**: First TD, halftime, etc.

### 5. Risk Management
Built into all modules:
- **Stop-loss**: Auto-exit at -15%
- **Take-profit**: Auto-exit at +50%
- **Position limits**: Max $5K per trade
- **Daily limits**: Max 20 trades/day
- **Capital limits**: Max $10K deployed
- **Time limits**: Auto-exit after 7 days

---

## 🛟 TROUBLESHOOTING

### "config.py not found"
```bash
cp config_template.py config.py
```

### "No trading wallet configured"
Edit `config.py` and add your wallet address + private key

### "API rate limit exceeded"
The free Etherscan V2 key allows 5 calls/sec. Wait a moment and retry.

### "Module not found"
```bash
pip install -r requirements.txt
```

### "WebSocket connection failed"
Check your internet connection. The system will auto-reconnect.

### Trades not executing
1. Check `PAPER_TRADING_MODE` in config.py
2. Verify wallet has USDC balance on Polygon
3. Check if `MIN_CONFIDENCE_SCORE` is too high
4. Verify `SNIPE_THRESHOLD_USD` threshold

---

## 📚 ADDITIONAL RESOURCES

- **Full Documentation**: `APOLLO_EDGE_README.md`
- **Setup Guide**: `SETUP_GUIDE.md`
- **Config Template**: `config_template.py`

---

## 🎯 RECOMMENDED WORKFLOW

1. **Start with monitoring** (no wallet needed):
   ```bash
   python launch.py --monitor
   ```

2. **Add wallet and try paper trading**:
   ```bash
   # Edit config.py, set PAPER_TRADING_MODE = True
   python launch.py --snipe
   ```

3. **When comfortable, go live** (small amount first):
   ```bash
   # Edit config.py, set PAPER_TRADING_MODE = False
   # Set MAX_POSITION_SIZE_USD = 100  (start small!)
   python launch.py --snipe
   ```

4. **Scale up gradually**:
   - Increase position sizes slowly
   - Monitor win rate and P&L
   - Adjust confidence thresholds based on results

---

## ⚠️ DISCLAIMERS

- **Not Financial Advice**: This is educational software
- **Use At Your Own Risk**: You can lose money
- **No Guarantees**: Past performance ≠ future results
- **Test First**: Always use paper trading mode first
- **Start Small**: Don't risk what you can't lose
- **Secure Your Keys**: Never share private keys

---

## 🚀 YOU'RE READY!

```bash
python launch.py
```

Happy trading! 🎯

