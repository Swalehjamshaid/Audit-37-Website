# scheduler.py (FINAL, ORGANIZED, RAILWAY-READY CODE)

import os
import sys
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue, Connection
from rq_scheduler import Scheduler
from dotenv import load_dotenv

# --- Ensure Path is Correct ---
# We use absolute imports (from app import ...) so the root path must be included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# --- Absolute Imports ---
# Import the application instance and models from your app.py
from app import app, db, User 
# Import the task function from your tasks.py
from tasks import send_scheduled_report 

# --- Scheduler Logic ---

def queue_daily_reports():
    """
    Function executed by the RQ Scheduler daily.
    It checks the database for users who have scheduled reports
    and queues a task for each of them.
    """
    # CRITICAL: Must use the app instance's context to access the database
    with app.app_context():
        # Find all users who have a scheduled website set
        scheduled_users = User.query.filter(User.scheduled_website.isnot(None)).all()
        
        if not scheduled_users:
            print(f"Scheduler: No active reports scheduled today.")
            return

        # Connect to Redis and initialize the Queue
        redis_conn = Redis.from_url(os.getenv('REDIS_URL'))
        task_queue = Queue(connection=redis_conn)
        
        print(f"Scheduler: Queuing {len(scheduled_users)} daily reports...")
        
        for user in scheduled_users:
            # Enqueue the report generation task for each user
            task_queue.enqueue(
                send_scheduled_report, 
                user.id, 
                user.scheduled_website, 
                user.scheduled_email,
                job_timeout='30m' # Important: give enough time for PDF/Email
            )
            print(f"  -> Queued report for user: {user.email}")


if __name__ == '__main__':
    load_dotenv()
    REDIS_URL = os.getenv('REDIS_URL')
    
    try:
        if not REDIS_URL:
            # Raise an error if the key environment variable is missing
            raise EnvironmentError("FATAL: REDIS_URL environment variable is missing!")

        redis_conn = Redis.from_url(REDIS_URL)
        redis_conn.ping()
        print("Successfully connected and authenticated with Redis.")
        
        # Initialize the RQ Scheduler
        with Connection(redis_conn):
            scheduler = Scheduler(connection=redis_conn)
            
            # Clear any existing jobs to ensure clean restart on deployment
            scheduler.empty()

            daily_interval = timedelta(hours=24)
            
            # Schedule the job. Run 10 seconds after startup, then every 24 hours.
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
