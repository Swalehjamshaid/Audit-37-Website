# Use the Python 3.13 slim image
FROM python:3.13-slim-bookworm

# ----------------------------------------------------
# 1. Install System Dependencies (for WeasyPrint/psycopg)
# ----------------------------------------------------
# This installs necessary libraries (libpango, libcairo, etc.) for WeasyPrint 
# and the PostgreSQL client libraries (libpq-dev) and compiler (gcc) for psycopg
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

# Set the working directory
WORKDIR /app

# ----------------------------------------------------
# 2. Install Python Dependencies
# ----------------------------------------------------
# Copy requirements.txt and install packages
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# 3. Copy Application Code
# ----------------------------------------------------
COPY . .

# ----------------------------------------------------
# 4. Define Default Command (for general use)
# ----------------------------------------------------
# Set a default command. This can be overridden by Railway service settings.
# Using 'app:app' as a placeholder for <file_name>:<app_variable>
# Adjust this part based on where your Flask app is defined (e.g., myapp:app or run:app)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
