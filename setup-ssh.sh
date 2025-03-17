#!/bin/bash

# Exit on error
set -e

# Check if server IP is provided
if [ -z "$1" ]; then
    echo "Usage: ./setup-ssh.sh <server_ip>"
    echo "Example: ./setup-ssh.sh 123.456.789.0"
    exit 1
fi

SERVER_IP=$1

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if ssh-copy-id is installed
if ! command_exists ssh-copy-id; then
    echo "Installing ssh-copy-id..."
    if command_exists apt-get; then
        sudo apt-get install -y openssh-client
    elif command_exists yum; then
        sudo yum install -y openssh-clients
    else
        echo "Could not install ssh-copy-id. Please install it manually."
        exit 1
    fi
fi

# Copy SSH key to server
echo "Copying SSH key to server..."
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@$SERVER_IP

# Test SSH connection
echo "Testing SSH connection..."
ssh -i ~/.ssh/id_ed25519 root@$SERVER_IP "echo 'SSH connection successful!'"

echo "SSH setup completed successfully!"
echo "You can now connect to your server using:"
echo "ssh root@$SERVER_IP" 