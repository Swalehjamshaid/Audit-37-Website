# worker.py (FINAL CORRECTED CODE)

import os
from redis import Redis
from rq import Worker, Connection # Import Connection directly from rq package
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis connection details
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if __name__ == '__main__':
    try:
        redis_conn = Redis.from_url(REDIS_URL)
        
        # Using the standard Connection class imported from rq
        with Connection(redis_conn): 
            # Worker processes tasks from the 'default' queue
            worker = Worker(['default'], connection=redis_conn)
            print("RQ Worker started. Listening for tasks...")
            worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        exit(1)
