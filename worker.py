# worker.py
import os
from redis import Redis
from rq import Queue, Worker
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

# This works locally (Docker) AND in production (Render/Railway/Fly)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

if __name__ == "__main__":
    try:
        redis_conn = Redis.from_url(REDIS_URL)

        # Listen to default queue (add more like 'high', 'low' if needed)
        queues = [Queue("default", connection=redis_conn)]
        # Or listen to ALL queues: queues = Queue.all(connection=redis_conn)

        worker = Worker(queues, connection=redis_conn)

        print("RQ Worker started successfully!")
        print(f"Connected to Redis: {REDIS_URL.split('@')[-1] if '@' in REDIS_URL else REDIS_URL}")
        print("Listening on queues: default")

        worker.work(with_scheduler=False)  # Change to True only if using rq-scheduler in same process

    except Exception as e:
        print(f"Failed to start RQ Worker: {e}")
        raise
