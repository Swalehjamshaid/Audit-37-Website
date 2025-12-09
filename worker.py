# worker.py

import os
from redis import Redis
from rq import Worker, Connection
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

if __name__ == '__main__':
    try:
        redis_conn = Redis.from_url(REDIS_URL)
        
        with Connection(redis_conn):
            worker = Worker(['default'], connection=redis_conn)
            print("RQ Worker started. Listening for tasks...")
            worker.work() 
            
    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        exit(1)
