# worker.py (REQUIRED for RQ Task Processing)

import os
import sys
import redis
from rq import Worker, Connection
from dotenv import load_dotenv

# Ensure the root directory is on the path to find 'app.py' and 'tasks.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import the Flask application instance to load configuration and modules
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
        
        # Workers must be run within the application context to access db/config/etc.
        with app.app_context():
            print("RQ Worker starting up...")
            # The worker listens on the 'default' queue (used by app.py and scheduler.py)
            worker = Worker(['default'], connection=redis_conn)
            worker.work()
            
    except Exception as e:
        print(f"FATAL: RQ Worker failed to start. Error: {e}")
        sys.exit(1)
