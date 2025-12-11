# Official Python 3.13 on Debian Bookworm – works perfectly on Railway
FROM python:3.13-slim-bookworm

# Best practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install WeasyPrint + PostgreSQL system dependencies
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

WORKDIR /app

# Virtual environment (optional but clean)
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Production-ready start command using Gunicorn + auto $PORT from Railway
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 app:app
