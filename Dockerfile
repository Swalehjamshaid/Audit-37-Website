# Start with a stable, slim Python base image
FROM python:3.13-slim-bookworm

# -----------------
# System Dependencies for WeasyPrint and Psycopg
# -----------------
# This single RUN command installs all necessary system libraries:
# - WeasyPrint dependencies (libpango, libcairo, etc.)
# - PostgreSQL client libraries (libpq-dev) and the compiler (gcc) for psycopg
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libharfbuzz0b \
        libpangocairo-1.0-0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
        libcairo-gobject2 \
        libgirepository-1.0-1 \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# -----------------
# Python Dependencies
# -----------------
# Copy the requirements file first to leverage Docker caching (if requirements.txt hasn't changed)
COPY requirements.txt .

# Install all Python packages, including the new 'rq-scheduler'
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# -----------------
# Expose Port and Define Startup Command
# -----------------
# Railway typically handles the port, but exposing it is good practice
EXPOSE 8080

# The startup command is crucial. We use a shell script entrypoint 
# to run BOTH gunicorn (your web server) AND rq-scheduler (your worker/scheduler)
# or you run them as separate services in Railway.

# --- OPTION 1: Running Gunicorn (Web App) Only ---
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]

# --- OPTION 2: Using a custom entrypoint to start multiple processes (Recommended for one container) ---
# Create a script to run both. Name it `start.sh`.
# The final CMD will execute this script. 
#
# NOTE: Railway recommends running separate services for your web app and scheduler/worker,
# but if you must run both in one container, a tool like 'supervisord' or a simple shell script is needed. 

# *** If running Gunicorn in one container and Scheduler in another (the Railway way): ***
# The Dockerfile for your **Web App** service should end with:
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]

# The Dockerfile for your **Scheduler** service should end with:
# CMD ["rq-scheduler"]

# --- If you want a single service that runs both (less common on Railway): ---
# Assume your Flask app is in `wsgi.py` and the Flask instance is named `app`
# This line runs Gunicorn on port 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
