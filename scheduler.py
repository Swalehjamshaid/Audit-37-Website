# scheduler.py (2025-compatible version - NO Connection import needed)
import os
import sys
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from dotenv import load_dotenv

# Add the parent directory to the path to import app and its functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import the application context and task function from app.py
from app import app, db, User, send_scheduled_report

# Load environment variables from .env (if present)
load_dotenv()

# --- Scheduler Logic ---
def queue_daily_reports():
    """
    Function executed by the RQ Scheduler daily.
    It checks the database for users who have scheduled reports
    and queues a task for each of them.
    """
    with app.app_context():
        # Find all users who have a scheduled website set
        scheduled_users = User.query.filter(User.scheduled_website.isnot(None)).all()
       
        if not scheduled_users:
            print(f"Scheduler: No active reports scheduled today.")
            return

        REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        redis_conn = Redis.from_url(REDIS_URL)
        task_queue = Queue(connection=redis_conn)
       
        print(f"Scheduler: Queuing {len(scheduled_users)} daily reports...")
       
        for user in scheduled_users:
            # Enqueue the report generation task for each user
            task_queue.enqueue(
                send_scheduled_report,
                user.id,
                user.scheduled_website,
                user.scheduled_email,
                job_timeout='30m'
            )
            print(f" -> Queued report for user: {user.email}")

if __name__ == '__main__':
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    try:
        redis_conn = Redis.from_url(REDIS_URL)
       
        # Modern initialization: No Connection context manager needed
        scheduler = Scheduler(connection=redis_conn)
       
        # Clear any existing jobs to ensure clean restart
        scheduler.empty()

        # Define the daily interval
        daily_interval = timedelta(hours=24)
       
        # Schedule the job. Run immediately upon startup, then every 24 hours.
        scheduler.schedule(
            scheduled_time=datetime.utcnow() + timedelta(seconds=10),
            func=queue_daily_reports,
            interval=daily_interval,
            repeat=None
        )
       
        print("RQ Scheduler started successfully. Daily report queuing job is active.")
        scheduler.run()
           
    except Exception as e:
        print(f"FATAL: RQ Scheduler failed to start. Error: {e}")
        exit(1)
