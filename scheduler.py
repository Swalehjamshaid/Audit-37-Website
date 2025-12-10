# scheduler.py — FINAL Railway-proof version (December 2025)
import os
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

# --- CRITICAL: Railway always mounts code at /app ---
import sys
project_root = "/app"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit37website.settings')
import django
django.setup()

# Now safe to import your app and models
from app import send_scheduled_report
from accounts.models import User  # ← change only if your User model is somewhere else


def queue_daily_reports():
    """Runs daily → finds users with scheduled reports → enqueues PDF jobs"""
    from django.db import connection
    with connection.cursor():  # ensures DB is ready
        users = User.objects.filter(
            scheduled_website__isnull=False
        ).exclude(
            scheduled_website=''
        ).select_related('profile')

        if not users.exists():
            print(f"[{datetime.utcnow()}] Scheduler: No scheduled reports today.")
            return

        redis_conn = Redis.from_url(os.getenv('REDIS_URL'))
        queue = Queue(connection=redis_conn)

        print(f"[{datetime.utcnow()}] Scheduler: Queuing {users.count()} daily report(s)...")

        for user in users:
            if user.scheduled_email and user.scheduled_website:
                queue.enqueue(
                    send_scheduled_report,
                    user.id,
                    user.scheduled_website,
                    user.scheduled_email,
                    job_timeout='30m'
                )
                print(f"  → Queued: {user.email} | {user.scheduled_website}")
            else:
                print(f"  → Skipped (missing data): {user.email}")


if __name__ == '__main__':
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        print("FATAL: REDIS_URL environment variable missing!")
        exit(1)

    try:
        conn = Redis.from_url(redis_url)
        conn.ping()
        print("Successfully connected to Redis")

        scheduler = Scheduler(connection=conn)
        scheduler.empty()  # clear old jobs on restart

        # First run in 30 seconds, then every 24 hours
        scheduler.schedule(
            scheduled_time=datetime.utcnow() + timedelta(seconds=30),
            func=queue_daily_reports,
            interval=86400,   # 24 hours
            repeat=None
        )

        print("RQ Scheduler started — daily reports active every 24h")
        scheduler.run(burst=False)  # runs forever

    except Exception as e:
        print(f"FATAL: Scheduler crashed → {e}")
        raise
