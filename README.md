# 🎯 APOLLO EDGE

## *Institutional-Grade Prediction Market Intelligence*

<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   █████╗ ██████╗  ██████╗ ██╗     ██╗      ██████╗                    ║
║  ██╔══██╗██╔══██╗██╔═══██╗██║     ██║     ██╔═══██╗                   ║
║  ███████║██████╔╝██║   ██║██║     ██║     ██║   ██║                   ║
║  ██╔══██║██╔═══╝ ██║   ██║██║     ██║     ██║   ██║                   ║
║  ██║  ██║██║     ╚██████╔╝███████╗███████╗╚██████╔╝                   ║
║  ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  EDGE              ║
║                                                                       ║
║        Whale Detection • Cross-Chain Tracing • Live Arbitrage        ║
║                   Automated Sniping • NFL Props                       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Polymarket](https://img.shields.io/badge/Polymarket-Integrated-green.svg)](https://polymarket.com)

</div>

---

## 🚀 What Is Apollo Edge?

Apollo Edge is an **institutional-grade trading intelligence system** for prediction markets. It detects whale movements, traces cross-chain fund flows, identifies arbitrage opportunities, and can execute trades in sub-second timeframes.

```mermaid
flowchart TB
    subgraph "🌊 DATA SOURCES"
        PM[("Polymarket\nAPI")]
        KL[("Kalshi\nAPI")]
        ESPN[("ESPN\nLive Feed")]
        ETH[("Etherscan\nV2 API")]
        SOL[("Solana\nRPC")]
    end

    subgraph "🧠 APOLLO EDGE CORE"
        WD["🐋 Whale Detector"]
        CT["🔗 Cluster Tracer"]
        AS["💰 Arb Scanner"]
        LG["⚡ Live Game Engine"]
        PB["📋 Playbook Manager"]
    end

    subgraph "⚡ EXECUTION"
        SN["🎯 Snipe Engine"]
        RM["🛡️ Risk Manager"]
        PM_EX[("Polymarket\nExecution")]
    end

    subgraph "📊 OUTPUT"
        AL["🚨 Alerts"]
        TR["📈 Trades"]
        AN["📊 Analytics"]
    end

    PM --> WD
    PM --> AS
    KL --> AS
    ESPN --> LG
    ETH --> WD
    ETH --> CT
    SOL --> CT

    WD --> PB
    CT --> PB
    AS --> PB
    LG --> PB

    PB --> SN
    SN --> RM
    RM --> PM_EX

    PB --> AL
    PM_EX --> TR
    SN --> AN
```

---

## 🎯 Core Capabilities

### 🐋 **Whale Detection & Sniping**

Monitors Polymarket in real-time, detects large positions (>$10K), and can automatically follow whale trades.

```mermaid
sequenceDiagram
    participant PM as Polymarket CTF
    participant WD as Whale Detector
    participant CF as Confidence Scorer
    participant SE as Snipe Engine
    participant EX as Execution

    loop Every 500ms
        WD->>PM: Scan Recent Trades
        PM-->>WD: New Transactions
        WD->>WD: Filter > $10K
        WD->>CF: Score Confidence
        CF-->>WD: 85% Confidence
        
        alt Size > $25K & Confidence > 70%
            WD->>SE: Create Snipe Order
            SE->>SE: Calculate Size (10% of whale)
            SE->>EX: Execute Trade
            EX-->>SE: Fill Confirmation
        else Below Threshold
            WD->>WD: Log & Alert Only
        end
    end
```

### 🔗 **5-Hop Cross-Chain Tracing**

Traces funding sources from Polygon back through Wormhole bridges to Solana, identifying original CEX sources.

```mermaid
flowchart LR
    subgraph "POLYGON"
        PW["🎯 Polymarket\nWallet"]
    end

    subgraph "BRIDGE"
        WH["🌉 Wormhole"]
        AB["🌉 Allbridge"]
    end

    subgraph "SOLANA"
        SW1["Wallet 1"]
        SW2["Wallet 2"]
        SW3["Wallet 3"]
    end

    subgraph "CEX SOURCES"
        BIN["Binance"]
        CB["Coinbase"]
        OKX["OKX"]
    end

    PW -.->|"Trace Back"| WH
    PW -.->|"Trace Back"| AB
    WH -.-> SW1
    WH -.-> SW2
    AB -.-> SW3
    SW1 -.->|"Hop 1-3"| BIN
    SW2 -.->|"Hop 1-5"| CB
    SW3 -.->|"Hop 1-4"| OKX

    style PW fill:#e1f5fe
    style BIN fill:#fff3e0
    style CB fill:#fff3e0
    style OKX fill:#fff3e0
```

### ⚡ **Live Game Arbitrage**

Detects game events (touchdowns, injuries) faster than sportsbooks can update odds, creating arbitrage windows.

```mermaid
gantt
    title Live Game Arbitrage Timeline
    dateFormat X
    axisFormat %Lms

    section Event Detection
    Touchdown Scored       :done, 0, 50
    ESPN API Detects       :done, 50, 100
    Apollo Edge Alerts     :done, 100, 150

    section Our Execution
    Create Order           :active, 150, 175
    Submit to Polymarket   :active, 175, 225
    Order Filled           :crit, 225, 275

    section Sportsbook Lag
    Book Notices Event     :5000, 10000
    Book Updates Odds      :10000, 20000
    Arb Window Closes      :20000, 30000
```

### 📋 **Automated Playbooks**

Pre-configured trading strategies that auto-execute based on customizable conditions.

```mermaid
flowchart TD
    subgraph "📋 PLAYBOOK TYPES"
        WF["🐋 Whale Follow\nFollow trades > $50K"]
        MC["📊 Market Condition\nPrice thresholds"]
        AR["💰 Arbitrage\nCross-platform arb"]
        CL["🔗 Cluster\nCoordinated wallets"]
        TB["⏰ Time-Based\nScheduled trades"]
    end

    subgraph "🎯 CONDITIONS"
        C1["whale_size > 50000"]
        C2["market_price < 0.30"]
        C3["spread_pct > 3%"]
        C4["cluster_size > 5"]
        C5["game_time == kickoff"]
    end

    subgraph "⚡ ACTIONS"
        A1["BUY 10% of whale"]
        A2["SELL at threshold"]
        A3["EXECUTE arb route"]
        A4["ALERT + Follow"]
        A5["ENTER position"]
    end

    WF --> C1 --> A1
    MC --> C2 --> A2
    AR --> C3 --> A3
    CL --> C4 --> A4
    TB --> C5 --> A5
```

---

## 📊 System Architecture

```mermaid
flowchart TB
    subgraph "📥 INPUT LAYER"
        direction TB
        API1["Polymarket Gamma API"]
        API2["Polymarket CLOB"]
        API3["Kalshi API"]
        API4["Etherscan V2"]
        API5["ESPN Live"]
        API6["Solana RPC"]
    end

    subgraph "🧠 PROCESSING LAYER"
        direction TB
        
        subgraph "Detection"
            WH["Whale Detector"]
            TR["Cluster Tracer"]
            AR["Arb Scanner"]
        end
        
        subgraph "Analysis"
            CS["Confidence Scorer"]
            PQ["Priority Queue"]
            SG["Signal Generator"]
        end
        
        subgraph "Strategy"
            PB["Playbook Manager"]
            WL["Watchlist Engine"]
            RQ["Route Calculator"]
        end
    end

    subgraph "⚡ EXECUTION LAYER"
        direction TB
        SE["Snipe Engine"]
        RM["Risk Manager"]
        OM["Order Manager"]
    end

    subgraph "📤 OUTPUT LAYER"
        direction TB
        EX["Trade Execution"]
        AL["Alerts & Logs"]
        DB["Position DB"]
    end

    API1 --> WH
    API2 --> WH
    API3 --> AR
    API4 --> TR
    API5 --> AR
    API6 --> TR

    WH --> CS
    TR --> CS
    AR --> CS
    
    CS --> PQ
    PQ --> SG
    SG --> PB
    
    PB --> WL
    WL --> RQ
    RQ --> SE
    
    SE --> RM
    RM --> OM
    
    OM --> EX
    OM --> AL
    OM --> DB
```

---

## 🏁 Quick Start

### 1. Install Dependencies

```bash
pip install requests aiohttp websocket-client
```

### 2. Run the System

```bash
# Interactive menu (no wallet needed)
python launch.py

# Or use direct commands
python launch.py --whales      # Find whale positions
python launch.py --arb         # Scan arbitrage opportunities
python launch.py --props       # NFL props scanner
python launch.py --clusters    # Cluster analysis demo
```

### 3. For Live Trading

```bash
# Copy config template
cp config_template.py config.py

# Edit config.py with your wallet details
# Set PAPER_TRADING_MODE = False

# Start sniping
python launch.py --snipe
```

---

## 📁 Project Structure

```mermaid
graph LR
    subgraph "🎯 Core Modules"
        AE["apollo_edge.py\n(Main Engine)"]
        WS["whale_sniper.py\n(Detection + Sniping)"]
        LG["live_game_arbitrage.py\n(Live Arb)"]
    end

    subgraph "🔍 Analysis"
        WF["whale_finder.py\n(Wallet Analysis)"]
        SB["solana_bridge_tracer.py\n(Cross-Chain)"]
        NP["nfl_props_scanner.py\n(Props Markets)"]
    end

    subgraph "⚙️ Configuration"
        PB["playbooks.py\n(Strategy Manager)"]
        AS["auto_scaling.py\n(Capital Scaling)"]
        CF["config.py\n(Settings)"]
    end

    subgraph "🚀 Entry Points"
        LA["launch.py\n(CLI Interface)"]
    end

    LA --> AE
    LA --> WS
    LA --> LG
    LA --> WF
    LA --> SB
    LA --> NP

    AE --> PB
    WS --> AS
    AE --> CF
```

| File | Description |
|------|-------------|
| `launch.py` | Interactive CLI with menu system |
| `apollo_edge.py` | Main orchestration engine |
| `whale_sniper.py` | Real-time whale detection & auto-sniping |
| `live_game_arbitrage.py` | Sub-second live game event detection |
| `whale_finder.py` | Wallet analysis & 5-hop tracing |
| `solana_bridge_tracer.py` | Cross-chain Solana → Polygon tracing |
| `nfl_props_scanner.py` | Comprehensive NFL props market coverage |
| `playbooks.py` | Automated strategy playbooks |
| `auto_scaling.py` | Dynamic capital-based position sizing |
| `config.py` | Centralized configuration |

---

## 🐋 Whale Detection Flow

```mermaid
stateDiagram-v2
    [*] --> Scanning: Start Monitoring

    Scanning --> NewTrade: Trade Detected
    NewTrade --> SizeCheck: Check Position Size
    
    SizeCheck --> TooSmall: < $10K
    SizeCheck --> WhaleAlert: >= $10K
    
    TooSmall --> Scanning: Skip
    
    WhaleAlert --> ConfidenceCheck: Score Confidence
    
    ConfidenceCheck --> LowConfidence: < 70%
    ConfidenceCheck --> HighConfidence: >= 70%
    
    LowConfidence --> AlertOnly: Log Alert
    AlertOnly --> Scanning
    
    HighConfidence --> SnipeCheck: Check Snipe Threshold
    
    SnipeCheck --> BelowSnipe: < $25K
    SnipeCheck --> Snipeable: >= $25K
    
    BelowSnipe --> AlertOnly
    
    Snipeable --> CreateOrder: Generate Snipe Order
    CreateOrder --> RiskCheck: Validate Risk Limits
    
    RiskCheck --> RiskFail: Limits Exceeded
    RiskCheck --> Execute: Within Limits
    
    RiskFail --> AlertOnly
    
    Execute --> Filled: Order Successful
    Execute --> Retry: Order Failed
    
    Retry --> Execute: Retry (max 3)
    Retry --> AlertOnly: All Retries Failed
    
    Filled --> ManagePosition: Track Position
    ManagePosition --> Scanning
```

---

## 💰 Auto-Scaling Capital Management

The system automatically adjusts trading parameters based on your wallet balance:

```mermaid
xychart-beta
    title "Position Size Scaling by Balance"
    x-axis ["$100", "$200", "$500", "$1K", "$2K", "$5K"]
    y-axis "Max Position ($)" 0 --> 2500
    bar [45, 90, 225, 450, 900, 2250]
```

| Balance | Max/Trade | Positions | Daily Trades | Follow % |
|---------|-----------|-----------|--------------|----------|
| $100 | $45 | 1 | 5 | 1% |
| $200 | $90 | 1 | 5 | 1% |
| $500 | $225 | 2 | 10 | 2% |
| $1,000 | $450 | 2 | 15 | 5% |
| $2,000 | $900 | 3 | 20 | 10% |
| $5,000 | $2,250 | 4 | 20 | 10% |

---

## 🏈 NFL Props Coverage

```mermaid
mindmap
  root((NFL Props))
    Championship
      Super Bowl Winner
      AFC Champion
      NFC Champion
    Awards
      MVP
      OPOY
      DPOY
      Super Bowl MVP
    Player Props
      Passing Yards
      Passing TDs
      Rushing Yards
      Rushing TDs
      Receiving Yards
      Receptions
    Game Props
      Spreads
      Totals
      Moneylines
      Quarter Props
    Super Bowl Specials
      First TD Scorer
      Coin Toss
      Anthem Length
      Gatorade Color
```

---

## ⚡ Speed Optimizations

Apollo Edge is built for **millisecond-level execution**:

```mermaid
flowchart LR
    subgraph "Detection"
        D1["Poll Interval:\n500ms"]
        D2["Event Detection:\n<100ms"]
    end
    
    subgraph "Processing"
        P1["Signal Generation:\n<50ms"]
        P2["Playbook Eval:\n<25ms"]
    end
    
    subgraph "Execution"
        E1["Order Creation:\n<25ms"]
        E2["Submission:\n<100ms"]
    end

    D1 --> D2 --> P1 --> P2 --> E1 --> E2

    style D1 fill:#e3f2fd
    style D2 fill:#e3f2fd
    style P1 fill:#fff3e0
    style P2 fill:#fff3e0
    style E1 fill:#e8f5e9
    style E2 fill:#e8f5e9
```

**Target Latencies:**
- Event Detection: <500ms
- Trade Execution: <100ms
- Total Event-to-Fill: <1 second

---

## 🛡️ Risk Management

```mermaid
flowchart TD
    subgraph "📊 Position Limits"
        PL1["Max Position: $5,000"]
        PL2["Max Concurrent: 10"]
        PL3["Max Capital: $10,000"]
    end

    subgraph "🛑 Exit Rules"
        EX1["Stop Loss: -15%"]
        EX2["Take Profit: +50%"]
        EX3["Time Limit: 7 days"]
    end

    subgraph "📆 Daily Limits"
        DL1["Max Snipes: 20/day"]
        DL2["Max Loss: $2,000/day"]
        DL3["Cooldown: 60s between"]
    end

    subgraph "⚠️ Safety"
        SF1["Paper Trading Mode"]
        SF2["Slippage Protection: 1%"]
        SF3["Wallet Validation"]
    end
```

---

## 🔌 API Integrations

| API | Purpose | Status |
|-----|---------|--------|
| **Polymarket Gamma** | Market data, prices | ✅ Active |
| **Polymarket CLOB** | Orderbook, execution | ✅ Active |
| **Kalshi** | Cross-platform arb | ✅ Active |
| **Etherscan V2** | On-chain tracing | ✅ Active |
| **ESPN** | Live game events | ✅ Active |
| **Solana RPC** | Cross-chain tracing | ✅ Active |
| **Wormhole** | Bridge transaction lookup | ✅ Active |

---

## 📈 Command Reference

### Interactive Mode
```bash
python launch.py
```

### Direct Commands
```bash
# Whale Operations
python launch.py --whales                    # Find whales
python launch.py --snipe                     # Active sniping
python launch.py --monitor                   # Passive monitoring

# Analysis
python launch.py --clusters                  # Cluster analysis
python launch.py --wallet 0x...              # Analyze wallet
python launch.py --arb                       # Arbitrage scan

# Markets
python launch.py --props                     # NFL props

# System
python launch.py --full                      # Full system
python launch.py --status                    # View status
```

### Individual Modules
```bash
python whale_sniper.py --mode=demo
python apollo_edge.py --mode=scan
python nfl_props_scanner.py
python solana_bridge_tracer.py --polygon-address 0x...
```

---

## ⚙️ Configuration

Create `config.py` from the template:

```python
# === WALLET CONFIGURATION ===
TRADING_WALLET_ADDRESS = "0x..."
TRADING_WALLET_PRIVATE_KEY = "..."  # Never share!
PAPER_TRADING_MODE = True           # Start with paper trading

# === DETECTION THRESHOLDS ===
MIN_WHALE_SIZE_USD = 10000          # Minimum to track
SNIPE_THRESHOLD_USD = 25000         # Minimum to auto-snipe
MIN_CONFIDENCE_SCORE = 70           # Minimum confidence

# === EXECUTION ===
FOLLOW_PERCENTAGE = 0.10            # Follow 10% of whale
MAX_POSITION_SIZE_USD = 5000        # Max per trade
MAX_SLIPPAGE_PCT = 1.0              # Slippage tolerance

# === RISK MANAGEMENT ===
STOP_LOSS_PCT = 15.0                # Auto stop-loss
TAKE_PROFIT_PCT = 50.0              # Auto take-profit
MAX_DAILY_SNIPES = 20               # Daily limit
MAX_DAILY_LOSS_USD = 2000           # Loss limit
```

---

## 🎓 How It Works

### The Edge: Following Smart Money

```mermaid
flowchart LR
    subgraph "👀 They Act"
        W["Whale buys\n$100K YES\non Chiefs"]
    end

    subgraph "🎯 We Detect"
        D["Detect in\n<1 second"]
    end

    subgraph "💰 We Follow"
        F["Buy $10K YES\n(10% of whale)"]
    end

    subgraph "📈 Result"
        R["Price moves up\nWe profit"]
    end

    W --> D --> F --> R
```

### The Cross-Chain Trace

```mermaid
flowchart TB
    Q["Who funded this\nPolymarket whale?"]
    
    Q --> T1["Check Polygon\ntransactions"]
    T1 --> T2["Found: Wormhole\nbridge deposit"]
    T2 --> T3["Trace to Solana\nsource wallet"]
    T3 --> T4["5-hop analysis\nback to CEX"]
    T4 --> A["Answer: Funded\nfrom Binance"]
```

---

## 📊 Sample Output

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    APOLLO EDGE - NFL BETTING INTELLIGENCE              ║
╚═══════════════════════════════════════════════════════════════════════╝

[12:34:56] 🐋 WHALE DETECTED: $87,500 BUY on Chiefs -3.5
           Wallet: 0x7a23...4f2b
           Confidence: 89%
           ⚡ SNIPING: $8,750 (10% follow)

[12:34:56] ✅ SNIPE EXECUTED
           Fill Price: 0.62
           Est. Profit: +$4,200 at 0.85

[12:35:12] 💰 ARBITRAGE FOUND
           Chiefs ML: Polymarket 0.58 / Kalshi 0.63
           Spread: 5.2%
           Max Size: $15,000
           
[12:35:30] 🏈 LIVE EVENT: Touchdown KC
           Detected in: 89ms
           Arb Window: ~15 seconds
           Executing...
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⚠️ Disclaimer

This software is for educational purposes only. Trading prediction markets involves significant risk. Never trade with money you can't afford to lose. Past performance does not guarantee future results.

---

## 📄 License

MIT License - see LICENSE file for details.

---

<div align="center">

**Built for the next generation of prediction market traders**

🐋 Detect Whales • 🔗 Trace Clusters • ⚡ Execute Fast • 💰 Capture Edge

</div>
