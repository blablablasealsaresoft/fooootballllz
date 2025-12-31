# 🏗️ PROXY WALLET - COMPLETE GUIDE

## Your Account: @Sappyseeel
## Main Wallet: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc

---

## 🎯 TWO OPTIONS FOR TRADING

### **Option 1: Direct Wallet (RECOMMENDED FOR BEGINNERS)**

**Setup:**
```python
# In config.py:
USE_BUILDER_RELAYER = False
TRADING_WALLET_ADDRESS = "0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc"
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"
```

**Fund:**
- Transfer USDC to: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc`
- Add some MATIC for gas (~$10 = 200 trades)

**Trade:**
- Just run: `python launch.py --full`
- Trades execute from your main wallet
- MATIC used for gas

**Withdraw:**
- Send USDC back to yourself anytime
- It's your wallet - you control everything!

**Pros:**
- ✅ Simplest setup
- ✅ No proxy deployment needed
- ✅ Easy withdrawals
- ✅ Full control

**Cons:**
- ⚠️ Pay MATIC gas ($0.50/trade)

---

### **Option 2: Proxy Wallet (GASLESS - ADVANCED)**

**Setup:**
```python
# In config.py:
USE_BUILDER_RELAYER = True
POLYMARKET_WALLET_TYPE = "PROXY"
```

**How It Works:**

#### **Step 1: Proxy Gets Deployed (Automatic)**
```
First time you trade:
1. System creates proxy contract for you
2. Relayer pays deployment gas
3. You get proxy address: 0xABC...
4. System saves it to config.py
```

#### **Step 2: Fund the Proxy**
```
Transfer USDC:
From: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc (your main)
To: 0xABC... (your proxy - shown in logs)
Amount: $500-1000 to start
```

#### **Step 3: Trade Gaslessly**
```
All trades execute from proxy:
- Relayer pays gas in MATIC
- You only spend USDC
- No MATIC needed!
```

#### **Step 4: Withdraw Funds**
```python
# The proxy is YOUR contract - you control it!

# Withdraw USDC from proxy back to main wallet:
from py_clob_client import RelayClient, RelayerTxType
from eth_account import Account

# Your wallet
wallet = Account.from_key("your_private_key")

# Connect to your proxy
client = RelayClient(
    "https://relayer.polymarket.com",
    137,  # Polygon
    wallet,
    {},
    RelayerTxType.PROXY
)

# Withdraw USDC
usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
amount = 1000 * 10**6  # $1000 USDC (6 decimals)

# Transfer from proxy back to your main wallet
transfer_tx = create_transfer_tx(
    token=usdc_address,
    to=wallet.address,  # Your main wallet
    amount=amount
)

# Execute via relayer (gasless!)
result = await client.execute([transfer_tx], "withdraw")
```

**Pros:**
- ✅ No MATIC needed
- ✅ Gasless trading ($0/trade)
- ✅ Lower costs over time

**Cons:**
- ⚠️ More complex setup
- ⚠️ Need to deploy proxy first
- ⚠️ Extra step to withdraw

---

## 💡 **MY RECOMMENDATION**

### **For @Sappyseeel: Start with Direct Wallet**

**Why:**
1. ✅ **Simpler** - No proxy complexity
2. ✅ **Faster** - Use immediately
3. ✅ **Easier** - Simple withdrawals
4. ✅ **Flexible** - Switch to proxy later if wanted

**Setup (2 Steps):**

**Step 1: Add Private Key**
```python
# config.py, line 40:
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"

# Line 130:
USE_BUILDER_RELAYER = False
```

**Step 2: Fund Wallet**
```
Send USDC + some MATIC to:
0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc

Amounts:
- USDC: $500-1000 (for trading)
- MATIC: ~10 MATIC ($5) (for gas)
```

**Then:**
```bash
python launch.py --full
```

**Done! You're trading!**

---

## 🔄 **HOW TO WITHDRAW FUNDS**

### **From Direct Wallet (Simple)**
```
Your wallet IS your trading wallet!
Just send USDC to any address you want.

Use MetaMask:
1. Open MetaMask
2. Select Send
3. Enter destination address
4. Enter amount
5. Send!
```

### **From Proxy Wallet (Advanced)**
```python
# Create withdraw_funds.py script:

from py_clob_client import RelayClient, RelayerTxType
from eth_account import Account
from web3 import Web3

# Load your wallet
private_key = "0xYourKeyHere"
wallet = Account.from_key(private_key)

# Connect to proxy
client = RelayClient(
    "https://relayer.polymarket.com",
    137,
    wallet,
    {},
    RelayerTxType.PROXY
)

# Your proxy address (from config.py or logs)
proxy_address = "0xYourProxyAddress"

# Transfer USDC from proxy to main wallet
usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
amount_to_withdraw = 1000 * 10**6  # $1000 (USDC has 6 decimals)

# Create transfer transaction
# This requires building the ERC20 transfer call
# (Full implementation available in Polymarket docs)

