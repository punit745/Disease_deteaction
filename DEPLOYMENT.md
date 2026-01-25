# Deployment Guide - Disease Detection System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Security Considerations](#security-considerations)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

### System Requirements
- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL 15 or higher (for production)
- Nginx (for reverse proxy)
- 2GB+ RAM
- 10GB+ disk space

### Software Dependencies
- Git
- pip
- virtualenv or conda

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-web.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize Database

```bash
python -c "from app import init_db; init_db()"
```

### 6. Run Development Server

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Quick Start with Docker Compose

1. **Build and Start Services**

```bash
docker-compose up -d
```

2. **Initialize Database**

```bash
docker-compose exec web python -c "from app import init_db; init_db()"
```

3. **View Logs**

```bash
docker-compose logs -f web
```

4. **Stop Services**

```bash
docker-compose down
```

### Docker Configuration

The `docker-compose.yml` includes:
- **Web Application** (Flask + Gunicorn)
- **PostgreSQL Database**
- **Nginx Reverse Proxy**

Services are connected via a custom bridge network and use persistent volumes for data.

## Production Deployment

### Ubuntu/Debian Server Setup

#### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### 3. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 4. Clone and Configure

```bash
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-
cp .env.example .env
nano .env  # Edit configuration
```

#### 5. Generate Secret Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

Add these to your `.env` file.

#### 6. Deploy with Docker Compose

```bash
docker-compose up -d
docker-compose exec web python -c "from app import init_db; init_db()"
```

#### 7. Configure Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSL/TLS Configuration

#### Using Let's Encrypt (Recommended)

1. **Install Certbot**

```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain Certificate**

```bash
sudo certbot --nginx -d yourdomain.com
```

3. **Update nginx.conf**

Uncomment the HTTPS server block in `nginx.conf` and update paths.

4. **Restart Services**

```bash
docker-compose restart nginx
```

### Systemd Service (Alternative to Docker)

Create `/etc/systemd/system/disease-detection.service`:

```ini
[Unit]
Description=Disease Detection Web Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/disease_detection
Environment="PATH=/opt/disease_detection/venv/bin"
ExecStart=/opt/disease_detection/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable disease-detection
sudo systemctl start disease-detection
```

## Environment Configuration

### Required Environment Variables

```bash
# Application
SECRET_KEY=<64-character-random-string>
JWT_SECRET_KEY=<64-character-random-string>
FLASK_ENV=production
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Server
PORT=5000
```

### Optional Variables

```bash
# File Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# JWT
JWT_EXPIRATION_HOURS=24

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Database Setup

### PostgreSQL Installation (Standalone)

```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```

Create database and user:

```sql
CREATE DATABASE disease_detection;
CREATE USER disease_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE disease_detection TO disease_user;
\q
```

### Database Migrations

Initialize tables:

```bash
python -c "from app import init_db; init_db()"
```

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U disease_user disease_detection > backup.sql

# Restore
docker-compose exec -T db psql -U disease_user disease_detection < backup.sql
```

## Security Considerations

### 1. Environment Security

- Never commit `.env` files to version control
- Use strong, unique passwords and secret keys
- Rotate keys periodically
- Use environment-specific configurations

### 2. Database Security

- Use strong database passwords
- Restrict database access to application server only
- Enable SSL for database connections in production
- Regular backups with encryption

### 3. API Security

- JWT token authentication implemented
- Rate limiting configured in nginx
- CORS properly configured
- Input validation on all endpoints

### 4. SSL/TLS

- Always use HTTPS in production
- Use Let's Encrypt for free SSL certificates
- Configure strong cipher suites
- Enable HTTP Strict Transport Security (HSTS)

### 5. Application Security

- Sanitize all user inputs
- Use parameterized queries (SQLAlchemy ORM)
- Implement proper error handling
- Log security events

### 6. HIPAA Compliance Considerations

For healthcare data:
- Encrypt data at rest and in transit
- Implement audit logging
- Access controls and authentication
- Data backup and disaster recovery
- Business Associate Agreements (BAA)
- Regular security assessments

## Monitoring and Maintenance

### Health Checks

The application provides a health check endpoint:

```bash
curl http://localhost:5000/api/health
```

### Logging

#### View Application Logs

```bash
# Docker
docker-compose logs -f web

# Systemd
sudo journalctl -u disease-detection -f
```

#### Log Files

Logs are stored in:
- Application: `logs/app.log`
- Nginx: Docker container logs
- Database: Docker container logs

### Performance Monitoring

#### Resource Usage

```bash
# Docker stats
docker stats

# System resources
htop
```

#### Database Performance

```bash
# Connect to database
docker-compose exec db psql -U disease_user disease_detection

# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Check database size
SELECT pg_size_pretty(pg_database_size('disease_detection'));
```

### Backup Strategy

#### Automated Backups

Create a cron job for regular backups:

```bash
# Add to crontab (crontab -e)
0 2 * * * cd /path/to/Disease_deteaction- && docker-compose exec -T db pg_dump -U disease_user disease_detection | gzip > /backups/db-$(date +\%Y\%m\%d).sql.gz
```

#### File Backups

```bash
# Backup uploads directory
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz uploads/
```

### Scaling Considerations

#### Horizontal Scaling

1. Use a load balancer (e.g., AWS ELB, Nginx)
2. Deploy multiple application instances
3. Use external PostgreSQL (e.g., AWS RDS)
4. Shared file storage (e.g., AWS S3, NFS)

#### Vertical Scaling

1. Increase Gunicorn workers
2. Allocate more memory/CPU to containers
3. Optimize database queries
4. Add database indexes

### Maintenance Tasks

#### Update Application

```bash
git pull origin main
docker-compose build
docker-compose up -d
```

#### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-web.txt
```

#### Database Cleanup

```bash
# Remove old test results (older than 2 years)
docker-compose exec web python -c "
from app import app, db, TestResult
from datetime import datetime, timedelta
with app.app_context():
    cutoff = datetime.utcnow() - timedelta(days=730)
    TestResult.query.filter(TestResult.test_date < cutoff).delete()
    db.session.commit()
"
```

## Troubleshooting

### Common Issues

#### Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U disease_user disease_detection
```

#### Application Won't Start

```bash
# Check logs
docker-compose logs web

# Verify environment variables
docker-compose exec web env

# Check disk space
df -h
```

#### High Memory Usage

```bash
# Reduce Gunicorn workers in Dockerfile
# Optimize database queries
# Add caching layer (Redis)
```

### Getting Help

- Check application logs
- Review nginx error logs
- Monitor system resources
- Check database connections
- Verify environment configuration

## Production Checklist

- [ ] Secret keys generated and configured
- [ ] Database secured with strong password
- [ ] SSL/TLS certificates installed
- [ ] Firewall configured
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Error tracking setup
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] Database indexes optimized
- [ ] Log rotation configured
- [ ] Health checks verified
- [ ] Documentation updated
- [ ] Security audit completed

## Support

For issues and questions:
- GitHub Issues: https://github.com/punit745/Disease_deteaction-/issues
- Documentation: See README.md and API_DOCUMENTATION.md
