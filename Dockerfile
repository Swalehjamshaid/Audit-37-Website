# Use a Python base image with the necessary system libraries installed for WeasyPrint

# Choose the Python version from your requirements.txt
FROM python:3.13-slim-bookworm 

# Install system dependencies required by WeasyPrint (via aptPkgs in nixpacks.toml)
# We combine the most common WeasyPrint dependencies here for safety
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libxml2 \
    libxslt \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the application
WORKDIR /app

# CRITICAL FIX 1: Set the Python path permanently inside the container
# This ensures that 'app.py', 'tasks.py', etc., are always discoverable.
ENV PYTHONPATH=/app:$PYTHONPATH 

# Copy requirements file first to leverage Docker caching for pip install
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# CRITICAL FIX 2: Do NOT define a CMD or ENTRYPOINT here.
# We rely entirely on the Procfile to launch the multiple services (web, worker, scheduler).