print(f"Withdrawing ${amount_to_withdraw/10**6} USDC")
print(f"From proxy: {proxy_address}")
print(f"To main wallet: {wallet.address}")
```

**Or simpler:**
```
Use Polymarket.com:
1. Connect your main wallet (0x843eB2EA...)
2. Go to "Withdraw"
3. System recognizes your proxy
4. Withdraw USDC back to main wallet
5. Done!
```

---

## 🎯 **CHECKING YOUR PROXY ADDRESS**

### **If You Use Builder Relayer:**

**Option A: Check Logs**
```
When proxy deploys, you'll see:
[INFO] Proxy wallet deployed: 0xABC123...
[INFO] Transfer USDC to proxy for trading
```

**Option B: Check config.py**
```python
# System updates this automatically:
POLYMARKET_PROXY_ADDRESS = "0xABC123..."
```

**Option C: Query Polymarket**
```python
# Your proxy is deterministic based on your main wallet
# Formula: CREATE2(your_wallet, salt, proxy_bytecode)
# The system calculates this automatically
```

---

## 💰 **FUNDING GUIDE**

### **Step 1: Fund Main Wallet First**
```
Address: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc
What: USDC on Polygon + some MATIC
How: Polymarket.com deposit or exchange withdrawal
```

### **Step 2: If Using Proxy**
```
Wait for first trade:
1. Proxy gets deployed automatically
2. System shows proxy address
3. Transfer USDC from main → proxy
4. Trade gaslessly!
```

### **Step 3: If Direct Wallet**
```
Just trade from main wallet:
- No proxy needed
- Simpler flow
- Pay small gas fees
```

---

## 🔧 **CONFIGURATION COMPARISON**

### **Direct Wallet (RECOMMENDED)**
```python
# config.py:
USE_BUILDER_RELAYER = False
TRADING_WALLET_ADDRESS = "0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc"
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"

# Fund main wallet with:
# - USDC: $500-1000
# - MATIC: 10 MATIC (~$5)

# Trade: python launch.py --full
# Withdraw: Use MetaMask anytime
```

### **Proxy Wallet (ADVANCED)**
```python
# config.py:
USE_BUILDER_RELAYER = True
POLYMARKET_WALLET_TYPE = "PROXY"
TRADING_WALLET_ADDRESS = "0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc"
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"

# Step 1: Fund main wallet with USDC
# Step 2: Run: python launch.py --full
# Step 3: System deploys proxy (shows address)
# Step 4: Transfer USDC to proxy
# Step 5: Trade gaslessly
# Withdraw: Use py-clob-client or Polymarket.com
```

---

## ✅ **MY RECOMMENDATION FOR YOU**

### **Start Simple - Use Direct Wallet**

```python
# Edit config.py:

# Line 40 - Add your private key
TRADING_WALLET_PRIVATE_KEY = "0xYourKeyHere"

# Line 130 - Set to False
USE_BUILDER_RELAYER = False
```

**Then:**
1. Fund `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc` with USDC + MATIC
2. Run: `python launch.py --full`
3. Start trading immediately!
4. Withdraw anytime via MetaMask

**Later, if you want gasless:**
- Change `USE_BUILDER_RELAYER = True`
- Restart system
- Proxy deploys automatically
- Transfer funds to proxy when prompted

---

## 🎯 **QUICK START (RIGHT NOW)**

```python
# 1. Edit config.py, add these two lines:

# Line 40:
TRADING_WALLET_PRIVATE_KEY = "0xYourMetaMaskPrivateKey"

# Line 130:
USE_BUILDER_RELAYER = False  # Direct wallet (simpler!)
```

```bash
# 2. Fund your wallet
# Go to: https://polymarket.com
# Connect: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc
# Deposit: $500 USDC + 10 MATIC
```

```bash
# 3. Launch
python launch.py --full
```

**You're trading! No proxy complexity!** 🚀

---

## 🔄 **FUNDS FLOW COMPARISON**

### **Direct Wallet (Simple)**
```
Deposit → Main Wallet (0x843eB2EA...)
Trade → From Main Wallet
Withdraw → Send from Main Wallet (MetaMask)

✅ ONE wallet to manage
✅ Easy deposits/withdrawals
```

### **Proxy Wallet (Advanced)**
```
Deposit → Main Wallet (0x843eB2EA...)
Deploy → Proxy Created (0xABC...)
Transfer → Main → Proxy
Trade → From Proxy (gasless!)
Withdraw → Proxy → Main → Destination

⚠️ TWO wallets to manage
⚠️ Extra transfer steps
```

---

## 💡 **BOTTOM LINE**

**For @Sappyseeel:**

1. **Add your private key** to config.py (line 40)
2. **Set `USE_BUILDER_RELAYER = False`** (line 130)
3. **Fund your main wallet**: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc`
4. **Launch**: `python launch.py --full`

**You'll be trading in 5 minutes with NO proxy complexity!**

**Want me to update your config.py to use direct wallet mode right now?**
