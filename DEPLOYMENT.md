# 🚀 Deployment Guide

This guide covers deploying the WebRTC application to production.

## 📋 Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` in `.env` to a strong random string
- [ ] Set `DEBUG=False` in production environment
- [ ] Configure proper CORS `ALLOWED_ORIGINS`
- [ ] Set up SSL/TLS certificates
- [ ] Review and update all default credentials

### Configuration
- [ ] Copy `.env.example` to `.env` and configure
- [ ] Set up email SMTP for OTP delivery
- [ ] Configure database (PostgreSQL recommended for production)
- [ ] Set up Redis for session management (optional)

### Infrastructure
- [ ] Server with minimum 2GB RAM, 2 CPU cores
- [ ] Domain name configured
- [ ] Firewall configured (ports 80, 443, 8000)
- [ ] SSL certificate (Let's Encrypt recommended)

## 🐳 Docker Deployment (Recommended)

### 1. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

### 2. Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
nano .env

# Update these critical values:
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
```

### 3. Build and Start Services

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access Application

- Frontend: http://your-domain.com
- API Docs: http://your-domain.com/docs

## 🖥️ Manual Deployment

### 1. Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx
sudo apt install nginx -y

# Install PostgreSQL (recommended)
sudo apt install postgresql postgresql-contrib -y
```

### 2. Clone and Setup Application

```bash
# Clone repository
git clone <your-repo-url>
cd webRTC

# Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

```bash
# For PostgreSQL
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE webrtc_db;
CREATE USER webrtc_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE webrtc_db TO webrtc_user;
\q

# Update .env
DATABASE_URL=postgresql://webrtc_user:secure_password@localhost:5432/webrtc_db
```

### 4. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

### 5. Configure Nginx

Create `/etc/nginx/sites-available/webrtc`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 10M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/webrtc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
```

### 7. Create Systemd Service

Create `/etc/systemd/system/webrtc.service`:

```ini
[Unit]
Description=WebRTC Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/webRTC/backend
Environment="PATH=/path/to/webRTC/backend/venv/bin"
ExecStart=/path/to/webRTC/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable webrtc
sudo systemctl start webrtc
sudo systemctl status webrtc
```

## 🔒 Security Hardening

### 1. Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Fail2Ban (Optional)

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Regular Updates

```bash
# Set up unattended upgrades
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## 📊 Monitoring

### Application Logs

```bash
# Docker
docker-compose logs -f backend

# Systemd
sudo journalctl -u webrtc -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Docker
git pull
docker-compose down
docker-compose build
docker-compose up -d

# Manual
cd webRTC
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart webrtc
```

### Database Backup

```bash
# PostgreSQL
pg_dump -U webrtc_user webrtc_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U webrtc_user webrtc_db < backup_20240101.sql
```

## 🌐 CDN and Optimization

### Enable Gzip Compression (Nginx)

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### Static File Caching

```nginx
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

## 🆘 Troubleshooting

### Application Won't Start

```bash
# Check logs
docker-compose logs backend
sudo journalctl -u webrtc -n 50

# Check database connection
psql -U webrtc_user -d webrtc_db -h localhost

# Check port availability
sudo netstat -tulpn | grep 8000
```

### WebSocket Connection Issues

- Ensure Nginx is properly configured for WebSocket
- Check firewall allows WebSocket connections
- Verify SSL certificate is valid

### Database Migration Errors

```bash
# Reset migrations (CAUTION: Data loss!)
cd backend
alembic downgrade base
alembic upgrade head
```

## 📈 Scaling

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Use shared PostgreSQL and Redis
- Configure session persistence

### Vertical Scaling

- Increase server resources
- Adjust `--workers` parameter
- Optimize database queries
- Enable Redis caching

## 🔐 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | Random 32+ char string |
| `DEBUG` | Debug mode | `False` in production |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host/db` |
| `REDIS_HOST` | Redis server host | `localhost` or `redis` |
| `SMTP_HOST` | Email server | `smtp.gmail.com` |
| `ALLOWED_ORIGINS` | CORS origins | `https://yourdomain.com` |

## ✅ Post-Deployment Verification

1. Visit your domain in browser
2. Test user registration flow
3. Verify email OTP delivery
4. Create and join a test room
5. Test video calling with multiple users
6. Check WebSocket connectivity
7. Monitor logs for errors
8. Test mobile responsiveness

---

**Need help?** Open an issue on GitHub or check the main README.
