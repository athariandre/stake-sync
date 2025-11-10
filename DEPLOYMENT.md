# Deployment Guide

## Prerequisites

- Linux server with Python 3.9+
- Domain name (optional but recommended)
- Google Gemini API key
- SendGrid API key

## Production Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-venv python3-pip nginx supervisor -y

# Create application user
sudo useradd -m -s /bin/bash stakesync
sudo su - stakesync
```

### 2. Clone and Setup

```bash
# Clone repository
git clone https://github.com/athariandre/stake-sync.git
cd stake-sync

# Run setup script
./setup.sh

# Edit .env with production values
nano .env
```

### 3. Configure Environment Variables

Update `.env`:

```env
# Production API keys
GEMINI_KEY=your_production_gemini_key
SENDGRID_API_KEY=your_production_sendgrid_key
SENDGRID_FROM_EMAIL=updates@yourdomain.com

# Production database (upgrade to PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/stakesync

# Server configuration
HOST=127.0.0.1
PORT=8000

# Security
SECRET_KEY=generate_a_secure_random_key_here
```

### 4. Database Setup (PostgreSQL)

For production, use PostgreSQL instead of SQLite:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres psql
CREATE DATABASE stakesync;
CREATE USER stakesync WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE stakesync TO stakesync;
\q

# Update requirements.txt to include psycopg2
echo "psycopg2-binary>=2.9.0" >> requirements.txt
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://stakesync:your_password@localhost/stakesync

# Initialize database
python -m app.database.init_db
```

### 5. Configure Supervisor

Create `/etc/supervisor/conf.d/stakesync.conf`:

```ini
[program:stakesync]
command=/home/stakesync/stake-sync/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
directory=/home/stakesync/stake-sync
user=stakesync
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/stakesync/app.log
stderr_logfile=/var/log/stakesync/app_error.log
environment=PATH="/home/stakesync/stake-sync/venv/bin"
```

Create log directory:

```bash
sudo mkdir -p /var/log/stakesync
sudo chown stakesync:stakesync /var/log/stakesync

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start stakesync
```

### 6. Configure Nginx

Create `/etc/nginx/sites-available/stakesync`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 4G;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/stakesync/stake-sync/app/static;
        expires 30d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/stakesync /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 8. Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Docker Deployment (Alternative)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Initialize database
RUN python -m app.database.init_db

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_KEY=${GEMINI_KEY}
      - SENDGRID_API_KEY=${SENDGRID_API_KEY}
      - SENDGRID_FROM_EMAIL=${SENDGRID_FROM_EMAIL}
      - DATABASE_URL=postgresql://stakesync:password@db/stakesync
    depends_on:
      - db
    volumes:
      - ./app:/app/app
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=stakesync
      - POSTGRES_USER=stakesync
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with Docker:

```bash
docker-compose up -d
```

## Monitoring & Maintenance

### Check Application Status

```bash
# Supervisor
sudo supervisorctl status stakesync

# Logs
sudo tail -f /var/log/stakesync/app.log
sudo tail -f /var/log/stakesync/app_error.log

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump -U stakesync stakesync > backup_$(date +%Y%m%d).sql

# Restore
psql -U stakesync stakesync < backup_20240101.sql
```

### Update Application

```bash
sudo su - stakesync
cd stake-sync
git pull
source venv/bin/activate
pip install -r requirements.txt
python -m app.database.init_db  # Run migrations if any
exit

sudo supervisorctl restart stakesync
```

## Security Checklist

- [ ] Use strong SECRET_KEY in .env
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS with SSL certificate
- [ ] Set proper file permissions (644 for files, 755 for directories)
- [ ] Keep .env file secure (chmod 600)
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Set up database backups
- [ ] Use firewall rules
- [ ] Implement rate limiting (optional)
- [ ] Set up monitoring/alerting

## Performance Optimization

### Database Indexing

The models already include necessary indexes, but monitor query performance:

```python
# Add additional indexes if needed
from sqlalchemy import Index

# In models.py
Index('idx_draft_user_status', Draft.user_id, Draft.status)
```

### Caching (Optional)

For high traffic, add Redis caching:

```bash
pip install redis
```

Update config.py to include Redis settings and cache frequently accessed data.

### Load Balancing

For multiple servers, use Nginx as a load balancer:

```nginx
upstream stakesync {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    location / {
        proxy_pass http://stakesync;
    }
}
```

## Troubleshooting

### Application won't start

```bash
# Check logs
sudo supervisorctl tail stakesync stderr

# Check Python syntax
cd /home/stakesync/stake-sync
source venv/bin/activate
python -m py_compile app/main.py
```

### Database connection errors

```bash
# Test PostgreSQL connection
psql -U stakesync -d stakesync -h localhost

# Check DATABASE_URL in .env
```

### Email sending fails

```bash
# Verify SendGrid API key
curl -X "GET" "https://api.sendgrid.com/v3/user/profile" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Support

For deployment issues:
- Check application logs
- Review Nginx error logs
- Test API endpoints manually
- Verify environment variables

## Rollback Procedure

If deployment fails:

```bash
sudo su - stakesync
cd stake-sync
git checkout <previous-commit-hash>
source venv/bin/activate
pip install -r requirements.txt
exit

sudo supervisorctl restart stakesync
```
