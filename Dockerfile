# FROM python:3.9-slim
FROM python:3.9-slim

# Copy the application
COPY app/ ./app/

# WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Add the app directory to Python path
# ENV PYTHONPATH=/app

# Create a non-root user
# RUN useradd -m appuser
# RUN chown -R appuser:appuser /app
# USER appuser

# Expose the port the app runs on
# EXPOSE 8000

# Command to run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
