# 📋 APOLLO EDGE - PLAYBOOKS & PLAYLISTS GUIDE

## 🎯 What Are Playbooks?

**Playbooks** are pre-configured trading strategies that automatically execute when specific conditions are met. Think of them as "if-then" rules for trading.

**Example:** "If a whale buys Patriots > $50K, then automatically follow with $5K"

---

## 🎮 TYPES OF PLAYLISTS

### 1. 📋 Playbooks (Conditional Strategies)
Pre-configured rules that auto-execute trades based on conditions.

**Structure:**
```
IF [conditions are met]
THEN [execute actions]
```

### 2. 👁️ Watchlists (Curated Monitoring)
Lists of wallets, markets, or tokens to monitor for activity.

**Use Cases:**
- Track top 10 whale wallets
- Monitor all Super Bowl markets
- Watch MVP candidates
- Follow high-volume markets

### 3. 📊 Signal Queue (Prioritized Opportunities)
Ranked list of trading signals sorted by score.

**Scoring Factors:**
- Priority (0-100)
- Confidence (0-100)
- Expected Edge (profit %)

### 4. 🔄 Arbitrage Routes (Execution Paths)
Pre-defined paths for cross-platform arbitrage.

**Example:**
```
Buy on Polymarket → Sell on Kalshi
```

---

## 📦 PRE-BUILT PLAYBOOKS

### 1. Patriots Whale Follow
**ID:** `patriots_whale_follow`

**What it does:**
- Watches for whales buying Patriots markets
- Auto-follows with 10% of whale size (max $5K)
- Only triggers on positions > $50K

**Conditions:**
```python
whale_size > $50,000
market_name contains "patriots"
whale_action == "buy"
```

**Actions:**
```python
buy(size=$5,000, follow_pct=0.10)
```

**Settings:**
- Cooldown: 5 minutes
- Max executions: 10

---

### 2. Chiefs Value Play
**ID:** `chiefs_value`

**What it does:**
- Buys Chiefs when odds drop below 30%
- Only on high-volume markets ($100K+)
- Contrarian value play

**Conditions:**
```python
market_name contains "chiefs"
price < 0.30
volume > $100,000
```

**Actions:**
```python
buy(size=$2,000, limit_price=0.30)
```

**Settings:**
- Cooldown: 1 hour
- Max executions: 3

---

### 3. MVP Arbitrage
**ID:** `mvp_arb`

**What it does:**
- Auto-executes MVP arbitrage opportunities
- Minimum 3% spread required
- High-liquidity markets only

**Conditions:**
```python
market_category == "mvp"
spread_pct > 3.0%
liquidity > $50,000
```

**Actions:**
```python
buy(platform="polymarket")
sell(platform="kalshi")
```

**Settings:**
- Cooldown: 1 minute
- Max executions: 50

---

### 4. Whale Cluster Alert
**ID:** `whale_cluster_alert`

**What it does:**
- Detects coordinated whale activity
- Alerts when 3+ cluster wallets buy same market
- Auto-follows after 30-second confirmation

**Conditions:**
```python
cluster_wallets_active >= 3
total_cluster_size > $75,000
```

**Actions:**
```python
alert(priority="high")
buy(size=$3,000, wait_seconds=30)
```

**Settings:**
- Cooldown: 10 minutes
- Max executions: 20

---

### 5. Super Bowl Momentum
**ID:** `superbowl_momentum`

**What it does:**
- Follows rapid price movements on SB markets
- Triggers on 5% price change in 5 minutes
- Momentum trading strategy

**Conditions:**
```python
market_name contains "super bowl"
price_change_5m > 5%
volume_5m > $50,000
```

**Actions:**
```python
buy(size=$1,000, follow_momentum=True)
```

**Settings:**
- Cooldown: 5 minutes
- Max executions: 15

---

### 6. Fade The Public
**ID:** `fade_the_public`

**What it does:**
- Contrarian strategy: sells when public heavily buys
- Only when whales aren't participating
- Targets overpriced markets

**Conditions:**
```python
public_buy_volume > 80%
price > 0.70
whale_participation < 20%
```

**Actions:**
```python
sell(size=$1,500)
```

**Settings:**
- Cooldown: 30 minutes
- Max executions: 10

---

## 🚀 QUICK START

