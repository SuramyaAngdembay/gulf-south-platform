#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p nginx/ssl/live/$DOMAIN_NAME

# Generate SSL certificate using Let's Encrypt
echo "Setting up SSL certificate..."
docker run --rm -it \
    -v "$(pwd)/nginx/ssl:/etc/letsencrypt" \
    -v "$(pwd)/nginx/www:/var/www" \
    certbot/certbot certonly \
    --webroot -w /var/www \
    --email your-email@example.com \
    -d $DOMAIN_NAME \
    --agree-tos \
    --non-interactive

# Build and start the containers
echo "Building and starting containers..."
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose exec backend alembic upgrade head

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo "Deployment completed successfully!"
echo "Your application is now running at https://$DOMAIN_NAME" 