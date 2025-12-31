#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                           APOLLO EDGE - UNIFIED LAUNCHER                      ║
║                                                                               ║
║              BlackRock-Tier NFL Betting Intelligence System                   ║
║                                                                               ║
║     Whale Detection • Cluster Analysis • Arbitrage • Fast Execution • Props   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

QUICK START:
    python launch.py                    # Interactive menu
    python launch.py --full             # Full system (all modules)
    python launch.py --whales           # Whale detection only
    python launch.py --snipe            # Active sniping mode
    python launch.py --arb              # Arbitrage scanner
    python launch.py --props            # NFL props scanner

YOUR API KEY IS EMBEDDED: I47C92D1C8TN7JRRXGHCY8UXYCHE5UYEPJ
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# ============================================================================
# ASCII ART BANNER
# ============================================================================

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ██████╗  ██████╗ ██╗     ██╗      ██████╗     ███████╗██████╗  ██████╗ ███████╗
║    ██╔══██╗██╔══██╗██╔═══██╗██║     ██║     ██╔═══██╗    ██╔════╝██╔══██╗██╔════╝ ██╔════╝
║    ███████║██████╔╝██║   ██║██║     ██║     ██║   ██║    █████╗  ██║  ██║██║  ███╗█████╗  
║    ██╔══██║██╔═══╝ ██║   ██║██║     ██║     ██║   ██║    ██╔══╝  ██║  ██║██║   ██║██╔══╝  
║    ██║  ██║██║     ╚██████╔╝███████╗███████╗╚██████╔╝    ███████╗██████╔╝╚██████╔╝███████╗
║    ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝ ╚═════╝     ╚══════╝╚═════╝  ╚═════╝ ╚══════╝
║                                                                               ║
║                    NFL BETTING INTELLIGENCE SYSTEM                            ║
║                                                                               ║
║     🐋 Whale Detection    📊 Cluster Analysis    💰 Arbitrage Scanner        ║
║     ⚡ Fast Execution     🏈 Full Props          📈 Position Management       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# MODULES
# ============================================================================

MODULES = {
    "apollo_edge": {
        "file": "apollo_edge.py",
        "name": "Apollo Edge - Full System",
        "description": "Complete trading system with all modules",
        "commands": {
            "demo": ["python", "apollo_edge.py", "--mode=demo"],
            "scan": ["python", "apollo_edge.py", "--mode=scan"],
            "monitor": ["python", "apollo_edge.py", "--mode=monitor"],
        }
    },
    "whale_finder": {
        "file": "whale_finder.py",
        "name": "Whale Finder",
        "description": "Find and analyze Polymarket whales",
        "commands": {
            "find": ["python", "whale_finder.py"],
            "analyze": ["python", "whale_finder.py"],  # + wallet address
        }
    },
    "whale_sniper": {
        "file": "whale_sniper.py",
        "name": "Whale Sniper",
        "description": "Real-time whale detection and sniping",
        "commands": {
            "monitor": ["python", "whale_sniper.py", "--mode=monitor"],
            "snipe": ["python", "whale_sniper.py", "--mode=snipe"],
            "demo": ["python", "whale_sniper.py", "--mode=demo"],
        }
    },
    "nfl_props": {
        "file": "nfl_props_scanner.py",
        "name": "NFL Props Scanner",
        "description": "Scan all NFL props across platforms",
        "commands": {
            "scan": ["python", "nfl_props_scanner.py"],
        }
    },
    "cluster_analyzer": {
        "file": "polymarket_whale_hunter_v2.py",
        "name": "Cluster Analyzer",
        "description": "5-hop wallet cluster analysis",
        "commands": {
            "demo": ["python", "polymarket_whale_hunter_v2.py"],
        }
    },
    "solana_tracer": {
        "file": "solana_bridge_tracer.py",
        "name": "Solana Bridge Tracer",
        "description": "Trace deposits from Solana to Polygon",
        "commands": {
            "trace": ["python", "solana_bridge_tracer.py"],
        }
    },
    "playbooks": {
        "file": "playbooks.py",
        "name": "Playbooks & Playlists",
        "description": "Pre-configured trading strategies",
        "commands": {
            "list": ["python", "playbooks.py", "--list"],
            "watchlists": ["python", "playbooks.py", "--list-watchlists"],
            "signals": ["python", "playbooks.py", "--list-signals"],
            "create": ["python", "playbooks.py", "--create"],
        }
    },
    "live_arb": {
        "file": "live_game_arbitrage.py",
        "name": "Live Game Arbitrage",
        "description": "Real-time game event detection for arbitrage",
        "commands": {
            "monitor": ["python", "live_game_arbitrage.py"],
        }
    }
}


