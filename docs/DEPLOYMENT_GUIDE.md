# 🚀 Deployment Guide

This guide covers various deployment options for the Auto Feedback Generator, from local development to production cloud deployments.

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Git
- Basic understanding of web deployment

## 🏠 Local Development

### Quick Setup
```bash
# Clone and setup
git clone https://github.com/1234-ad/auto-feedback-generator.git
cd auto-feedback-generator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run services
python run_backend.py    # Terminal 1
python run_frontend.py   # Terminal 2
```

## 🐳 Docker Deployment

### Single Container (Development)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 5000 8501

# Install supervisor for multi-process
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### Docker Compose (Recommended)
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    command: python run_backend.py
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./backend:/app/backend
    restart: unless-stopped

  frontend:
    build: .
    command: python run_frontend.py
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:5000
      - STREAMLIT_HEADLESS=true
    depends_on:
      - backend
    volumes:
      - ./frontend:/app/frontend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

### Build and Run
```bash
# Create .env file with your variables
echo "OPENAI_API_KEY=your_key_here" > .env

# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment Options

### 1. Render (Recommended for Beginners)

**Backend Deployment:**
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python run_backend.py
   Environment: Python 3.9
   ```
4. Add environment variables:
   ```
   OPENAI_API_KEY=your_key_here
   FLASK_ENV=production
   PORT=5000
   ```

**Frontend Deployment:**
1. Create another Web Service for frontend
2. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
   Environment: Python 3.9
   ```
3. Add environment variables:
   ```
   BACKEND_URL=https://your-backend-url.onrender.com
   STREAMLIT_HEADLESS=true
   ```

### 2. Heroku

**Prepare for Heroku:**
```bash
# Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT backend.app:app" > Procfile
echo "streamlit: streamlit run frontend/app.py --server.port \$PORT --server.address 0.0.0.0" >> Procfile

# Create runtime.txt
echo "python-3.9.18" > runtime.txt
```

**Deploy Backend:**
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-feedback-backend

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

**Deploy Frontend:**
```bash
# Create frontend app
heroku create your-feedback-frontend

# Set environment variables
heroku config:set BACKEND_URL=https://your-feedback-backend.herokuapp.com
heroku config:set STREAMLIT_HEADLESS=true

# Deploy
git push heroku main
```

### 3. Railway

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python run_backend.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Deploy Steps:**
1. Connect GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically triggers on git push

### 4. Streamlit Cloud (Frontend Only)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file path: `frontend/app.py`
5. Add secrets in Streamlit Cloud dashboard:
   ```toml
   [secrets]
   BACKEND_URL = "https://your-backend-url.com"
   ```

### 5. AWS Deployment

**Using AWS Elastic Beanstalk:**

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 auto-feedback-generator

# Create environment
eb create production

# Set environment variables
eb setenv OPENAI_API_KEY=your_key_here FLASK_ENV=production

# Deploy
eb deploy
```

**Using AWS Lambda + API Gateway:**
```python
# lambda_handler.py
import serverless_wsgi
from backend.app import app

def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
```

### 6. Google Cloud Platform

**App Engine deployment:**
```yaml
# app.yaml
runtime: python39

env_variables:
  OPENAI_API_KEY: "your_key_here"
  FLASK_ENV: "production"

handlers:
- url: /.*
  script: auto

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

```bash
# Deploy
gcloud app deploy
```

## 🔧 Production Configuration

### Environment Variables
```env
# Production settings
FLASK_ENV=production
DEBUG=False
OPENAI_API_KEY=your_production_key
OPENAI_MODEL=gpt-4
MAX_TOKENS=500
TEMPERATURE=0.7

# Security
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://yourdomain.com

# Performance
GUNICORN_WORKERS=4
CACHE_TTL=3600
RATE_LIMIT_PER_MINUTE=30

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_here
```

### Nginx Configuration
```nginx
# nginx.conf
upstream backend {
    server backend:5000;
}

upstream frontend {
    server frontend:8501;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Supervisor Configuration
```ini
# supervisord.conf
[supervisord]
nodaemon=true
user=root

[program:backend]
command=python run_backend.py
directory=/app
autostart=true
autorestart=true
stderr_logfile=/var/log/backend.err.log
stdout_logfile=/var/log/backend.out.log

[program:frontend]
command=python run_frontend.py
directory=/app
autostart=true
autorestart=true
stderr_logfile=/var/log/frontend.err.log
stdout_logfile=/var/log/frontend.out.log
```

## 📊 Monitoring and Logging

### Health Checks
```python
# health_check.py
import requests
import time

def check_services():
    services = {
        'backend': 'http://localhost:5000/api/health',
        'frontend': 'http://localhost:8501'
    }
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            status = "✅ UP" if response.status_code == 200 else "❌ DOWN"
            print(f"{name}: {status}")
        except Exception as e:
            print(f"{name}: ❌ DOWN - {str(e)}")

if __name__ == "__main__":
    check_services()
```

### Logging Configuration
```python
# logging_config.py
import logging
import os

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
```

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit API keys to version control
- Use secure secret management services
- Rotate keys regularly

### 2. HTTPS/SSL
```bash
# Generate SSL certificate with Let's Encrypt
certbot --nginx -d yourdomain.com
```

### 3. Rate Limiting
```python
# Add to Flask app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/generate-feedback')
@limiter.limit("10 per minute")
def generate_feedback():
    # Your code here
```

### 4. Input Validation
- Validate all inputs server-side
- Sanitize user data
- Use parameterized queries

## 🚨 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9
```

**2. OpenAI API Errors**
```python
# Add retry logic
import time
from openai.error import RateLimitError

def call_openai_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return openai.ChatCompletion.create(...)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
```

**3. Memory Issues**
```bash
# Monitor memory usage
docker stats

# Limit container memory
docker run -m 512m your-image
```

### Performance Optimization

**1. Caching**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=3600)
def generate_feedback_cached(prompt_hash):
    # Your feedback generation logic
```

**2. Database Connection Pooling**
```python
# If using database
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement session management
- Consider microservices architecture

### Vertical Scaling
- Monitor resource usage
- Optimize code performance
- Use caching strategies

### Database Scaling
- Implement read replicas
- Use connection pooling
- Consider NoSQL for high throughput

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

This deployment guide provides comprehensive coverage of various deployment scenarios. Choose the option that best fits your needs, budget, and technical requirements.