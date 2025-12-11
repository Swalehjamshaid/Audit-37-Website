# worker.py (FINAL, ORGANIZED, RAILWAY-READY CODE)

import os
import sys
import redis
from rq import Worker, Connection
from dotenv import load_dotenv

# --- Absolute Imports ---
from app import app

load_dotenv()

if __name__ == '__main__':
    REDIS_URL = os.getenv('REDIS_URL')
    
    if not REDIS_URL:
        print("FATAL: REDIS_URL environment variable is missing! Worker cannot start.")
        sys.exit(1)
        
    try:
        redis_conn = redis.from_url(REDIS_URL)
        redis_conn.ping()
        
        with app.app_context():
            print("RQ Worker starting up...")
            worker = Worker(['default'], connection=redis_conn)
            worker.work()
            
    except Exception as e:
        print(f"FATAL: RQ Worker failed to start. Error: {e}")
        sys.exit(1)
