# worker.py (FINAL CORRECTED CODE)

import os
from redis import Redis
from rq import Worker, Connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis connection details
# CRITICAL FIX: REMOVED the fallback value 'redis://localhost:6379'
REDIS_URL = os.getenv('REDIS_URL') 

if __name__ == '__main__':
    try:
        # Check if the URL is missing before attempting connection
        if not REDIS_URL:
            # Raise an error if the essential variable is missing
            raise EnvironmentError("REDIS_URL environment variable is missing!")
            
        # Use Redis.from_url to handle parsing the full secure URL
        redis_conn = Redis.from_url(REDIS_URL) 
        
        # Check connection health to ensure auth succeeds
        redis_conn.ping() 
        print("Successfully connected and authenticated with Redis.")

        # Worker processes tasks from the 'default' queue
        with Connection(redis_conn): 
            worker = Worker(['default'], connection=redis_conn)
            print("RQ Worker started. Listening for tasks...")
            worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        exit(1)
