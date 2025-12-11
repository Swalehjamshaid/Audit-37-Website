import os
import json
import random
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from redis import Redis
from rq import Queue
from weasyprint import HTML, CSS

load_dotenv()
app = Flask(__name__)

# Database
DB_URL = os.getenv("DATABASE_URL")
if DB_URL and DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL or 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email
app.config.update({
    'MAIL_SERVER': os.getenv('MAIL_SERVER'),
    'MAIL_PORT': int(os.getenv('MAIL_PORT') or 587),
    'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER')
})

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))

# Redis queue
try:
    redis_conn = Redis.from_url(os.getenv('REDIS_URL') or os.getenv('REDIS_RAILWAY', 'redis://localhost:6379'))
    task_queue = Queue(connection=redis_conn)
except:
    task_queue = None

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'warning')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrap

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    scheduled_website = db.Column(db.String(255))
    scheduled_email = db.Column(db.String(120))
    reports = db.relationship('AuditReport', backref='user', lazy=True)

class AuditReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_url = db.Column(db.String(255), nullable=False)
    date_audited = db.Column(db.DateTime, default=datetime.utcnow)
    metrics_json = db.Column(db.Text, nullable=False)
    performance_score = db.Column(db.Integer, default=0)
    security_score = db.Column(db.Integer, default=0)
    accessibility_score = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 37 Metrics Engine
class AuditService:
    METRICS = { ... }  # ← your full 37 metrics are already here (same as before)

    @staticmethod
    def run_audit(url):
        # same code you already have – returns 37 fake results
        ...

# Admin auto-create + background task functions (same as before)
def create_admin_user(): ... 
def generate_pdf_content(...): ...
def send_scheduled_report(...): ...

# All your routes (home, login, dashboard, run_audit, pdf, schedule, admin, etc.) – unchanged

# Startup
with app.app_context():
    create_admin_user()

# NO app.run() → Gunicorn runs this file
