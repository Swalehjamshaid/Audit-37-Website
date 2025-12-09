# worker.py (2025-compatible version - NO Connection import needed)
import os
from redis import Redis
from rq import Worker, Queue
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# Get Redis URL (fallback to local Redis if not set)
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

if __name__ == '__main__':
    try:
        # Create Redis connection
        redis_conn = Redis.from_url(REDIS_URL)

        # Option 1: Listen to specific queue(s) - RECOMMENDED
        queues = [Queue('default', connection=redis_conn)]
        # Add more queues if needed:
        # queues = [Queue('default', connection=redis_conn), Queue('high', connection=redis_conn)]

        # Option 2: Or listen to ALL existing queues (useful in most cases)
        # queues = Queue.all(connection=redis_conn)

        worker = Worker(queues, connection=redis_conn)

        print("RQ Worker started successfully! Listening on queues: default")
        worker.work(with_scheduler=False)  # set True only if you need the RQ Scheduler

    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        raise  # or exit(1)
