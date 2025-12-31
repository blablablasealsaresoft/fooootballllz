# 💰 FUNDING YOUR APOLLO EDGE BOT

## Your Wallet: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc
## Your Account: @Sappyseeel

---

## 🎯 SIMPLE SETUP (RECOMMENDED)

Your config is now set to **Direct Wallet Mode** (simpler!):
```python
USE_BUILDER_RELAYER = False  # No proxy complexity
```

### **What You Need to Fund**

Your main wallet: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc`

**Funds needed:**
- **USDC**: $500-1000 (for trading)
- **MATIC**: 10 MATIC (~$5-10) (for gas fees)

**Why MATIC?**
- Each trade costs ~$0.02-0.50 in gas
- 10 MATIC = ~200 trades
- Small amount goes a long way

---

## 💵 HOW TO FUND YOUR WALLET

### **Method 1: Polymarket.com (EASIEST)**

1. **Go to Polymarket**
   - Visit: https://polymarket.com
   - Click "Connect Wallet"
   - Connect your MetaMask (0x843eB2EA...)

2. **Deposit**
   - Click "Deposit" button
   - Choose amount (start with $500)
   - Follow bridge instructions
   - USDC automatically on Polygon!

3. **Add MATIC**
   - Visit: https://wallet.polygon.technology/
   - Bridge MATIC from Ethereum
   - Or buy directly on exchange

**Total time: 10-15 minutes**

---

### **Method 2: Exchange Withdrawal**

**For USDC:**
1. **Go to your exchange** (Coinbase, Binance, etc.)
2. **Withdraw USDC**
   - Select **Polygon network** (CRITICAL!)
   - NOT Ethereum, NOT other chains
3. **Enter address**: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc`
4. **Amount**: $500-1000
5. **Confirm** withdrawal
6. **Wait**: 5-10 minutes

**For MATIC:**
1. **Withdraw MATIC** from exchange
2. **Select Polygon network**
3. **Enter address**: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc`
4. **Amount**: 10-20 MATIC
5. **Confirm**

**Total time: 15-20 minutes**

---

### **Method 3: Polygon Bridge (From Ethereum)**

If you have USDC on Ethereum mainnet:

1. **Go to Polygon Bridge**
   - Visit: https://wallet.polygon.technology/polygon/bridge
   - Connect MetaMask

2. **Bridge USDC**
   - Select: USDC
   - Amount: $500-1000
   - Destination: Polygon PoS
   - Confirm transaction

3. **Wait**
   - Takes 7-8 minutes
   - USDC appears on Polygon

4. **Bridge MATIC too**
   - Same process for MATIC
   - Amount: 10-20 MATIC

**Total time: 20-30 minutes**

---

## 🔍 VERIFY YOUR BALANCE

### **Check on Polygonscan**
```
Visit: https://polygonscan.com/address/0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc

You'll see:
- USDC balance: $XXX
- MATIC balance: XX MATIC
- Transaction history
```

### **Check in Apollo Edge**
```bash
python launch.py
# Select [S] View Status

Shows:
- Wallet balance: $XXX USDC
- MATIC balance: XX MATIC
- Ready to trade: YES/NO
```

---

## 💸 HOW TO WITHDRAW FUNDS

### **Option 1: Use MetaMask**
```
1. Open MetaMask
2. Select your wallet (0x843eB2EA...)
3. Click "Send"
4. Enter destination address
5. Select token (USDC)
6. Enter amount
7. Confirm
8. Done!
```

### **Option 2: Send Back to Exchange**
```
1. Get your exchange deposit address
2. IMPORTANT: Use Polygon network
3. Send USDC from 0x843eB2EA... to exchange
4. Wait for confirmations
5. USDC appears in exchange account
```

### **Option 3: Send to Another Wallet**
```
# Just send like any Polygon transaction
From: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc
To: Any address you control
Token: USDC
Network: Polygon
```

**It's YOUR wallet - you control everything!**

---

## 📊 GAS COST BREAKDOWN

### **Typical Costs (Direct Wallet)**
```
Trade (buy/sell): ~$0.10-0.30
Approve token: ~$0.20 (one-time per token)
Transfer USDC: ~$0.05
Claim winnings: ~$0.15

