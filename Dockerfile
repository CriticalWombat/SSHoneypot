FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tor nmap netcat gcc libffi-dev libssl-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy application code
COPY app/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir aiohttp

# Expose port for SSH wrapper
EXPOSE 22

# Start Tor in the background and run the app
CMD tor & python main.py