### View All Playbooks
```bash
python launch.py --playbooks
```

Or from interactive menu:
```bash
python launch.py
# Select [7] Playbooks → [a] List Playbooks
```

### Load a Preset Playbook
```bash
python launch.py --load-playbook patriots_whale_follow
```

Or:
```bash
python playbooks.py --load-preset patriots_whale_follow
```

### View Watchlists
```bash
python launch.py --watchlists
```

### View Signal Queue
```bash
python launch.py --signals
```

---

## 📝 CREATING CUSTOM PLAYBOOKS

### Method 1: Interactive Creator
```bash
python playbooks.py --create
```

### Method 2: Code (Python)
```python
from playbooks import Playbook, Condition, Action, ConditionOperator, ActionType, PlaybookType

# Create custom playbook
playbook = Playbook(
    id="my_custom_strategy",
    name="My Custom Strategy",
    description="Description here",
    playbook_type=PlaybookType.WHALE_FOLLOW,
    conditions=[
        Condition(
            field="whale_size",
            operator=ConditionOperator.GREATER_THAN,
            value=30000
        ),
        Condition(
            field="market_name",
            operator=ConditionOperator.CONTAINS,
            value="ravens"
        )
    ],
    actions=[
        Action(
            action_type=ActionType.BUY,
            params={"size": 2500}
        )
    ],
    cooldown_seconds=300,
    max_executions=20
)

# Add to manager
from playbooks import PlaybookManager
manager = PlaybookManager()
manager.add_playbook(playbook)
```

---

## 👁️ WATCHLISTS

### Pre-Built Watchlists

#### Top 10 Whales
**ID:** `top_whales`
- Tracks most successful whale wallets
- Auto-triggers associated playbooks

#### Super Bowl Markets
**ID:** `superbowl_markets`
- Monitors all SB-related markets
- Keywords: "super bowl", "sb59", "championship"

#### MVP Candidates
**ID:** `mvp_candidates`
- Top MVP contenders
- Players: Mahomes, Allen, Lamar, Purdy, Stroud

#### High Volume Markets
**ID:** `high_volume_markets`
- Markets with > $1M volume
- Dynamically populated

### Load Watchlists
```bash
python playbooks.py --list-watchlists
```

### Adding Items to Watchlist
```python
from playbooks import PlaybookManager

manager = PlaybookManager()
wl = manager.get_watchlist("top_whales")
wl.add("0x1234567890abcdef...")
```

---

## 📊 SIGNAL QUEUE

The signal queue automatically prioritizes trading opportunities by score.

### Score Calculation
```
Score = (Priority × 40%) + (Confidence × 30%) + (Edge × 30%)
```

### View Queue
```bash
python launch.py --signals
```

### Auto-Execution
Enable in `config.py`:
```python
SIGNAL_QUEUE_AUTO_EXECUTE = True
SIGNAL_QUEUE_EXECUTION_INTERVAL = 5  # seconds
```

---

## ⚙️ CONFIGURATION

Add to your `config.py`:

```python
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
]

# Auto-load these watchlists
AUTO_LOAD_WATCHLISTS = [
    "top_whales",
    "superbowl_markets",
    "mvp_candidates",
]

# Signal queue settings
SIGNAL_QUEUE_MAX_SIZE = 100
SIGNAL_QUEUE_AUTO_EXECUTE = True
SIGNAL_QUEUE_EXECUTION_INTERVAL = 5
```

---

## 🔄 INTEGRATION WITH MAIN SYSTEM

Playbooks automatically integrate with:

### Whale Sniper
When whale detected:
1. Check watchlists
2. Evaluate playbooks
3. Add signals to queue
4. Execute if conditions met

### Arbitrage Scanner
When arb found:
1. Check if route exists
2. Evaluate playbook conditions
3. Add to signal queue
4. Auto-execute if enabled

### Apollo Edge (Full System)
```bash
python apollo_edge.py --mode=monitor
```
- Auto-loads playbooks from config
- Evaluates on every scan cycle
- Executes top signals from queue

---

## 📈 PLAYBOOK PERFORMANCE TRACKING

Each playbook tracks:
- **Execution count**
- **Total P&L**
- **Last execution time**
- **Average success rate**

View stats:
```bash
python playbooks.py --list
```

