# Use official Python 3.13 slim image based on Debian Bookworm (current in 2025)
FROM python:3.13-slim-bookworm

# Environment variables for best Python practices in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install exact same system dependencies you had before (they still exist on Bookworm)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libharfbuzz-icu0 \
        libpangocairo-1.0-0 \
        libgirepository-1.0-1 \
        libgobject-2.0-0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Replace this with your real start command!
# Examples:
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "app.py"]
