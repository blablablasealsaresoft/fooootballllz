# 🚀 APOLLO EDGE - NFL Betting Intelligence System

**BlackRock-Tier Trading Infrastructure for NFL Prediction Markets**

---

## ⚡ QUICK START

```bash
# Install (just requests needed for basic usage)
pip install requests aiohttp websocket-client

# Launch interactive menu
python launch.py

# Or run specific modules:
python launch.py --whales      # Find whale positions
python launch.py --snipe       # Active sniping mode  
python launch.py --arb         # Arbitrage scanner
python launch.py --props       # NFL props coverage
python launch.py --full        # Everything combined
```

---

## 🎯 SYSTEM CAPABILITIES

| Module | Purpose |
|--------|---------|
| **Whale Finder** | Detect large Polymarket positions ($10K+) |
| **Whale Sniper** | Real-time detection + auto-follow trades |
| **Cluster Analyzer** | 5-hop wallet trace to find coordinated betting |
| **Arbitrage Scanner** | Cross-platform spread detection |
| **NFL Props Scanner** | Full market coverage across all platforms |
| **Apollo Edge** | Unified system combining all modules |

---

## 🔑 YOUR API KEY (ALREADY EMBEDDED)

```
Etherscan V2: I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ
```

Works for 60+ chains: Polygon (Polymarket), Ethereum, Arbitrum, Base, etc.

---

## 📦 FILES INCLUDED

```
launch.py                    # Unified launcher (start here)
apollo_edge.py              # Full trading system
whale_finder.py             # Simple whale detection
whale_sniper.py             # Real-time sniping engine
nfl_props_scanner.py        # Full props market scanner
polymarket_whale_hunter_v2.py # Advanced cluster analysis
solana_bridge_tracer.py     # Cross-chain funding trace
```

---

## 🐋 WHALE DETECTION

### Find Active Whales
```bash
python whale_finder.py
```

Output:
```
🐋 WHALE: 0x1234567890ab... = $156,234.50

TRACING: 0x1234567890abcdef...
[HOP 1] → 0x1234... (EOA) - Incoming: $156,234.50
[HOP 2] → 0x28c6... (Binance 14)
         [!] CEX FOUND: Binance 14

SUMMARY:
  Risk Score: 35/100
  Flags: ['HIGH_BALANCE', 'CEX_FUNDED: Binance 14']
```

### Analyze Specific Wallet
```bash
python whale_finder.py 0xSuspiciousWalletAddress
```

---

## ⚡ WHALE SNIPING

### Passive Monitoring (No Trades)
```bash
python whale_sniper.py --mode=monitor
```

Real-time alerts:
```
🐋 [14:32:15] $45,000 BUY
   Wallet: 0x1234567890ab...
   Confidence: 85%
   ⚡ SNIPEABLE!
```

### Active Sniping (Auto-Trade)
```bash
python whale_sniper.py --mode=snipe
```

⚠️ **WARNING**: This will execute real trades automatically!

Configuration (in whale_sniper.py):
```python
MIN_WHALE_SIZE_USD = 10000      # Track whales > $10K
SNIPE_THRESHOLD_USD = 25000     # Auto-snipe > $25K
FOLLOW_PERCENTAGE = 0.10        # Follow 10% of whale
MAX_FOLLOW_SIZE_USD = 10000     # Max $10K per snipe
STOP_LOSS_PCT = 15.0            # 15% stop loss
TAKE_PROFIT_PCT = 50.0          # 50% take profit
```

---

## 💰 ARBITRAGE SCANNER

```bash
python launch.py --arb
```

Finds cross-platform spreads:
```
ARBITRAGE OPPORTUNITY
  Market: Super Bowl Champion 2026
  Outcome: Denver Broncos
  Polymarket: 11.2%
  Kalshi: 14.5%
  Spread: 3.3%
  Action: BUY on Polymarket, SELL on Kalshi
```

---

## 🏈 NFL PROPS COVERAGE

```bash
python nfl_props_scanner.py
```

Scans:
- **Championship**: Super Bowl, AFC/NFC Champions
- **MVP Awards**: NFL MVP, Super Bowl MVP
- **Player Props**: Passing yards, TDs, rushing, receiving
- **Game Props**: Spreads, totals, moneylines
- **Division Winners**: All 8 divisions
- **Super Bowl Props**: First TD, halftime, etc.

Platforms:
- Polymarket
- Kalshi
- ESPN/Sportsbooks (for comparison)

---

## 📊 CLUSTER ANALYSIS

### Find Wallet Clusters
```bash
python polymarket_whale_hunter_v2.py --trace-wallet 0xAddress
```

Identifies:
- **Common Funding Source**: Multiple wallets from same origin
- **Timing Correlation**: Deposits within 1 hour
- **CEX Origins**: Binance, Coinbase, OKX hot wallets
- **Bridge Deposits**: Wormhole, Polygon Bridge

