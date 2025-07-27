# AI Pitch Deck Generator - Deployment Guide

This guide provides comprehensive instructions for deploying the AI Pitch Deck Generator platform in various environments.

## 🚀 Quick Start (Development)

### Prerequisites
- Docker and Docker Compose
- Git
- At least 8GB RAM and 20GB disk space

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-pitch-deck-generator
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```bash
# AI Services
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
SECRET_KEY=your_secret_key_here

# Database (optional - defaults provided in docker-compose)
DATABASE_URL=postgresql://pitchdeck_user:pitchdeck_password@postgres:5432/pitchdeck
REDIS_URL=redis://redis:6379

# External APIs (optional)
CRUNCHBASE_API_KEY=your_crunchbase_key
PITCHBOOK_API_KEY=your_pitchbook_key

# File Storage (optional)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=your_bucket_name
```

### 3. Start the Platform
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Monitoring**: http://localhost:3001 (admin/admin)

## 🏭 Production Deployment

### Option 1: Docker Compose (Recommended for Small-Medium Scale)

#### 1. Production Environment Setup
```bash
# Create production environment file
cp .env.example .env.production

# Edit production environment variables
nano .env.production
```

#### 2. Production Docker Compose
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale services as needed
docker-compose -f docker-compose.prod.yml up -d --scale backend=3 --scale celery-worker=2
```

### Option 2: Kubernetes Deployment

#### 1. Prerequisites
- Kubernetes cluster (1.20+)
- Helm 3.0+
- kubectl configured

#### 2. Deploy to Kubernetes
```bash
# Add Helm repository
helm repo add ai-pitch-deck https://charts.ai-pitch-deck.com

# Install the platform
helm install ai-pitch-deck ai-pitch-deck/ai-pitch-deck-generator \
  --namespace ai-pitch-deck \
  --create-namespace \
  --values values-production.yaml
```

#### 3. Production Values Configuration
Create `values-production.yaml`:
```yaml
global:
  environment: production
  
backend:
  replicas: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "500m"
  
frontend:
  replicas: 2
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  
database:
  postgresql:
    enabled: true
    postgresqlPassword: "secure_password"
    persistence:
      enabled: true
      size: 100Gi
  
redis:
  enabled: true
  auth:
    enabled: true
    password: "secure_redis_password"
  
monitoring:
  prometheus:
    enabled: true
  grafana:
    enabled: true
    adminPassword: "secure_grafana_password"
```

### Option 3: Cloud Platform Deployment

#### AWS ECS Deployment
```bash
# Deploy using AWS CLI
aws ecs create-cluster --cluster-name ai-pitch-deck

# Deploy services
aws ecs create-service \
  --cluster ai-pitch-deck \
  --service-name backend \
  --task-definition backend-task \
  --desired-count 3
```

#### Google Cloud Run Deployment
```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-pitch-deck-backend
gcloud run deploy ai-pitch-deck-backend \
  --image gcr.io/PROJECT_ID/ai-pitch-deck-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔧 Configuration

### Database Configuration
```bash
# PostgreSQL Configuration
POSTGRES_DB=pitchdeck
POSTGRES_USER=pitchdeck_user
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Connection Pool Settings
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
DATABASE_POOL_TIMEOUT=30
```

### Redis Configuration
```bash
# Redis Settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=secure_redis_password
REDIS_DB=0
REDIS_MAX_CONNECTIONS=50
```

### AI Model Configuration
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Anthropic Configuration
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000
```

### Security Configuration
```bash
# JWT Settings
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
CORS_ALLOW_CREDENTIALS=true
```

## 📊 Monitoring and Logging

### Prometheus Metrics
The platform exposes metrics at `/metrics`:
- Request rates and latencies
- Database connection pool status
- AI model usage and costs
- User activity metrics

### Grafana Dashboards
Pre-configured dashboards include:
- Application Performance
- AI Model Usage
- User Engagement
- System Health

### Log Aggregation
```bash
# Configure log shipping to ELK stack
docker-compose -f docker-compose.yml -f docker-compose.logging.yml up -d
```

## 🔒 Security Hardening

### SSL/TLS Configuration
```bash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/private.key \
  -out nginx/ssl/certificate.crt