# ============================================================================
# FUNCTIONS
# ============================================================================

def check_dependencies():
    """Check if required packages are installed"""
    required = ["requests", "aiohttp", "websocket-client"]
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print("[*] Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing, 
                      capture_output=True)
        print("[+] Dependencies installed")
    
    return True


def run_module(module_name: str, command: str = None, extra_args: list = None):
    """Run a specific module"""
    if module_name not in MODULES:
        print(f"[!] Unknown module: {module_name}")
        return
    
    module = MODULES[module_name]
    
    # Check if file exists
    if not os.path.exists(module["file"]):
        print(f"[!] Module file not found: {module['file']}")
        return
    
    # Get command
    if command and command in module["commands"]:
        cmd = module["commands"][command]
    else:
        # Default to first command
        cmd = list(module["commands"].values())[0]
    
    # Add extra args
    if extra_args:
        cmd = cmd + extra_args
    
    print(f"\n[*] Starting: {module['name']}")
    print(f"[*] Command: {' '.join(cmd)}")
    print("-" * 60)
    
    # Run
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Stopped")


def interactive_menu():
    """Show interactive menu"""
    
    # Check config status once
    config_exists = os.path.exists("config.py")
    wallet_configured = False
    paper_mode = True
    wallet_addr = ""
    
    if config_exists:
        try:
            from config import TRADING_WALLET_ADDRESS, PAPER_TRADING_MODE
            wallet_configured = (TRADING_WALLET_ADDRESS and 
                               TRADING_WALLET_ADDRESS != "0xYOUR_WALLET_ADDRESS_HERE")
            paper_mode = PAPER_TRADING_MODE
            wallet_addr = TRADING_WALLET_ADDRESS[:10] + "..." if wallet_configured else ""
        except:
            pass
    
    while True:
        print(BANNER)
        
        # Show trading status
        print("="*70)
        if not config_exists:
            print("  ⚠️  CONFIG NOT FOUND - Copy config_template.py to config.py")
        elif not wallet_configured:
            print("  ⚠️  WALLET NOT SET - Edit config.py and add your wallet")
        elif paper_mode:
            print(f"  📝 PAPER TRADING MODE - Wallet: {wallet_addr}")
            print("     (Set PAPER_TRADING_MODE = False in config.py for live trading)")
        else:
            print(f"  💰 LIVE TRADING MODE - Wallet: {wallet_addr}")
            print("     ⚠️  Real trades will execute automatically!")
        print("="*70)
        
        print("\nMAIN MENU")
        print()
        print("  [1] 🐋 Find Whales          - Scan for large Polymarket positions")
        print("  [2] ⚡ Whale Sniper          - Real-time detection & auto-snipe")
        print("  [3] 📊 Cluster Analysis      - 5-hop wallet funding trace")
        print("  [4] 💰 Arbitrage Scanner     - Find cross-platform opportunities")
        print("  [5] 🏈 NFL Props Scanner     - Full props market coverage")
        print("  [6] 🚀 Full System           - All modules combined")
        print()
        print("  [7] 📋 Playbooks             - View/manage trading strategies")
        print("  [8] 👁️  Watchlists           - Monitor wallets/markets")
        print("  [9] 📊 Signal Queue          - View prioritized opportunities")
        print()
        print("  [A] Analyze Wallet          - Deep dive on specific wallet")
        print("  [S] View Status             - System status and stats")
        print("  [H] Setup Guide             - How to configure your wallet")
        print()
        print("  [Q] Quit")
        print()
        
        choice = input("Select option: ").strip().upper()
        
        if choice == "1":
            run_module("whale_finder", "find")
        elif choice == "2":
            print("\n  [a] Monitor Only (passive)")
            print("  [b] Active Sniping (auto-trade)")
            sub = input("  Select: ").strip().lower()
            if sub == "a":
                run_module("whale_sniper", "monitor")
            elif sub == "b":
                if not wallet_configured:
                    print("\n  ❌ Cannot snipe without wallet configured!")
                    print("     Edit config.py and add your wallet first.")
                elif paper_mode:
                    print("\n  📝 Paper trading mode - trades will be simulated")
                    run_module("whale_sniper", "snipe")
                else:
                    print("\n  ⚠️  WARNING: LIVE TRADING MODE!")
                    print("     Real trades will execute with your wallet!")
                    confirm = input("  Type 'SNIPE' to confirm: ").strip()
                    if confirm == "SNIPE":
                        run_module("whale_sniper", "snipe")
        elif choice == "3":
            run_module("cluster_analyzer", "demo")
        elif choice == "4":
            run_module("apollo_edge", "scan")
        elif choice == "5":
            run_module("nfl_props", "scan")
        elif choice == "6":
            if not wallet_configured:
                print("\n  Running in scan-only mode (no wallet configured)")
            run_module("apollo_edge", "monitor")
        elif choice == "7":
            print("\n  [a] List Playbooks")
            print("  [b] Load Preset Playbook")
            print("  [c] Create Custom Playbook")
            sub = input("  Select: ").strip().lower()
            if sub == "a":
                run_module("playbooks", "list")
            elif sub == "b":
                print("\nAvailable presets:")
                print("  - patriots_whale_follow")
                print("  - chiefs_value")
                print("  - mvp_arb")
                print("  - whale_cluster_alert")
                print("  - superbowl_momentum")
                print("  - fade_the_public")
                preset = input("\nEnter preset ID: ").strip()
                subprocess.run(["python", "playbooks.py", "--load-preset", preset])
            elif sub == "c":
                run_module("playbooks", "create")
        elif choice == "8":
            run_module("playbooks", "watchlists")
        elif choice == "9":
            run_module("playbooks", "signals")
        elif choice.upper() == "A":
            wallet = input("Enter wallet address: ").strip()
            if wallet.startswith("0x"):
                run_module("whale_finder", "analyze", [wallet])
        elif choice.upper() == "S":
            show_status()
        elif choice.upper() == "H":
            print("\n" + "="*60)
            print("WALLET SETUP GUIDE")
            print("="*60)
            print("""
1. Copy the config template:
   cp config_template.py config.py

2. Open config.py in your editor

3. Find these lines and fill in your details:
   
   TRADING_WALLET_ADDRESS = "0xYourWalletAddress"
   TRADING_WALLET_PRIVATE_KEY = "0xYourPrivateKey"

4. For testing, keep:
   PAPER_TRADING_MODE = True

5. For live trading, change to:
   PAPER_TRADING_MODE = False

⚠️  SECURITY:
- Never share your private key
- Never commit config.py to git
- Use a dedicated trading wallet
- Only fund with what you can lose
            """)
        elif choice == "Q":
            print("\n[*] Goodbye!")
            break
        else:
            print("[!] Invalid option")
        
        input("\nPress Enter to continue...")
        os.system('clear' if os.name == 'posix' else 'cls')


