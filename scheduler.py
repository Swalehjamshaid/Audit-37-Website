# scheduler.py
import os
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

import sys
sys.path.insert(0, "/app")

os.environ.setdefault('FLASK_APP', 'app.py')
from tasks import send_scheduled_report
from app import db, User
from flask import current_app

def queue_daily_reports():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('app')
    with app.app_context():
        users = User.query.filter(User.scheduled_website.isnot(None)).all()
        if not users:
            print("No scheduled reports today.")
            return

        queue = Queue(connection=Redis.from_url(os.getenv('REDIS_URL')))
        for user in users:
            if user.scheduled_email and user.scheduled_website:
                queue.enqueue(
                    send_scheduled_report,
                    user.id,
                    user.scheduled_website,
                    user.scheduled_email,
                    job_timeout='30m'
                )
                print(f"Queued report for {user.email}")

if __name__ == '__main__':
    conn = Redis.from_url(os.getenv('REDIS_URL'))
    scheduler = Scheduler(connection=conn)
    scheduler.empty()
    scheduler.schedule(
        scheduled_time=datetime.utcnow() + timedelta(seconds=30),
        func=queue_daily_reports,
        interval=86400,
        repeat=None
    )
    print("Scheduler started — running daily")
    scheduler.run(burst=False)
