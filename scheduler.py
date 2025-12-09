# scheduler.py
import os
import sys
from datetime import datetime, timedelta

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from dotenv import load_dotenv

# Add project root to path (for importing app)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, User, send_scheduled_report

load_dotenv()

# Same Redis URL logic — works locally + production
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")


def queue_daily_reports():
    with app.app_context():
        users = User.query.filter(User.scheduled_website.isnot(None)).all()
        if not users:
            print("Scheduler: No users with scheduled reports.")
            return

        conn = Redis.from_url(REDIS_URL)
        q = Queue(connection=conn)

        print(f"Scheduler: Queuing reports for {len(users)} users...")
        for user in users:
            q.enqueue(
                send_scheduled_report,
                user.id,
                user.scheduled_website,
                user.scheduled_email,
                job_timeout="30m",
            )
            print(f"  → Queued for {user.email}")


if __name__ == "__main__":
    try:
        redis_conn = Redis.from_url(REDIS_URL)

        scheduler = Scheduler(connection=redis_conn)
        scheduler.empty()  # Clear old jobs on restart

        # Run 10 seconds after start, then every 24 hours
        scheduler.schedule(
            scheduled_time=datetime.utcnow() + timedelta(seconds=10),
            func=queue_daily_reports,
            interval=timedelta(hours=24).total_seconds(),
            repeat=None,
       аль
        print("RQ Scheduler started — daily reports scheduled!")
        print(f"Connected to Redis: {REDIS_URL.split('@')[-1] if '@' in REDIS_URL else REDIS_URL}")

        scheduler.run()

    except Exception as e:
        print(f"FATAL: Scheduler failed: {e}")
        raise
