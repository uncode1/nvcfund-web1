"""
Critical Performance Optimizations for NVC Banking Platform
"""
import logging
import os
from functools import lru_cache

# Disable excessive debug logging
logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('blockchain').setLevel(logging.WARNING)
logging.getLogger('cache_utils').setLevel(logging.WARNING)

# Optimize database queries
def optimize_database_performance():
    """Optimize database connection and query performance"""
    from app import app, db
    
    with app.app_context():
        # Optimize connection pool settings
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 5,
            "pool_pre_ping": False,  # Disable ping checks for speed
            "pool_recycle": 3600,
            "max_overflow": 0,
            "pool_timeout": 30
        }
        
        # Create indexes for frequently queried tables
        try:
            db.engine.execute("CREATE INDEX IF NOT EXISTS idx_bank_account_holder ON bank_account(account_holder_id);")
            db.engine.execute("CREATE INDEX IF NOT EXISTS idx_currency_exchange_from ON currency_exchange_rate(from_currency);")
            db.engine.execute("CREATE INDEX IF NOT EXISTS idx_currency_exchange_to ON currency_exchange_rate(to_currency);")
            print("Database indexes optimized")
        except Exception as e:
            print(f"Index creation skipped: {e}")

# Cache frequently accessed data
@lru_cache(maxsize=128)
def get_cached_exchange_rates():
    """Cache exchange rates to avoid repeated database queries"""
    from account_holder_models import CurrencyExchangeRate, db
    try:
        rates = CurrencyExchangeRate.query.filter_by(is_active=True).all()
        return {f"{rate.from_currency.value}_{rate.to_currency.value}": rate.rate for rate in rates}
    except:
        return {}

# Disable unnecessary blockchain connections during startup
def optimize_blockchain_connections():
    """Optimize blockchain connections for faster startup"""
    if os.environ.get('SKIP_BLOCKCHAIN_INIT'):
        return False
    return True

# Reduce currency rate update frequency
def optimize_currency_updates():
    """Reduce frequency of currency rate updates"""
    # Only update rates every 30 minutes instead of constantly
    import time
    last_update_file = '/tmp/last_currency_update'
    
    try:
        if os.path.exists(last_update_file):
            last_update = float(open(last_update_file).read())
            if time.time() - last_update < 1800:  # 30 minutes
                return False
    except:
        pass
    
    # Update timestamp
    with open(last_update_file, 'w') as f:
        f.write(str(time.time()))
    return True

# Apply all optimizations
def apply_performance_fixes():
    """Apply all critical performance optimizations"""
    optimize_database_performance()
    
    # Set environment variables for reduced logging
    os.environ['SKIP_BLOCKCHAIN_INIT'] = '1'
    os.environ['REDUCE_LOGGING'] = '1'
    os.environ['CACHE_ENABLED'] = '1'
    
    print("Performance optimizations applied successfully")

if __name__ == "__main__":
    apply_performance_fixes()