Output:
```
Patriots Whale Follow
  Type: whale_follow
  Executions: 8
  P&L: $3,245.50
  Enabled: ✅
```

---

## 🎯 USE CASES

### Use Case 1: Following a Specific Whale
```python
# Create watchlist for specific whale
watchlist = Watchlist(
    id="whale_0x123",
    name="Whale 0x123...",
    watch_type="wallets",
    items=["0x1234567890abcdef..."]
)

# Create playbook to follow
playbook = Playbook(
    id="follow_whale_0x123",
    name="Follow Whale 0x123",
    conditions=[
        Condition("wallet", "==", "0x1234567890abcdef..."),
        Condition("whale_size", ">", 25000)
    ],
    actions=[
        Action("buy", {"size": 2500})
    ]
)
```

### Use Case 2: Team-Specific Strategy
```python
# Follow all Ravens-related whale activity
playbook = Playbook(
    id="ravens_strategy",
    name="Ravens Whale Follow",
    conditions=[
        Condition("market_name", "contains", "ravens"),
        Condition("whale_size", ">", 40000),
        Condition("whale_confidence", ">", 80)
    ],
    actions=[
        Action("buy", {"size": 3000})
    ]
)
```

### Use Case 3: Multi-Market Arbitrage
```python
# Complex arb across 3 platforms
route = ArbitrageRoute(
    id="poly_kalshi_draft",
    name="Poly → Kalshi → DraftKings",
    buy_platform="polymarket",
    sell_platform="kalshi",
    intermediate_steps=[
        {"platform": "draftkings", "action": "hedge"}
    ],
    min_spread_pct=2.5
)
```

---

## 🚨 BEST PRACTICES

### 1. Start Conservative
- Begin with high thresholds ($50K+ whale size)
- Low position sizes ($1K-2K)
- Long cooldowns (10+ minutes)

### 2. Test in Paper Trading Mode
```python
PAPER_TRADING_MODE = True  # in config.py
```

### 3. Monitor Performance
- Check P&L regularly
- Adjust thresholds based on results
- Disable underperforming playbooks

### 4. Use Watchlists
- Curate quality wallets/markets
- Don't follow every signal
- Focus on proven performers

### 5. Combine Strategies
- Use multiple playbooks together
- Diversify across market types
- Balance aggressive + conservative

---

## 🔍 DEBUGGING

### Check Playbook Status
```bash
python playbooks.py --list
```

### View Evaluation Logs
Enable debug mode in `config.py`:
```python
DEBUG_MODE = True
```

### Test Playbook Conditions
```python
from playbooks import PlaybookManager

manager = PlaybookManager()
playbook = manager.get_playbook("patriots_whale_follow")

# Test with mock data
test_data = {
    "whale_size": 60000,
    "market_name": "Patriots to win Super Bowl",
    "whale_action": "buy"
}

if playbook.evaluate(test_data):
    print("✅ Conditions met!")
    actions = playbook.execute()
else:
    print("❌ Conditions not met")
```

---

## 📚 COMMAND REFERENCE

```bash
# View all playbooks
python launch.py --playbooks
python playbooks.py --list

# Load preset
python launch.py --load-playbook <preset_id>
python playbooks.py --load-preset <preset_id>

# View watchlists
python launch.py --watchlists
python playbooks.py --list-watchlists

# View signal queue
python launch.py --signals
python playbooks.py --list-signals

# Create custom
python playbooks.py --create

# Interactive menu
python launch.py
# Then select [7] Playbooks
```

---

## 🎉 YOU'RE READY!

```bash
# Load some playbooks
python launch.py --load-playbook patriots_whale_follow
python launch.py --load-playbook mvp_arb

# Start the system
python launch.py --full

# Or run with playbooks enabled
python apollo_edge.py --mode=monitor
```

Playbooks will now automatically execute when conditions are met! 🎯

---

## ⚠️ SAFETY NOTES

- ✅ Test in paper trading mode first
- ✅ Set reasonable position limits
- ✅ Use cooldowns to prevent overtrading
- ✅ Monitor performance regularly
- ✅ Start conservative, scale gradually
- ⚠️ Playbooks can execute rapidly - be careful!
- ⚠️ Always set max execution limits
- ⚠️ Review conditions carefully before enabling

---

## 🚀 HAPPY TRADING!

Playbooks automate your edge so you can focus on strategy. 📋