Average trade: $0.50 total
With 10 MATIC: ~200 trades
```

### **When to Refill MATIC**
```
System will warn you:
"[WARNING] Low MATIC balance: 1.2 MATIC remaining"

Refill when under 5 MATIC
Add 10-20 MATIC at a time
```

---

## 🚨 IMPORTANT NOTES

### **Network Selection**
```
✅ ALWAYS use Polygon network
❌ NOT Ethereum
❌ NOT BSC
❌ NOT other chains

Your wallet exists on ALL chains,
but USDC and bot are on POLYGON only!
```

### **USDC Contract Addresses**
```
Polygon USDC: 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
Polygon USDC.e: 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359

Either works! Apollo Edge supports both.
```

### **Security**
```
✅ Only fund what you can afford to lose
✅ Start with small amount ($500)
✅ Test with paper trading first
✅ Keep private key secure
✅ Never share private key
```

---

## 📝 YOUR COMPLETE SETUP CHECKLIST

### **Configuration**
- [x] Wallet address set: `0x843eB2EA...` ✅
- [x] TheOddsAPI key: `31c44bdb...` ✅
- [x] Direct wallet mode enabled ✅
- [ ] Private key added (line 40 in config.py)

### **Funding**
- [ ] Fund main wallet with USDC ($500-1000)
- [ ] Fund main wallet with MATIC (10-20 MATIC)
- [ ] Verify balance on Polygonscan
- [ ] Verify Apollo Edge sees balance

### **Testing**
- [x] Paper trading tested ✅
- [x] Playbooks loaded (9/9) ✅
- [x] System operational ✅
- [ ] Add private key and test with small amount

### **Go Live**
- [ ] Set `PAPER_TRADING_MODE = False`
- [ ] Start with `MAX_POSITION_SIZE_USD = 100`
- [ ] Run `python launch.py --full`
- [ ] Monitor first trades closely

---

## 🎉 YOUR NEXT STEPS

### **Step 1: Add Private Key**
```python
# config.py, line 40:
TRADING_WALLET_PRIVATE_KEY = "0xYourMetaMaskKeyHere"
```

### **Step 2: Fund Wallet**
```
Transfer to: 0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc
- $500 USDC (Polygon network)
- 10 MATIC (Polygon network)
```

### **Step 3: Test with Paper Mode**
```bash
python launch.py --full
# Watch it detect whales and simulate trades
```

### **Step 4: Go Live (When Ready)**
```python
# config.py:
PAPER_TRADING_MODE = False
MAX_POSITION_SIZE_USD = 100  # Start tiny!
```

```bash
python launch.py --full
```

---

## 🔄 WITHDRAWING PROFITS

### **Anytime You Want**
```
Your wallet = Your control!

1. Open MetaMask
2. Send USDC to wherever you want
3. Keep some MATIC for gas
4. That's it!
```

### **After Trading Session**
```
# Check your balance
python launch.py
# Select [S] View Status

# Shows:
- Starting balance: $1000
- Current balance: $1250
- Profit: $250
- Withdraw via MetaMask whenever you want!
```

---

## ✅ SUMMARY

**Your Wallet Setup:**
- **Address**: `0x843eB2EA48302E1CCB179F6352D5A0FF0F576EEc` ✅
- **Mode**: Direct wallet (simple) ✅
- **No proxy needed** ✅
- **Just add private key** ✅
- **Fund with USDC + MATIC** 
- **Trade and withdraw freely** ✅

**It's that simple!** 🎯

Want me to help you get your private key from MetaMask safely?

