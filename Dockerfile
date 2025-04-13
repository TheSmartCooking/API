# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set a specific working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends openssl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create a non-root user and set permissions for the /app directory
RUN adduser --disabled-password --gecos '' apiuser && chown -R apiuser /app
USER apiuser

# Expose the Flask port
EXPOSE 5000

# Add health check for the container
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:5000/ || exit 1

ENTRYPOINT ["python3", "app.py"]
