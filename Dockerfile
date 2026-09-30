FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Generate test data on container build if not already present
RUN python generate_test_data.py

EXPOSE 8080

# Default execution starts the TenderPulse AI web server
CMD ["python", "app.py"]