# Configure nginx with SSL
cp nginx/nginx-ssl.conf nginx/nginx.conf
```

### Network Security
```bash
# Configure firewall rules
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

### Database Security
```bash
# Enable SSL for PostgreSQL
echo "ssl = on" >> /etc/postgresql/postgresql.conf
echo "ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'" >> /etc/postgresql/postgresql.conf
echo "ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'" >> /etc/postgresql/postgresql.conf
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
docker exec ai-pitch-deck-postgres pg_dump -U pitchdeck_user pitchdeck > $BACKUP_DIR/backup_$DATE.sql

# Add to crontab for daily backups
0 2 * * * /path/to/backup-script.sh
```

### File Storage Backup
```bash
# Backup uploaded files
aws s3 sync /app/data/uploads s3://your-backup-bucket/uploads --delete

# Backup generated pitch decks
aws s3 sync /app/data/pitch-decks s3://your-backup-bucket/pitch-decks --delete
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale backend services
docker-compose up -d --scale backend=5 --scale celery-worker=3

# Scale with Kubernetes
kubectl scale deployment ai-pitch-deck-backend --replicas=5
```

### Load Balancing
```bash
# Configure nginx load balancer
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

### Database Scaling
```bash
# Configure read replicas
# Add to docker-compose.yml
postgres-replica:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: pitchdeck
    POSTGRES_USER: pitchdeck_user
    POSTGRES_PASSWORD: pitchdeck_password
  command: postgres -c hot_standby=on -c primary_conninfo='host=postgres user=pitchdeck_user password=pitchdeck_password'
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database connectivity
docker exec ai-pitch-deck-backend python -c "
import psycopg2
conn = psycopg2.connect('postgresql://pitchdeck_user:pitchdeck_password@postgres:5432/pitchdeck')
print('Database connection successful')
"
```

#### 2. AI API Rate Limits
```bash
# Check API usage
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/usage
```

#### 3. Memory Issues
```bash
# Monitor memory usage
docker stats ai-pitch-deck-backend ai-pitch-deck-celery-worker

# Increase memory limits
docker-compose up -d --scale backend=2
```

### Performance Optimization

#### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_startups_user_id ON startups(user_id);
CREATE INDEX idx_pitch_decks_startup_id ON pitch_decks(startup_id);
CREATE INDEX idx_slides_pitch_deck_id ON slides(pitch_deck_id);
```

#### 2. Caching Strategy
```python
# Configure Redis caching
CACHE_TTL = 3600  # 1 hour
CACHE_PREFIX = "ai_pitch_deck"
```

#### 3. CDN Configuration
```bash
# Configure CloudFront for static assets
aws cloudfront create-distribution \
  --origin-domain-name your-s3-bucket.s3.amazonaws.com \
  --default-root-object index.html
```

## 📞 Support

For deployment support:
- **Documentation**: [docs.ai-pitch-deck.com](https://docs.ai-pitch-deck.com)
- **Issues**: [GitHub Issues](https://github.com/ai-pitch-deck/issues)
- **Email**: support@ai-pitch-deck.com
- **Slack**: [Join our community](https://slack.ai-pitch-deck.com)

## 🔄 Updates and Maintenance

### Updating the Platform
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run database migrations
docker exec ai-pitch-deck-backend alembic upgrade head
```

### Health Checks
```bash
# Automated health check script
#!/bin/bash
curl -f http://localhost:8000/health || exit 1
curl -f http://localhost:3000 || exit 1
```

### Monitoring Alerts
Configure alerts for:
- Service downtime
- High error rates
- Database connection issues
- AI API failures
- Disk space usage
- Memory usage 