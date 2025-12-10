# scheduler.py
import os
from datetime import datetime, timedelta
from redis import Redis
from rq_scheduler import Scheduler
import sys
sys.path.insert(0, "/app")
os.environ.setdefault('FLASK_APP', 'app.py')
from tasks import send_scheduled_report
from app import db, User

def queue_daily_reports():
    from flask import current_app
    with current_app.app_context():
        users = User.query.filter(User.scheduled_website.isnot(None), User.scheduled_website != '').all()
        if users:
            from rq import Queue
            q = Queue(connection=Redis.from_url(os.getenv('REDIS_URL')))
            for user in users:
                if user.scheduled_email:
                    q.enqueue(send_scheduled_report, user.id, user.scheduled_website, user.scheduled_email)

if __name__ == '__main__':
    scheduler = Scheduler(connection=Redis.from_url(os.getenv('REDIS_URL')))
    scheduler.schedule(
        scheduled_time=datetime.utcnow() + timedelta(seconds=30),
        func=queue_daily_reports,
        interval=86400,
        repeat=None
    )
    print("Scheduler running...")
    scheduler.run(burst=False)
