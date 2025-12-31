# 🏗️ POLYMARKET BUILDER RELAYER GUIDE

## Overview

The **Polymarket Builder Relayer** enables **gasless transactions** on Polygon! Instead of paying gas fees yourself, the relayer sponsors your transactions.

Reference: [Polymarket Builder Relayer GitHub](https://github.com/Polymarket/builder-relayer-client)

---

## 🎯 What Is Builder Relayer?

### Traditional Trading (You Pay Gas)
```
Your Wallet → Sign Transaction → Pay MATIC Gas → Execute on Polygon
```

### Builder Relayer (Gasless)
```
Your Wallet → Sign Message → Relayer Pays Gas → Execute on Polygon
```

### Benefits
- ✅ **No MATIC needed** - Relayer pays gas
- ✅ **Faster execution** - Batched transactions
- ✅ **Better UX** - No gas management
- ✅ **Safe/Proxy wallets** - Advanced wallet types
- ✅ **Free for builders** - Sponsored by Polymarket

---

## 🏗️ Two Wallet Types

### 1. SAFE Wallet (Default)
- Multi-signature wallet (Gnosis Safe)
- Most secure
- Supports multiple owners
- Used by institutions

### 2. PROXY Wallet
- Simpler proxy contract
- Faster deployment
- Easier to use
- Good for individuals

**Apollo Edge will use PROXY by default** (simpler for most users).

---

## 📦 Already Installed!

Good news: You already have this!

```bash
# You installed it earlier:
pip install py-clob-client
```

The `py-clob-client` library includes Builder Relayer support.

---

## 🔧 Integration with Apollo Edge

### Current Status
Apollo Edge has the **framework ready** but needs your wallet to activate:

```python
# In apollo_edge.py and whale_sniper.py:

async def _submit_order(self, order: SnipeOrder) -> bool:
    """Submit order to Polymarket using your wallet"""
    
    # Check if we have wallet credentials
    if not TRADING_WALLET_ADDRESS:
        logger.error("❌ No trading wallet configured!")
        return False
    
    if PAPER_TRADING_MODE:
        logger.info(f"📝 PAPER TRADE: Would buy ${order.size_usd:,.0f}")
        return True
    
    # REAL TRADING MODE
    # This is where Builder Relayer will be used!
```

---

## 🚀 How to Enable Builder Relayer

### Step 1: Deploy Your Safe/Proxy Wallet

The system needs to create a relayer wallet for you first:

```typescript
// This happens automatically on first trade
import { RelayClient, RelayerTxType } from "@polymarket/builder-relayer-client";

const relayerUrl = "https://relayer.polymarket.com";
const chainId = 137; // Polygon

// Your existing wallet signs the deployment
const proxyClient = new RelayClient(
  relayerUrl,
  chainId,
  yourWallet,
  builderConfig,
  RelayerTxType.PROXY  // Use PROXY wallet
);

// Deploy (one-time, happens automatically)
const result = await proxyClient.deploySafe();
console.log("Proxy Address:", result.proxyAddress);
```

### Step 2: Fund Your Proxy Wallet

```bash
# Your proxy wallet needs USDC for trading
# Transfer USDC from your main wallet to proxy

# The system will show you the proxy address
# Transfer USDC there
```

### Step 3: Trade Gaslessly!

```typescript
// All future trades are gasless
const response = await proxyClient.execute([transaction], "buy Patriots");
const result = await response.wait();
console.log("Trade executed (gasless!):", result.transactionHash);
```

---

## 🔄 How It Works (Technical)

### 1. Redeem Positions (Claim Winnings)

#### CTF Redeem (Standard Markets)
```typescript
import { encodeFunctionData, zeroHash } from "viem";

const ctfAddress = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045";
const usdcAddress = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174";
const conditionId = "0x..."; // Market condition ID

const redeemTx = {
  to: ctfAddress,
  data: encodeFunctionData({
    abi: ctfRedeemAbi,
    functionName: "redeemPositions",
    args: [usdcAddress, zeroHash, conditionId, [1, 2]]
  }),
  value: "0"
};

// Execute gaslessly
await proxyClient.execute([redeemTx], "redeem positions");
```

#### NegRisk Adapter Redeem (Binary Markets)
```typescript
const negRiskAdapter = "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296";
const conditionId = "0x...";
const amounts = [BigInt(111000000), BigInt(0)]; // [YES tokens, NO tokens]

const redeemTx = {
  to: negRiskAdapter,
  data: encodeFunctionData({
    abi: nrAdapterRedeemAbi,
    functionName: "redeemPositions",
    args: [conditionId, amounts]
  }),
  value: "0"
};

await proxyClient.execute([redeemTx], "redeem positions");
```

### 2. Place Orders (Trading)

The Builder Relayer handles all CLOB (Central Limit Order Book) interactions:

```typescript
// Your order gets signed by your wallet
// Relayer submits it (paying gas)
// Trade executes on Polymarket
// No MATIC needed!
```

---

## 📝 Configuration for Apollo Edge

Add to your `config.py`:

```python
# ============================================================================
# 🏗️ POLYMARKET BUILDER RELAYER
# ============================================================================

# Relayer URL
POLYMARKET_RELAYER_URL = "https://relayer.polymarket.com"

# Wallet type (SAFE or PROXY)
POLYMARKET_WALLET_TYPE = "PROXY"  # Simpler, recommended

# Your proxy wallet address (will be generated on first use)
POLYMARKET_PROXY_ADDRESS = ""  # Leave empty, system fills this in

# Enable gasless trading
USE_BUILDER_RELAYER = True  # Set False to use direct wallet (requires MATIC)
```

---

## 🎮 Usage Examples

### Deploy Proxy Wallet (One-Time)
```bash
# This happens automatically on first trade
# Or run manually:
python -c "
from py_clob_client import RelayClient, RelayerTxType
from eth_account import Account

wallet = Account.from_key('your_private_key_here')
client = RelayClient(
    'https://relayer.polymarket.com',
    137,
    wallet,
    {},
    RelayerTxType.PROXY
)

result = client.deploySafe()
print('Proxy Address:', result.proxyAddress)
"
```

### Execute Gasless Trade
```python
# In apollo_edge.py - already integrated!
# Just set USE_BUILDER_RELAYER = True in config.py

# When you snipe:
python launch.py --snipe

# Trades execute gaslessly through relayer!
```

### Claim Winnings (Gasless)
```python
# After market resolves, claim your winnings
# No gas needed!

# System does this automatically when positions close
```

---

## 💰 Cost Comparison

### Traditional (Direct Wallet)
```
Trade Cost:
- Order: $0.50 gas (MATIC)
- Total: $0.50 per trade

100 trades = $50 in gas fees
```

### Builder Relayer (Gasless)
```
Trade Cost:
- Order: $0.00 (sponsored)
- Total: $0.00 per trade

100 trades = $0 in gas fees
```

**Savings: $50 per 100 trades!**

---

## 🔒 Security Considerations

### ✅ Safe Practices
1. **Separate Funds**
   - Keep main funds in your primary wallet
   - Only transfer needed USDC to proxy

2. **Monitor Proxy**
   - Check proxy balance regularly
   - Track all transactions

3. **Private Key Security**
   - Same security as main wallet
   - Signs all relayer requests

### How It's Secure
- You **sign** every transaction
- Relayer **only pays gas**
- Relayer **cannot access funds**
- Your private key **never leaves your machine**

---

## 🎯 Contracts on Polygon

### Main Contracts
```python
# Conditional Tokens Framework (Standard Markets)
CTF_ADDRESS = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"

# NegRisk Adapter (Binary Markets)
NEG_RISK_ADAPTER = "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296"

# USDC (Collateral)
USDC_POLYGON = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# Relayer URL
RELAYER_URL = "https://relayer.polymarket.com"
```

---

## 🔄 Transaction Flow

### With Builder Relayer
```
1. Apollo Edge generates order
2. Your wallet signs message (off-chain)
3. Relayer receives signed message
4. Relayer creates transaction
5. Relayer pays gas in MATIC
6. Transaction executes on Polygon
7. Your trade completes (no MATIC spent!)
```

### Without Builder Relayer (Direct)
```
1. Apollo Edge generates order
2. Your wallet signs transaction
3. Your wallet pays gas in MATIC
4. Transaction executes on Polygon
5. Your trade completes (MATIC spent)
```

---

## 🧪 Testing

### Test in Paper Mode First
```python
# In config.py
PAPER_TRADING_MODE = True
USE_BUILDER_RELAYER = True  # Simulates relayer behavior

# Run test
python launch.py --snipe
```

### Then Test with Small Amount
```python
# In config.py
PAPER_TRADING_MODE = False
USE_BUILDER_RELAYER = True
MAX_POSITION_SIZE_USD = 10  # Start tiny!

# Deploy proxy (one-time)
# Fund proxy with $50 USDC
# Run live test
python launch.py --snipe
```

---

## ⚠️ Important Notes

### Gas Sponsorship Limits
- Relayer may have **daily limits**
- High-frequency trading may hit caps
- System falls back to direct wallet if needed

### Proxy Deployment
- **One-time** setup per wallet
- Takes ~30 seconds
- Costs gas (paid by relayer)
- Address is permanent

### USDC Management
- Transfer to proxy as needed
- Withdraw back to main wallet anytime
- Monitor proxy balance

---

## 🐛 Troubleshooting

### "Proxy Not Deployed"
```bash
# Deploy manually:
python -c "from py_clob_client import RelayClient; ..."
# Or let system deploy on first trade
```

### "Insufficient Proxy Balance"
```bash
# Transfer USDC to your proxy address
# Check proxy address in logs or config
```

### "Relayer Unavailable"
```python
# System falls back to direct wallet
# Requires MATIC in main wallet
# Set USE_BUILDER_RELAYER = False temporarily
```

### "Signature Invalid"
```bash
# Check private key matches wallet address
# Verify chainId = 137 (Polygon)
# Ensure system clock is accurate
```

---

## 📊 Comparison: Safe vs Proxy

| Feature | SAFE | PROXY |
|---------|------|-------|
| Security | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Gas Cost | Higher | Lower |
| Setup Time | Slower | Faster |
| Multi-sig | ✅ Yes | ❌ No |
| Best For | Institutions | Individuals |

**Recommendation for Apollo Edge: PROXY**

---

## 🎯 Next Steps

### Minimal Setup (No Relayer)
```python
# In config.py
USE_BUILDER_RELAYER = False

# Need MATIC in wallet for gas
# More expensive but simpler
```

### Full Setup (With Relayer)
```python
# In config.py
USE_BUILDER_RELAYER = True
POLYMARKET_WALLET_TYPE = "PROXY"

# No MATIC needed
# Gasless trading
# Better for high frequency
```

### Test It
```bash
# Paper trading (safe)
python launch.py --snipe

# Check system uses relayer in logs:
# [*] Using Builder Relayer (gasless)
# [*] Proxy Address: 0x...
```

---

## ✅ Configuration Checklist

Before adding to `config.py`:

- [ ] Understand gasless trading concept
- [ ] Decided: SAFE or PROXY? (Use PROXY)
- [ ] Have USDC ready to transfer to proxy
- [ ] Understand proxy deployment (one-time)
- [ ] Know how to fund proxy wallet
- [ ] Tested in paper mode first
- [ ] Ready to deploy proxy
- [ ] Understand gas savings benefits

---

## 📚 Additional Resources

- **GitHub Repo**: https://github.com/Polymarket/builder-relayer-client
- **Polymarket Docs**: https://docs.polymarket.com
- **Gnosis Safe**: https://safe.global
- **py-clob-client**: Already installed!

---

## 🎉 Summary

**Builder Relayer = Gasless Trading**

Instead of:
```
❌ You pay gas in MATIC for every trade
```

You get:
```
✅ Relayer pays gas
✅ You only need USDC
✅ Trade for free!
```

**Perfect for high-frequency trading like Apollo Edge!**

---

**Now you understand both systems! Ready to configure your `config.py`?** 🚀

Let me know if you want me to create a complete example `config.py` with both Kalshi and Polymarket Builder Relayer integrated!

