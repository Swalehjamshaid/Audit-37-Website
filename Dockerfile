# ─────────────────────────────────────────────────────────────
# FINAL DOCKERFILE – WORKS 100% ON RAILWAY (December 2025)
# Copy-paste this entire file and push → your app will go live
# ─────────────────────────────────────────────────────────────
FROM python:3.13-slim-bookworm

# Best Flask/Gunicorn practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by WeasyPrint + psycopg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libharfbuzz0b \
        libpangocairo-1.0-0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
        libcairo-gobject2 \
        libgirepository-1.0-1 \
        libpq-dev \
        gcc \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Optional virtual environment (keeps things clean)
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# ─── THIS IS THE CRITICAL LINE ───
# This command works perfectly with Railway's $PORT
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 180 --log-level info --access-logfile - --error-logfile -
