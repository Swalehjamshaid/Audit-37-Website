# scheduler.py (FINAL, ORGANIZED, RAILWAY-READY CODE)

import os
import sys
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue, Connection
from rq_scheduler import Scheduler
from dotenv import load_dotenv

# --- Absolute Imports ---
from app import app, db, User 
from tasks import send_scheduled_report 

# --- Scheduler Logic ---

def queue_daily_reports():
    """Queues a task for each user with a scheduled report."""
    with app.app_context():
        scheduled_users = User.query.filter(User.scheduled_website.isnot(None)).all()
        
        if not scheduled_users:
            print(f"Scheduler: No active reports scheduled today.")
            return

        redis_conn = Redis.from_url(os.getenv('REDIS_URL'))
        task_queue = Queue(connection=redis_conn)
        
        print(f"Scheduler: Queuing {len(scheduled_users)} daily reports...")
        
        for user in scheduled_users:
            task_queue.enqueue(
                send_scheduled_report, 
                user.id, 
                user.scheduled_website, 
                user.scheduled_email,
                job_timeout='30m'
            )
            print(f"  -> Queued report for user: {user.email}")


if __name__ == '__main__':
    load_dotenv()
    REDIS_URL = os.getenv('REDIS_URL')
    
    try:
        if not REDIS_URL:
            raise EnvironmentError("FATAL: REDIS_URL environment variable is missing!")

        redis_conn = Redis.from_url(REDIS_URL)
        redis_conn.ping()
        print("Successfully connected and authenticated with Redis.")
        
        with Connection(redis_conn):
            scheduler = Scheduler(connection=redis_conn)
            scheduler.empty()

            daily_interval = timedelta(hours=24)
            
            scheduler.schedule(
                scheduled_time=datetime.utcnow() + timedelta(seconds=10),
                func=queue_daily_reports,
                interval=daily_interval,
                repeat=None
            )
            
            print("RQ Scheduler started. Daily report queuing job is active.")
            scheduler.run()
            
    except Exception as e:
        print(f"FATAL: RQ Scheduler failed to start. Error: {e}")
        sys.exit(1)
