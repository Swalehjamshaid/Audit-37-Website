# ─────────────────────────────────────────────────────────────
# FINAL WORKING DOCKERFILE – Python 3.13 + Railway (Dec 2025)
# ─────────────────────────────────────────────────────────────
FROM python:3.13-slim-bookworm

# Best practices for production containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for WeasyPrint + PostgreSQL driver
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

# Set work directory
WORKDIR /app

# Optional: use a virtual env (cleaner, but not required)
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose nothing (Railway ignores it anyway)

# Start command – uses Railway's $PORT automatically
CMD exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 180 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
