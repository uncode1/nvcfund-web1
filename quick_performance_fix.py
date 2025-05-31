#!/usr/bin/env python3
"""
Quick Performance Fix - Apply immediately
"""
import os
import sys

# Set performance environment variables
os.environ['REDUCE_LOGGING'] = '1'
os.environ['SKIP_BLOCKCHAIN_INIT'] = '1' 
os.environ['CACHE_ENABLED'] = '1'
os.environ['FLASK_ENV'] = 'production'

# Disable debug logging that's slowing down the system
import logging
logging.getLogger('web3').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('blockchain').setLevel(logging.ERROR)
logging.getLogger('cache_utils').setLevel(logging.ERROR)
logging.getLogger('rlp.codec').setLevel(logging.ERROR)

print("Performance optimizations applied - system should run faster now")