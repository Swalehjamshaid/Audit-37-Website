# worker.py (Updated to fix RQ Import Error)

import os
from redis import Redis
from rq import Worker, connections # CORRECTED: Changed 'Connection' to 'connections'
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis connection details
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if __name__ == '__main__':
    try:
        redis_conn = Redis.from_url(REDIS_URL)
        
        # CORRECTED USAGE: Accessing the Connection object through the connections module
        with connections.Connection(redis_conn): 
            # Worker processes tasks from the 'default' queue
            worker = Worker(['default'], connection=redis_conn)
            print("RQ Worker started. Listening for tasks...")
            worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        exit(1)
