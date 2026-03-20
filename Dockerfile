# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies for tkinter and GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set display for GUI applications
ENV DISPLAY=:0

# Run the application
CMD ["python", "graph.py"]
