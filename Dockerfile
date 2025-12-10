# Use an official Python runtime as a parent image
# python:3.13-slim-buster is a small, stable, and Debian-based base image.
FROM python:3.13-slim-buster

# Environment variables for best Python practices in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for WeasyPrint
# This is the crucial step to fix the 'gobject-2.0-0' OSError.
# It installs the GTK/Cairo/Pango libraries needed for rendering PDFs.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libharfbuzz-icu0 \
        libpangocairo-1.0-0 \
        libgirepository-1.0-1 \
        libgobject-2.0-0 \
        libcairo2 \
        libgdk-pixbuf2.0-0 \
        # Dependencies for compiling Python extensions if needed
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the application
WORKDIR /app

# Create a virtual environment and set it on the PATH
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run your application when the container starts
# IMPORTANT: You must replace 'python app.py' with the actual command 
# that starts your web application (e.g., Gunicorn command).
CMD ["python", "app.py"]
