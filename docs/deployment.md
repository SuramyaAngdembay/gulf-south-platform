# Deployment Guide

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Node.js 16 or higher
- Nginx (for production)
- SSL certificate (for HTTPS)

## Production Environment Setup

### 1. Server Requirements

- Ubuntu 20.04 LTS or higher
- 2GB RAM minimum
- 20GB storage minimum
- Public IP address
- Domain name (optional)

### 2. System Updates

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Install Required Software

```bash
# Install Python and pip
sudo apt install python3.8 python3.8-venv python3-pip -y

# Install MySQL
sudo apt install mysql-server -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs -y

# Install Nginx
sudo apt install nginx -y
```

### 4. Configure MySQL

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p

CREATE DATABASE gulf_south_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gulf_south_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON gulf_south_platform.* TO 'gulf_south_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Backend Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/gulf-south-platform.git
cd gulf-south-platform/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with production settings
nano .env

# Run database migrations
alembic upgrade head

# Install Gunicorn
pip install gunicorn

# Create systemd service file
sudo nano /etc/systemd/system/gulf-south.service
```

Add the following content to the service file:
```ini
[Unit]
Description=Gulf South Platform Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gulf-south-platform/backend
Environment="PATH=/var/www/gulf-south-platform/backend/venv/bin"
ExecStart=/var/www/gulf-south-platform/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl start gulf-south
sudo systemctl enable gulf-south
```

### 6. Frontend Deployment

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/gulf-south
```

Add the following Nginx configuration:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # Frontend
    location / {
        root /var/www/gulf-south-platform/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/gulf-south /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your_domain.com
```

### 8. Security Considerations

1. Firewall Configuration:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. Regular Updates:
```bash
# Create update script
sudo nano /usr/local/bin/update-gulf-south.sh
```

Add the following content:
```bash
#!/bin/bash
cd /var/www/gulf-south-platform
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart gulf-south
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
```

Make it executable:
```bash
sudo chmod +x /usr/local/bin/update-gulf-south.sh
```

3. Backup Script:
```bash
sudo nano /usr/local/bin/backup-gulf-south.sh
```

Add the following content:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/gulf-south"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup database
mysqldump -u gulf_south_user -p gulf_south_platform > $BACKUP_DIR/db_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /var/www/gulf-south-platform

# Keep only last 7 backups
find $BACKUP_DIR -type f -mtime +7 -delete
```

Make it executable:
```bash
sudo chmod +x /usr/local/bin/backup-gulf-south.sh
```

### 9. Monitoring

1. Install monitoring tools:
```bash
sudo apt install prometheus node-exporter -y
```

2. Configure Prometheus:
```bash
sudo nano /etc/prometheus/prometheus.yml
```

Add the following configuration:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

3. Start monitoring services:
```bash
sudo systemctl start prometheus node-exporter
sudo systemctl enable prometheus node-exporter
```

## Maintenance

### Regular Tasks

1. Database Backup:
```bash
# Add to crontab
0 2 * * * /usr/local/bin/backup-gulf-south.sh
```

2. System Updates:
```bash
# Add to crontab
0 4 * * * /usr/local/bin/update-gulf-south.sh
```

3. Log Rotation:
```bash
sudo nano /etc/logrotate.d/gulf-south
```

Add the following configuration:
```
/var/log/gulf-south/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
```

### Troubleshooting

1. Check service status:
```bash
sudo systemctl status gulf-south
sudo systemctl status nginx
```

2. Check logs:
```bash
sudo journalctl -u gulf-south
sudo tail -f /var/log/nginx/error.log
```

3. Database issues:
```bash
sudo mysql -u gulf_south_user -p
SHOW PROCESSLIST;
```

## Scaling

### Horizontal Scaling

1. Add more application servers
2. Configure load balancer
3. Use database replication

### Vertical Scaling

1. Increase server resources
2. Optimize database queries
3. Implement caching

## Disaster Recovery

1. Regular backups
2. Point-in-time recovery
3. Failover procedures 