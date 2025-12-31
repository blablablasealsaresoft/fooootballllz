@echo off
REM ====================================================================
REM APOLLO EDGE - LOAD ALL CORE PLAYBOOKS
REM Loads all 9 essential playbooks for your 5 core features
REM ====================================================================

echo.
echo ====================================================================
echo           LOADING ALL CORE PLAYBOOKS
echo           9 Playbooks for 5 Core Features
echo ====================================================================
echo.

REM WHALE DETECTION & SNIPING
echo [1/9] Loading: Whale Snipe $10K+...
python playbooks.py --load-preset whale_snipe_10k
echo.

echo [2/9] Loading: Whale Snipe $25K+ (Auto)...
python playbooks.py --load-preset whale_snipe_25k
echo.

REM 5-HOP CLUSTER ANALYSIS
echo [3/9] Loading: Coordinated Whale Cluster...
python playbooks.py --load-preset whale_cluster_alert
echo.

echo [4/9] Loading: CEX Whale Tracker...
python playbooks.py --load-preset cex_whale_detector
echo.

REM SPORTSBOOK VALUE DETECTION
echo [5/9] Loading: MVP Value vs Sportsbooks...
python playbooks.py --load-preset sportsbook_value_mvp
echo.

echo [6/9] Loading: Super Bowl Value Detector...
python playbooks.py --load-preset sportsbook_value_superbowl
echo.

REM NFL PROPS COVERAGE
echo [7/9] Loading: Super Bowl Momentum...
python playbooks.py --load-preset superbowl_momentum
echo.

echo [8/9] Loading: AFC/NFC Champion Value...
python playbooks.py --load-preset afc_nfc_champion_value
echo.

echo [9/9] Loading: Player Props Whale Follow...
python playbooks.py --load-preset player_props_whale
echo.

echo ====================================================================
echo                    ALL PLAYBOOKS LOADED!
echo ====================================================================
echo.
echo Your 9 core playbooks are now active and will auto-load on startup!
echo.
echo VERIFY:
echo   python launch.py --playbooks
echo.
echo START TRADING:
echo   python launch.py --full
echo.
echo ====================================================================
pause

