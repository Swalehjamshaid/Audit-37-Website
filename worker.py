# worker.py (FINAL CORRECTED CODE)

import os
from redis import Redis
from rq import Worker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis connection details
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if __name__ == '__main__':
    try:
        # Use Redis.from_url to handle parsing the full URL (including auth/password)
        redis_conn = Redis.from_url(REDIS_URL) 
        
        # Check connection health to ensure auth succeeds before starting worker
        redis_conn.ping() 
        print("Successfully connected and authenticated with Redis.")

        # Worker processes tasks from the 'default' queue
        worker = Worker(['default'], connection=redis_conn)
        print("RQ Worker started. Listening for tasks...")
        worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        # The AuthenticationError will be caught here
        exit(1)
