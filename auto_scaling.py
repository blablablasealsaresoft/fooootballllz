#!/usr/bin/env python3
"""
AUTO-SCALING CAPITAL MANAGEMENT
================================
Automatically adjusts trading limits based on your wallet balance.

FEATURES:
- Detects USDC balance in real-time
- Scales position sizes automatically
- Adjusts daily limits based on capital
- No manual config updates needed!

USAGE:
    # Enable in config.py:
    ENABLE_AUTO_SCALING = True
    
    # System automatically adjusts when you add funds!
"""

from typing import Dict
import logging

logger = logging.getLogger('AutoScaling')


class AutoScalingManager:
    """Manages auto-scaling of trading parameters based on balance"""
    
    def __init__(self, config):
        self.config = config
        self.enable_auto_scaling = getattr(config, 'ENABLE_AUTO_SCALING', True)
        self.capital_usage_pct = getattr(config, 'CAPITAL_USAGE_PCT', 90)
        self.position_size_pct = getattr(config, 'POSITION_SIZE_PCT', 50)
        self.min_reserve = getattr(config, 'MIN_USDC_RESERVE', 10)
        
        self.last_balance = 0
        self.scaled_limits = {}
    
    def calculate_limits(self, usdc_balance: float) -> Dict:
        """Calculate trading limits based on current balance"""
        
        if not self.enable_auto_scaling:
            # Use manual limits from config
            return {
                "max_capital": self.config.MAX_TRADING_CAPITAL,
                "max_position": self.config.MAX_POSITION_SIZE_USD,
                "max_positions": self.config.MAX_CONCURRENT_POSITIONS,
                "max_daily_snipes": self.config.MAX_DAILY_SNIPES,
                "max_daily_loss": self.config.MAX_DAILY_LOSS_USD,
                "follow_pct": self.config.FOLLOW_PERCENTAGE,
                "auto_scaled": False
            }
        
        # AUTO-SCALING MODE
        
        # Available capital = balance - reserve
        available = max(0, usdc_balance - self.min_reserve)
        
        # Trading capital = 90% of available
        max_trading = available * (self.capital_usage_pct / 100)
        
        # Position size = 50% of trading capital per position
        max_position = max(10, max_trading * (self.position_size_pct / 100))
        
        # Max concurrent positions
        if max_position > 0:
            max_concurrent = min(10, int(max_trading / max_position))
        else:
            max_concurrent = 1
        
        # Daily snipes scale with capital
        if usdc_balance < 200:
            max_daily = 5
        elif usdc_balance < 500:
            max_daily = 10
        elif usdc_balance < 1000:
            max_daily = 15
        else:
            max_daily = 20
        
        # Daily loss = 30% of capital (or manual setting)
        max_daily_loss = min(
            available * 0.30,  # 30% max
            self.config.MAX_DAILY_LOSS_USD if hasattr(self.config, 'MAX_DAILY_LOSS_USD') else 1000
        )
        
        # Follow percentage scales with capital
        if usdc_balance < 200:
            follow_pct = 0.01  # 1% for small capital
        elif usdc_balance < 500:
            follow_pct = 0.02  # 2% for medium capital
        elif usdc_balance < 1000:
            follow_pct = 0.05  # 5% for growing capital
        else:
            follow_pct = 0.10  # 10% for large capital
        
        limits = {
            "balance": usdc_balance,
            "available": available,
            "max_capital": max_trading,
            "max_position": max_position,
            "max_positions": max_concurrent,
            "max_daily_snipes": max_daily,
            "max_daily_loss": max_daily_loss,
            "follow_pct": follow_pct,
            "min_reserve": self.min_reserve,
            "auto_scaled": True
        }
        
        # Log if balance changed significantly
        if abs(usdc_balance - self.last_balance) > 50:
            logger.info(f"[AUTO-SCALE] Balance: ${usdc_balance:,.2f}")
            logger.info(f"[AUTO-SCALE] Max per trade: ${max_position:,.2f}")
            logger.info(f"[AUTO-SCALE] Max positions: {max_concurrent}")
            logger.info(f"[AUTO-SCALE] Daily limit: {max_daily} trades")
            logger.info(f"[AUTO-SCALE] Follow %: {follow_pct*100:.1f}%")
            self.last_balance = usdc_balance
        
        self.scaled_limits = limits
        return limits
    
    def get_limits(self) -> Dict:
        """Get current scaled limits"""
        return self.scaled_limits


def get_scaled_config(config, usdc_balance: float):
    """
    Get config with auto-scaled values based on balance
    
    Usage in your trading code:
        from auto_scaling import get_scaled_config
        
        balance = get_wallet_balance()
        scaled = get_scaled_config(CONFIG, balance)
        
        max_position = scaled['max_position']  # Auto-scaled!
    """
    scaler = AutoScalingManager(config)
    return scaler.calculate_limits(usdc_balance)


# ============================================================================
# SCALING EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("""
====================================================================
           AUTO-SCALING DEMONSTRATION
====================================================================
""")
    
    class MockConfig:
        ENABLE_AUTO_SCALING = True
        CAPITAL_USAGE_PCT = 90
        POSITION_SIZE_PCT = 50
        MIN_USDC_RESERVE = 10
        MAX_TRADING_CAPITAL = 100
        MAX_POSITION_SIZE_USD = 50
        MAX_CONCURRENT_POSITIONS = 2
        MAX_DAILY_SNIPES = 5
        MAX_DAILY_LOSS_USD = 30
        FOLLOW_PERCENTAGE = 0.01
    
    config = MockConfig()
    scaler = AutoScalingManager(config)
    
    # Test different balance levels
    test_balances = [100, 200, 500, 1000, 2000, 5000]
    
    print("\nHow your limits scale as you add funds:\n")
    print("Balance | Max/Trade | Positions | Daily Trades | Follow % | Daily Loss")
    print("-" * 80)
    
    for balance in test_balances:
        limits = scaler.calculate_limits(balance)
        print(f"${balance:>6,.0f}  | ${limits['max_position']:>8,.0f}  | "
              f"{limits['max_positions']:>9} | {limits['max_daily_snipes']:>12} | "
              f"{limits['follow_pct']*100:>7.1f}% | ${limits['max_daily_loss']:>10,.0f}")
    
    print()
    print("="*80)
    print("As you add funds, the system automatically:")
    print("  - Increases position sizes")
    print("  - Allows more concurrent positions")
    print("  - Increases daily trade limits")
    print("  - Scales follow percentage")
    print("  - Adjusts risk limits")
    print()
    print("NO MANUAL CONFIG UPDATES NEEDED!")
    print("="*80)

