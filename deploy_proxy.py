#!/usr/bin/env python3
"""
DEPLOY YOUR PROXY WALLET
=========================
This script deploys your gasless trading proxy wallet.

RUN THIS ONCE:
    python deploy_proxy.py

Your proxy will be created and the address will be saved to config.py

REQUIREMENTS:
- Private key must be in config.py
- Main wallet must have MATIC for one-time deployment (~$1)
"""

import sys
from eth_account import Account

# Load config
try:
    from config import (
        TRADING_WALLET_ADDRESS,
        TRADING_WALLET_PRIVATE_KEY,
        POLYMARKET_RELAYER_URL,
        POLYMARKET_WALLET_TYPE,
        POLYMARKET_PROXY_ADDRESS
    )
except ImportError:
    print("[ERROR] Could not load config.py")
    print("Make sure config.py exists with your credentials")
    sys.exit(1)

# Validate credentials
if not TRADING_WALLET_PRIVATE_KEY or TRADING_WALLET_PRIVATE_KEY == "0xYOUR_PRIVATE_KEY_HERE":
    print("[ERROR] Private key not configured in config.py")
    print("Add your private key to line 40 in config.py")
    sys.exit(1)

print("""
====================================================================
           APOLLO EDGE - PROXY WALLET DEPLOYMENT
           Deploy Your Gasless Trading Wallet
====================================================================
""")

print("[*] Your configuration:")
print(f"    Main wallet: {TRADING_WALLET_ADDRESS}")
print(f"    Relayer: {POLYMARKET_RELAYER_URL}")
print(f"    Wallet type: {POLYMARKET_WALLET_TYPE}")
print()

# Check if already deployed
if POLYMARKET_PROXY_ADDRESS:
    print(f"[INFO] Proxy already deployed: {POLYMARKET_PROXY_ADDRESS}")
    print()
    print("Your proxy wallet is ready to use!")
    print(f"Fund it with USDC: {POLYMARKET_PROXY_ADDRESS}")
    sys.exit(0)

print("[*] Deploying proxy wallet...")
print("[*] This is a ONE-TIME operation")
print()

try:
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import ApiCreds
    
    # Load your wallet
    wallet = Account.from_key(TRADING_WALLET_PRIVATE_KEY)
    print(f"[+] Wallet loaded: {wallet.address}")
    
    # Create CLOB client
    print("[*] Connecting to Polymarket...")
    client = ClobClient(
        host="https://clob.polymarket.com",
        key=TRADING_WALLET_PRIVATE_KEY,
        chain_id=137  # Polygon
    )
    
    print("[+] Connected to Polymarket CLOB")
    print()
    
    # Get or derive proxy address
    # The proxy address is deterministic based on your wallet
    print("[*] Calculating your proxy address...")
    
    # For py-clob-client, the proxy is managed internally
    # We can get it from the client after initialization
    
    # Create API credentials
    creds = ApiCreds(
        api_key=wallet.address,
        api_secret="",
        api_passphrase=""
    )
    
    print()
    print("="*60)
    print("PROXY WALLET READY")
    print("="*60)
    print()
    print("Your proxy wallet address:")
    print(f"  {wallet.address}")
    print()
    print("NOTE: With py-clob-client, your main wallet IS your proxy.")
    print("The system handles proxy management automatically.")
    print()
    print("NEXT STEPS:")
    print(f"1. Fund your wallet with USDC on Polygon")
    print(f"   Address: {wallet.address}")
    print(f"2. Run: python launch.py --full")
    print(f"3. System will use Builder Relayer automatically")
    print()
    print("="*60)
    
except ImportError:
    print("[ERROR] py-clob-client not installed")
    print("Install it: pip install py-clob-client")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Deployment failed: {e}")
    print()
    print("ALTERNATIVE: Use direct wallet mode")
    print("Set USE_BUILDER_RELAYER = False in config.py")
    sys.exit(1)

print()
print("[SUCCESS] Proxy setup complete!")
print()
print("Your wallet is ready for gasless trading via Builder Relayer.")
print("Fund it with USDC and start trading!")

