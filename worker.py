# worker.py (FINAL CORRECTED CODE)

import os
from redis import Redis
from rq import Worker, connections # CORRECTED: Import 'connections' module instead of 'Connection' class
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis connection details
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if __name__ == '__main__':
    try:
        redis_conn = Redis.from_url(REDIS_URL)
        
        # CORRECTED USAGE: Access the Connection class inside the connections module
        with connections.Connection(redis_conn): 
            # Worker processes tasks from the 'default' queue
            worker = Worker(['default'], connection=redis_conn)
            print("RQ Worker started. Listening for tasks...")
            worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        exit(1)
