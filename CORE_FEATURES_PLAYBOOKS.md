# 🎯 APOLLO EDGE - CORE FEATURES & PLAYBOOKS

## Your System Is Now Laser-Focused on 5 Core Features

---

## ⚡ 1. WHALE DETECTION & SNIPING

### **3 Playbooks Active**

#### 🐋 **Whale Snipe $10K+**
```python
TRIGGERS WHEN:
- Whale trades > $10,000
- Confidence > 70%
- Action: BUY

EXECUTES:
- Follow with $1,000 (10% of whale size)
- Cooldown: 5 minutes
- Max: 20 trades/day
```

#### ⚡ **Whale Snipe $25K+ (Auto)**
```python
TRIGGERS WHEN:
- Whale trades > $25,000
- Confidence > 75%
- Action: BUY

EXECUTES:
- Follow with $2,500 (10% of whale size)
- FAST EXECUTION MODE (sub-second)
- Cooldown: 3 minutes
- Max: 20 trades/day
```

#### 🏈 **Patriots Whale Follow**
```python
TRIGGERS WHEN:
- Whale trades > $50,000
- Market contains "patriots"
- Action: BUY

EXECUTES:
- Follow with $5,000 (10% of whale size)
- Cooldown: 5 minutes
- Max: 10 trades/day
```

### **What This Does**
- Monitors Polymarket CTF Exchange 24/7
- Detects large positions in real-time (500ms polling)
- Calculates confidence score (based on whale history, size, CEX source)
- Auto-executes follow trades with your risk parameters
- Tracks stop-loss (-15%) and take-profit (+50%)

---

## 📊 2. 5-HOP CLUSTER ANALYSIS

### **3 Playbooks Active**

#### 🕸️ **Coordinated Whale Cluster**
```python
TRIGGERS WHEN:
- 3+ wallets from same cluster trade same market
- Total cluster size > $75,000
- Cluster confidence > 80%

EXECUTES:
- HIGH PRIORITY ALERT
- Follow with $5,000 after 30-second confirmation
- Detects patterns like Théo's 11-wallet coordination
```

#### 🏦 **CEX Whale Tracker**
```python
TRIGGERS WHEN:
- Wallet funded from Binance, Coinbase, or OKX
- Whale trades > $50,000
- Trace back to CEX in ≤3 hops

EXECUTES:
- MEDIUM PRIORITY ALERT
- Follow with $2,500 (5% of whale size)
- Tracks: Binance, Coinbase, OKX, Gate.io, Crypto.com
```

#### 🌉 **Bridge Whale Tracker**
```python
TRIGGERS WHEN:
- Large deposit via Wormhole or Polygon Bridge
- Transfer size > $100,000
- Deposit happened within last hour

EXECUTES:
- HIGH PRIORITY ALERT (no trade, just notify)
- Indicates serious money entering market
```

### **What This Does**
- Traces wallet funding backwards through 5 hops
- Identifies coordinated wallet clusters
- Detects CEX sources (Binance = serious traders)
- Finds bridge activity (large institutional money)
- Maps network graphs of related wallets

---

## 💰 3. SPORTSBOOK VALUE DETECTION

### **2 Playbooks Active**

#### 🏆 **MVP Value vs Sportsbooks**
```python
TRIGGERS WHEN:
- MVP market category
- Sportsbooks show 65%+ probability
- Polymarket shows <55% probability
- Liquidity > $50,000

EXECUTES:
- Buy $2,000 (Polymarket undervalued by 10%+)
- Uses consensus of 50+ sportsbooks via TheOddsAPI
- Markets: DraftKings, FanDuel, BetMGM, Caesars, etc.
```

#### 🏈 **Super Bowl Value Detector**
```python
TRIGGERS WHEN:
- Super Bowl market
- Sportsbooks show 70%+ probability
- Polymarket shows <60% probability
- Volume > $100,000

EXECUTES:
- Buy $3,000 (significant undervalue)
- Cooldown: 10 minutes
- Max: 15 trades
```

### **What This Does**
- Compares Polymarket prices vs 50+ sportsbooks
- Identifies mispriced markets (10%+ discrepancy)
- Uses TheOddsAPI for real-time odds
- Trades only on Polymarket (no multi-platform complexity)
- Sportsbooks = price signal, not arb partner

**Note:** Replaced Kalshi arbitrage (too complex) with simpler, more effective sportsbook value detection!

---

## 🏈 4. FULL NFL PROPS COVERAGE

### **6 Playbooks Active**

#### 🏆 **Super Bowl Momentum**
```python
Markets: Super Bowl Champion
Triggers: 5% price change in 5 minutes + $50K volume
Action: Buy $1,500 (follow momentum)
```

#### 🎯 **Conference Champion Value**
```python
Markets: AFC/NFC Champions
Triggers: $20K+ whale + sportsbook confirmation
Action: Buy $2,000
```

#### 📊 **Player Props Whale**
```python
Markets: Passing yards, rushing yards, receiving yards, TDs
Triggers: $15K+ whale + 75% confidence
Action: Buy $1,500 (10% follow)
```

#### 🎲 **Game Props Value**
```python
Markets: Spreads, totals, moneylines
Triggers: 10%+ sportsbook edge + $25K liquidity
Action: Buy $1,000
```

#### 🏆 **Division Winner Early Bird**
```python
Markets: Division winners (8 divisions)
Triggers: $30K whale + sportsbook consensus + undervalued
Action: Buy $2,500
```

