#!/bin/bash

# Exit on error
set -e

# Server details
SERVER_IP="137.184.227.95"
USERNAME="suramya"

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

# Copy SSH key to root user
echo "Copying SSH key to root user..."
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@$SERVER_IP

# Create regular user and set up SSH
echo "Setting up regular user..."
ssh root@$SERVER_IP "adduser $USERNAME && usermod -aG sudo $USERNAME && mkdir -p /home/$USERNAME/.ssh && cp /root/.ssh/authorized_keys /home/$USERNAME/.ssh/ && chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh"

# Copy SSH key to regular user
echo "Copying SSH key to regular user..."
ssh-copy-id -i ~/.ssh/id_ed25519.pub $USERNAME@$SERVER_IP

# Update SSH config
echo "Updating SSH config..."
if [ ! -f ~/.ssh/config ]; then
    touch ~/.ssh/config
fi

# Add or update the host configuration
if grep -q "Host gulf-south" ~/.ssh/config; then
    sed -i "s|HostName.*|HostName $SERVER_IP|" ~/.ssh/config
else
    echo -e "\nHost gulf-south\n    HostName $SERVER_IP\n    User $USERNAME\n    IdentityFile ~/.ssh/id_ed25519" >> ~/.ssh/config
fi

# Set proper permissions
chmod 600 ~/.ssh/config

# Test connection with new user
echo "Testing connection with new user..."
ssh $USERNAME@$SERVER_IP "echo 'SSH connection successful!'"

echo "Droplet setup completed successfully!"
echo "You can now connect to your server using:"
echo "ssh gulf-south" 