def show_status():
    """Show system status"""
    print("\n" + "="*60)
    print("SYSTEM STATUS")
    print("="*60)
    print(f"\nTimestamp: {datetime.now().isoformat()}")
    
    # Check if config.py exists and is configured
    config_exists = os.path.exists("config.py")
    wallet_configured = False
    paper_mode = True
    
    if config_exists:
        try:
            from config import TRADING_WALLET_ADDRESS, PAPER_TRADING_MODE
            wallet_configured = (TRADING_WALLET_ADDRESS and 
                               TRADING_WALLET_ADDRESS != "0xYOUR_WALLET_ADDRESS_HERE")
            paper_mode = PAPER_TRADING_MODE
        except:
            pass
    
    print()
    print("Configuration:")
    print(f"  config.py exists: {'✅' if config_exists else '❌ (copy config_template.py)'}")
    print(f"  Wallet configured: {'✅' if wallet_configured else '❌ (add your wallet to config.py)'}")
    print(f"  Trading mode: {'📝 PAPER (simulated)' if paper_mode else '💰 LIVE (real trades)'}")
    print(f"  API Key: Etherscan V2 (I47C92D1...YEPJ)")
    print()
    
    print("Modules Available:")
    for name, module in MODULES.items():
        exists = "✅" if os.path.exists(module["file"]) else "❌"
        print(f"  {exists} {module['name']}: {module['file']}")
    
    print()
    print("Default Settings:")
    print("  Chain: Polygon (137)")
    print("  Min Whale Size: $10,000")
    print("  Snipe Threshold: $25,000")
    print("  Max Position: $5,000")
    print("  Stop Loss: 15%")
    print("  Take Profit: 50%")
    
    if not config_exists:
        print()
        print("⚠️  TO START TRADING:")
        print("   1. cp config_template.py config.py")
        print("   2. Edit config.py with your wallet address + private key")
        print("   3. Set PAPER_TRADING_MODE = False for live trading")