### The Théo Pattern
The system looks for patterns like the famous election whale:
- 11 wallets controlled by single entity
- $30M+ combined position
- $85M profit realized

---

## 🚀 FULL SYSTEM (APOLLO EDGE)

```bash
python apollo_edge.py --mode=monitor
```

Runs all modules simultaneously:
1. Real-time whale detection
2. Arbitrage scanning
3. Signal generation
4. Auto-execution (if enabled)
5. Position management
6. Risk monitoring

---

## ⚙️ CONFIGURATION

### Whale Detection Thresholds
```python
MIN_WHALE_SIZE_USD = 10000      # Minimum to track
SNIPE_THRESHOLD_USD = 25000     # Minimum to auto-snipe
WHALE_ALERT_THRESHOLD_USD = 25000  # Alert threshold
```

### Execution Settings
```python
MAX_SLIPPAGE_PCT = 1.0          # Max acceptable slippage
EXECUTION_TIMEOUT_MS = 5000     # 5 second timeout
RETRY_ATTEMPTS = 3              # Retry failed orders
```

### Risk Management
```python
MAX_DAILY_SNIPES = 20           # Daily trade limit
MAX_POSITION_SIZE_USD = 50000   # Max single position
STOP_LOSS_PCT = 15.0            # Stop loss percentage
TAKE_PROFIT_PCT = 50.0          # Take profit percentage
MAX_POSITION_PCT = 20           # Max % of portfolio
```

---

## 🎯 SIGNAL TYPES

| Signal | Source | Strength | Auto-Execute |
|--------|--------|----------|--------------|
| `whale_follow` | Large position detected | 50-100 | If > 70 |
| `whale_snipe` | Real-time whale activity | 90 | Immediate |
| `arbitrage` | Cross-platform spread | Based on spread | If > 2% |
| `cluster` | Coordinated wallet activity | Based on size | Manual |
| `momentum` | Price/volume divergence | 40-80 | Manual |

---

## 📡 KNOWN ADDRESSES

### Polymarket Contracts (Polygon)
```
CTF Exchange:        0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E
Neg Risk Exchange:   0xC5d563A36AE78145C45a50134d48A1215220f80a
```

### CEX Hot Wallets (Polygon)
```
Binance 14:    0x28c6c06298d514db089934071355e5743bf21d60
Coinbase 4:    0x56eddb7aa87536c09ccc2793473599fd21a8b17f
OKX:           0x5f65f7b609678448494de4c87521cdf6cef1e932
Bybit:         0x3c783c21a0383057d128bae431894a5c19f9cf06
```

### Bridge Contracts
```
Polygon Bridge:  0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf
Wormhole:        0x5a58505a96D1dbf8dF91cB21B54419FC36e93fdE
```

---

## 📈 WORKFLOW

### Manual Trading
1. Run `python launch.py --whales` to find whales
2. Identify interesting positions
3. Run `python whale_finder.py 0xWallet` for deep analysis
4. Check cluster patterns
5. Make manual trading decision

### Semi-Automated
1. Run `python whale_sniper.py --mode=monitor`
2. Watch for alerts
3. Manually approve snipes
4. System executes approved trades

### Fully Automated
1. Run `python whale_sniper.py --mode=snipe`
2. System auto-executes on qualifying signals
3. Positions managed with stop-loss/take-profit
4. Monitor via status output

---

## ⚠️ RISK WARNINGS

1. **This is experimental software** - Use at your own risk
2. **Prediction markets can be volatile** - Positions can go to zero
3. **Whale following is not guaranteed** - Whales can be wrong
4. **Arbitrage windows close fast** - Execution speed matters
5. **API rate limits apply** - 5 calls/sec for Etherscan free tier

---

## 🔧 TROUBLESHOOTING

### Rate Limits
```
[!] API: Max rate limit reached
```
Solution: Wait a few seconds, scripts have built-in delays

### Network Errors
```
requests.exceptions.ConnectionError
```
Solution: Check internet connection, retry

### Missing Modules
```
ModuleNotFoundError: No module named 'aiohttp'
```
Solution: `pip install aiohttp websocket-client`

---

## 📊 OUTPUT FILES

| File | Contents |
|------|----------|
| `whale_report.json` | Whale detection results |
| `nfl_props_data.json` | All NFL props data |
| `apollo_edge.log` | System logs |

---

## 🚀 RECOMMENDED WORKFLOW

### For Super Bowl Betting:
1. **Daily**: Run props scanner to get market overview
2. **Hourly**: Monitor whale activity for signals
3. **Real-time**: Sniper on for large position detection
4. **Weekly**: Cluster analysis to find coordinated betting

### For Arbitrage:
1. Run arbitrage scanner continuously
2. Alert on spreads > 2%
3. Execute quickly (spreads close fast)
4. Track fill rates and adjust

---

**Good luck! 🏈🐋💰**
