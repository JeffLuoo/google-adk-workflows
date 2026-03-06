FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any are needed for adk, but requirements.txt should be enough 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all agent code
COPY . .

# Expose the default adk web port
EXPOSE 8080

# Run adk web and bind to 0.0.0.0 so it's accessible outside the container
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]