#### 🎉 **Super Bowl Props Whale**
```python
Markets: First TD, halftime score, Gatorade color, etc.
Triggers: $10K+ whale on SB prop markets
Action: Buy $1,000 (10% follow)
```

### **Full Coverage**
- ✅ Super Bowl Champion (32 teams)
- ✅ AFC/NFC Champions
- ✅ MVP Awards (multiple categories)
- ✅ Player Props (yards, TDs, receptions)
- ✅ Game Props (spreads, totals, moneylines)
- ✅ Division Winners (8 divisions)
- ✅ Super Bowl Props (novelty markets)

---

## 🛡️ 5. RISK MANAGEMENT

### **Built Into Every Playbook**

#### Position Limits
```python
MAX_POSITION_SIZE_USD = 5000      # Max per trade
MAX_DAILY_SNIPES = 20             # Max trades per day
MAX_CONCURRENT_POSITIONS = 10     # Max open at once
MAX_TRADING_CAPITAL = 10000       # Max total deployed
```

#### Auto-Exit Rules
```python
STOP_LOSS_PCT = 15.0    # Exit at -15%
TAKE_PROFIT_PCT = 50.0  # Exit at +50%
MAX_HOLD_HOURS = 168    # Exit after 7 days max
```

#### Daily Limits
```python
MAX_DAILY_LOSS_USD = 2000  # Stop trading if lose $2K/day
```

#### Cooldowns
```
Prevent overtrading:
- Whale snipes: 3-5 min cooldown
- Value plays: 5-10 min cooldown
- Cluster alerts: 10 min cooldown
```

---

## 🎮 HOW TO USE

### **View All Playbooks**
```bash
python launch.py --playbooks
```

### **Your Current Config**
```python
# 9 Playbooks auto-loaded on startup:
AUTO_LOAD_PLAYBOOKS = [
    "whale_snipe_10k",           # ✅ Loaded
    "whale_snipe_25k",           # ✅ Loaded
    "whale_cluster_alert",       # ✅ Loaded
    "cex_whale_detector",        # ✅ Loaded
    "sportsbook_value_mvp",      # ✅ Loaded
    "sportsbook_value_superbowl",# ✅ Loaded
    "superbowl_momentum",        # ✅ Loaded
    "afc_nfc_champion_value",    # ✅ Loaded
    "player_props_whale",        # ✅ Loaded
]
```

### **Run Full System**
```bash
python launch.py --full
```

**All 9 playbooks will:**
- Monitor markets 24/7
- Evaluate conditions every 500ms
- Auto-execute when conditions met
- Track performance and P&L
- Respect risk limits

---

## 📊 PLAYBOOK SUMMARY TABLE

| Feature | Playbooks | Focus | Auto-Load |
|---------|-----------|-------|-----------|
| **Whale Detection** | 3 | $10K+, $25K+, Team-specific | ✅ 2 active |
| **Cluster Analysis** | 3 | Coordinated, CEX, Bridge | ✅ 2 active |
| **Value Detection** | 2 | MVP, Super Bowl | ✅ 2 active |
| **NFL Props** | 6 | All categories covered | ✅ 3 active |
| **Risk Management** | Built-in | All playbooks | ✅ Always on |

**Total: 14 specialized playbooks, 9 auto-loaded**

---

## 🎯 WHAT MAKES THIS POWERFUL

### **1. Laser-Focused**
Every playbook targets one of your 5 core features. No bloat, no distractions.

### **2. Proven Strategies**
- Whale following = proven edge (smart money)
- Cluster detection = institutional patterns
- Sportsbook comparison = market efficiency
- NFL props = comprehensive coverage
- Risk management = capital preservation

### **3. Automated Execution**
```
Whale trades $30K → Your playbook detects → Auto-follows with $3K → Position tracked → Auto-exit at +50%
```

### **4. Real Edge**
- Sub-second execution beats manual traders
- 5-hop trace reveals coordination others miss
- 50+ sportsbook consensus finds true value
- Risk limits prevent catastrophic losses

---

## 🚀 YOUR SYSTEM NOW

### **Core Features Activated**
```
✅ Whale Detection & Sniping (3 playbooks)
✅ 5-Hop Cluster Analysis (3 playbooks)
✅ Sportsbook Value Detection (2 playbooks, not Kalshi!)
✅ Full NFL Props Coverage (6 playbooks)
✅ Risk Management (built into all)
```

### **Status**
```
Paper Trading: ✅ Active (safe testing)
Config: ✅ Loaded
APIs: ✅ Working
Playbooks: ✅ 9 Active
Risk Limits: ✅ Enforced
```

### **Launch**
```bash
python launch.py --full
```

**Your laser-focused trading system is ready!** 🎯

---

## 📚 QUICK REFERENCE

### **Whale Following**
- Detects positions > $10K
- Auto-snipes > $25K
- Sub-second execution
- 10% follow size

### **Cluster Detection**
- 5-hop funding trace
- CEX identification
- Bridge monitoring
- Coordination patterns

### **Value Detection**
- 50+ sportsbooks
- 10%+ mispricing
- MVP & Super Bowl focus
- High-liquidity only

### **NFL Coverage**
- Champion markets
- Player props
- Game props
- Division winners
- Super Bowl props

### **Risk Protection**
- 15% stop-loss
- 50% take-profit
- Daily limits
- Position sizing
- Auto-exit

---

**Your bot is optimized and focused! Time to trade!** 🚀

