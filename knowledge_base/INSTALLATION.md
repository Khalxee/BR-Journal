# DocuApp Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+ / macOS 10.15+
- **Python**: 3.9 or higher
- **Memory**: 2GB RAM minimum
- **Storage**: 5GB available space
- **Network**: Internet connection for package installation

### Recommended Requirements
- **Memory**: 4GB RAM or higher
- **Storage**: 20GB available space
- **Database**: PostgreSQL 12+ for production
- **Cache**: Redis 6.0+ for optimal performance
- **Web Server**: Nginx for production deployment

## Installation Methods

### Method 1: Docker Installation (Recommended)

#### Prerequisites
- Docker 20.10+ installed
- Docker Compose 2.0+ installed

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-org/docuapp.git
cd docuapp

# Start with Docker Compose
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000
```

#### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://user:pass@db:5432/docuapp
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - .:/app
      - media_volume:/app/media
      - static_volume:/app/static

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=docuapp
      - POSTGRES_USER=docuapp
      - POSTGRES_PASSWORD=docuapp123
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
  media_volume:
  static_volume:
```

### Method 2: Manual Installation

#### Step 1: Install Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server

# CentOS/RHEL
sudo yum install python3 python3-pip postgresql postgresql-server redis

# macOS (using Homebrew)
brew install python3 postgresql redis
```

#### Step 2: Database Setup
```bash
# PostgreSQL setup
sudo -u postgres psql
CREATE DATABASE docuapp;
CREATE USER docuapp WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE docuapp TO docuapp;
\q

# Start services
sudo systemctl start postgresql
sudo systemctl start redis
sudo systemctl enable postgresql
sudo systemctl enable redis
```

#### Step 3: Application Setup
```bash
# Clone repository
git clone https://github.com/your-org/docuapp.git
cd docuapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database and Redis settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

### Method 3: Production Deployment

#### Prerequisites
- Ubuntu 20.04+ server
- Domain name configured
- SSL certificate (Let's Encrypt recommended)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx supervisor

# Create application user
sudo useradd -m -s /bin/bash docuapp
sudo su - docuapp
```

#### Step 2: Application Deployment
```bash
# As docuapp user
git clone https://github.com/your-org/docuapp.git
cd docuapp

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configure environment
cp .env.example .env
# Edit .env for production settings

# Setup database
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Step 3: Gunicorn Configuration
```bash
# Create gunicorn config
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "docuapp"
group = "docuapp"
EOF
```

#### Step 4: Supervisor Configuration
```bash
# Create supervisor config
sudo cat > /etc/supervisor/conf.d/docuapp.conf << EOF
[program:docuapp]
command=/home/docuapp/docuapp/venv/bin/gunicorn --config gunicorn.conf.py docuapp.wsgi:application
directory=/home/docuapp/docuapp
user=docuapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/docuapp.log
EOF

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start docuapp
```

#### Step 5: Nginx Configuration
```bash
# Create Nginx config
sudo cat > /etc/nginx/sites-available/docuapp << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /home/docuapp/docuapp/static/;
    }
    
    location /media/ {
        alias /home/docuapp/docuapp/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/docuapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Configuration

### Environment Variables
```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/docuapp
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# File upload settings
MEDIA_URL=/media/
STATIC_URL=/static/
```

### Database Configuration
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'docuapp'),
        'USER': os.environ.get('DB_USER', 'docuapp'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## SSL Certificate Setup

### Using Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add line: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring Setup

### Log Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/docuapp/django.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Check Script
```bash
#!/bin/bash
# health_check.sh
curl -f http://localhost:8000/health/ || exit 1
```

## Backup Configuration

### Database Backup Script
```bash
#!/bin/bash
# backup_db.sh
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U docuapp docuapp > "$BACKUP_DIR/docuapp_$DATE.sql"
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
```

### File Backup Script
```bash
#!/bin/bash
# backup_files.sh
BACKUP_DIR="/backups/files"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /home/docuapp/docuapp/media/
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
```

## Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database permissions
sudo -u postgres psql -c "SELECT * FROM pg_user;"

# Test connection
python manage.py dbshell
```

#### Static Files Not Loading
```bash
# Check static file collection
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t
sudo systemctl reload nginx

# Check file permissions
ls -la /home/docuapp/docuapp/static/
```

#### Application Not Starting
```bash
# Check Gunicorn
sudo supervisorctl status docuapp
sudo supervisorctl restart docuapp

# Check logs
sudo tail -f /var/log/docuapp.log
sudo journalctl -u supervisor
```

### Performance Tuning

#### Database Optimization
```sql
-- PostgreSQL configuration
-- Add to postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
```

#### Redis Configuration
```bash
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## Security Hardening

### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Application Security
```python
# settings.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

This installation guide provides comprehensive instructions for deploying DocuApp in various environments. For additional support, refer to the troubleshooting section or contact the support team.