def main():
    import argparse
    import sys
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        if sys.stderr:
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    parser = argparse.ArgumentParser(
        description="Apollo Edge - NFL Betting Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    python launch.py                    # Interactive menu
    python launch.py --full             # Run full system
    python launch.py --whales           # Find whales
    python launch.py --snipe            # Active sniping
    python launch.py --arb              # Arbitrage scan
    python launch.py --props            # NFL props scan
    python launch.py --wallet 0x123...  # Analyze wallet
        """
    )
    
    parser.add_argument("--full", action="store_true", help="Run full system")
    parser.add_argument("--whales", action="store_true", help="Find whales")
    parser.add_argument("--snipe", action="store_true", help="Active sniping")
    parser.add_argument("--monitor", action="store_true", help="Passive monitoring")
    parser.add_argument("--arb", action="store_true", help="Arbitrage scanner")
    parser.add_argument("--props", action="store_true", help="NFL props scanner")
    parser.add_argument("--clusters", action="store_true", help="Cluster analysis")
    parser.add_argument("--wallet", type=str, help="Analyze specific wallet")
    parser.add_argument("--playbooks", action="store_true", help="List all playbooks")
    parser.add_argument("--watchlists", action="store_true", help="List watchlists")
    parser.add_argument("--signals", action="store_true", help="Show signal queue")
    parser.add_argument("--load-playbook", type=str, help="Load preset playbook")
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Route to appropriate module
    if args.full:
        print(BANNER)
        run_module("apollo_edge", "monitor")
    elif args.whales:
        print(BANNER)
        run_module("whale_finder", "find")
    elif args.snipe:
        print(BANNER)
        print("\n⚠️  ACTIVE SNIPING MODE - Will execute trades!")
        run_module("whale_sniper", "snipe")
    elif args.monitor:
        print(BANNER)
        run_module("whale_sniper", "monitor")
    elif args.arb:
        print(BANNER)
        run_module("apollo_edge", "scan")
    elif args.props:
        print(BANNER)
        run_module("nfl_props", "scan")
    elif args.clusters:
        print(BANNER)
        run_module("cluster_analyzer", "demo")
    elif args.wallet:
        print(BANNER)
        run_module("whale_finder", "analyze", [args.wallet])
    elif args.playbooks:
        print(BANNER)
        run_module("playbooks", "list")
    elif args.watchlists:
        print(BANNER)
        run_module("playbooks", "watchlists")
    elif args.signals:
        print(BANNER)
        run_module("playbooks", "signals")
    elif args.load_playbook:
        print(BANNER)
        subprocess.run(["python", "playbooks.py", "--load-preset", args.load_playbook])
    else:
        # Interactive menu
        interactive_menu()


if __name__ == "__main__":
    main()
