#!/usr/bin/env python3
"""
LOAD ALL CORE PLAYBOOKS
========================
Loads all 9 essential playbooks for your 5 core features.

RUN THIS ONCE:
    python load_all_playbooks.py

Then all playbooks will auto-load on every system start!
"""

import subprocess
import time

print("""
====================================================================
           LOADING ALL CORE PLAYBOOKS
           9 Playbooks for 5 Core Features
====================================================================
""")

# All 9 core playbooks
PLAYBOOKS = [
    # WHALE DETECTION & SNIPING
    ("whale_snipe_10k", "Whale Snipe $10K+"),
    ("whale_snipe_25k", "Whale Snipe $25K+ (Auto)"),
    
    # 5-HOP CLUSTER ANALYSIS
    ("whale_cluster_alert", "Coordinated Whale Cluster"),
    ("cex_whale_detector", "CEX Whale Tracker"),
    
    # SPORTSBOOK VALUE DETECTION
    ("sportsbook_value_mvp", "MVP Value vs Sportsbooks"),
    ("sportsbook_value_superbowl", "Super Bowl Value Detector"),
    
    # NFL PROPS COVERAGE
    ("superbowl_momentum", "Super Bowl Momentum"),
    ("afc_nfc_champion_value", "AFC/NFC Champion Value"),
    ("player_props_whale", "Player Props Whale Follow"),
]

print(f"[*] Loading {len(PLAYBOOKS)} core playbooks...\n")

loaded = 0
failed = 0

for playbook_id, name in PLAYBOOKS:
    print(f"  Loading: {name}...")
    try:
        result = subprocess.run(
            ["python", "playbooks.py", "--load-preset", playbook_id],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Loaded:" in result.stdout or result.returncode == 0:
            print(f"    [SUCCESS]\n")
            loaded += 1
        else:
            print(f"    [FAILED]\n")
            failed += 1
            
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    [ERROR]: {e}\n")
        failed += 1

print("="*60)
print(f"RESULTS: {loaded} loaded, {failed} failed")
print("="*60)

if loaded > 0:
    print(f"""
[SUCCESS!] {loaded} playbooks are now active!

Your playbooks will auto-load on every system start.

VERIFY:
  python launch.py --playbooks

START TRADING:
  python launch.py --full

All your core features are now automated!
""")
else:
    print("""
[WARNING] No playbooks loaded. Check for errors above.

Try loading manually:
  python playbooks.py --load-preset whale_snipe_25k
""")

