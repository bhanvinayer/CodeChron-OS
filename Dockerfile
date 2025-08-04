# Use an official Python base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y unzip curl && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose the port (Railway/Render will set $PORT)
EXPOSE 3000

# Run Reflex, binding to the correct port and host
CMD ["reflex", "run", "--env", "prod", "--backend-port", "${PORT}", "--backend-host", "0.0.0.0"]
