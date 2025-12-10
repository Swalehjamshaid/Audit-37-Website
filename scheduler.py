# scheduler.py — Railway-proof version (2025)
import os
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

# --- CRITICAL: Fix Python path for Railway ---
# Railway runs from /app, your code is in /app/audit37website (or similar)
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can safely import Django stuff
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit37website.settings')
import django
django.setup()

from app import send_scheduled_report
from accounts.models import User  # adjust if your User model is elsewhere


def queue_daily_reports():
    """Run daily: find users with scheduled_website and enqueue report jobs"""
    from django.db import connection
    with connection.cursor():  # forces DB connection in thread
        users = User.objects.filter(scheduled_website__isnull=False).exclude(scheduled_website='')
        
        if not users:
            print(f"[{datetime.utcnow()}] Scheduler: No scheduled reports today.")
            return
            
        redis_conn = Redis.from_url(os.getenv('REDIS_URL'))
        queue = Queue(connection=redis_conn)
        
        print(f"[{datetime.utcnow()}] Scheduler: Queuing {users.count()} daily reports...")
        
        for user in users:
            if user.scheduled_email and user.scheduled_website:
                queue.enqueue(
                    send_scheduled_report,
                    user.id,
                    user.scheduled_website,
                    user.scheduled_email,
                    job_timeout='30m'
                )
                print(f"  → Queued for {user.email} | {user.scheduled_website}")


if __name__ == '__main__':
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        print("FATAL: REDIS_URL environment variable is missing!")
        exit(1)

    try:
        conn = Redis.from_url(redis_url)
        conn.ping()
        print("Connected to Redis successfully")

        scheduler = Scheduler(connection=conn)
        scheduler.empty()  # clear old jobs on restart

        # Run 30 seconds after startup, then every 24 hours
        scheduler.schedule(
            scheduled_time=datetime.utcnow() + timedelta(seconds=30),
            func=queue_daily_reports,
            interval=86400,  # 24 hours in seconds
            repeat=None
        )

        print("RQ Scheduler started — daily reports active every 24h")
        scheduler.run(burst=False)  # burst=False = run forever

    except Exception as e:
        print(f"FATAL: Scheduler crashed → {e}")
        raise
