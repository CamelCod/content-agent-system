# Deployment Guide

Complete deployment instructions for multiple platforms.

---

## 📋 Pre-Deployment Checklist

- [ ] Python 3.11+ installed
- [ ] OpenRouter API key obtained
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Local testing completed

---

## 🌐 Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free hosting, zero DevOps

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/content-agent-system.git
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - Go to App Settings → Secrets
   - Add:
   ```toml
   OPENROUTER_API_KEY = "your_key_here"
   ```

4. **Access Your App**
   - URL: `https://your-app-name.streamlit.app`

### Configuration

Files used:
- `requirements.txt` - Dependencies
- `packages.txt` - System packages
- `.streamlit/config.toml` - Streamlit config

---

## 🚂 Railway

**Best for**: Auto-deployment, great free tier

### Steps

1. **Install Railway CLI** (optional)
```bash
npm install -g railway
```

2. **Deploy via GitHub**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Streamlit

3. **Add Environment Variables**
   - Go to Variables tab
   - Add `OPENROUTER_API_KEY`

4. **Configure Start Command** (if needed)
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Files Used
- `requirements.txt`
- `Procfile` (optional)
- `runtime.txt` (optional)

---

## 🎨 Hugging Face Spaces

**Best for**: ML/AI community, free GPU options

### Steps

1. **Create Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Select "Streamlit" as SDK
   - Name your space

2. **Upload Files**
```bash
git clone https://huggingface.co/spaces/username/space-name
cd space-name
# Copy your files
cp -r /path/to/content-agent-system/* .
git add .
git commit -m "Initial deployment"
git push
```

3. **Add Secrets**
   - Go to Settings → Repository secrets
   - Add `OPENROUTER_API_KEY`

4. **Configuration File**

Create `README.md` in space root:
```yaml
---
title: Content Agent System
emoji: ✍️
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
---
```

---

## 🟣 Heroku

**Best for**: Traditional PaaS, extensive add-ons

### Steps

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and Create App**
```bash
heroku login
heroku create your-app-name
```

3. **Set Environment Variables**
```bash
heroku config:set OPENROUTER_API_KEY=your_key_here
```

4. **Deploy**
```bash
git push heroku main
```

5. **Open App**
```bash
heroku open
```

### Required Files

**Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt**
```
python-3.11.7
```

**packages.txt** (optional)
```
build-essential
```

---

## 🐳 Docker

**Best for**: Containerized deployment, any platform

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p knowledge_bases vector_stores

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    volumes:
      - ./knowledge_bases:/app/knowledge_bases
      - ./vector_stores:/app/vector_stores
```

### Deploy

```bash
# Build
docker build -t content-agent-system .

# Run
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=your_key \
  content-agent-system

# Or with docker-compose
docker-compose up
```

---

## 🖥️ Local Network Deployment

**Best for**: Internal tools, team use

### Option 1: Streamlit Sharing

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Access from other devices: `http://your-ip:8501`

### Option 2: Nginx Reverse Proxy

**Install Nginx**
```bash
sudo apt install nginx
```

**Configure** (`/etc/nginx/sites-available/content-agent`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Enable and Restart**
```bash
sudo ln -s /etc/nginx/sites-available/content-agent /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Option 3: Systemd Service

Create `/etc/systemd/system/content-agent.service`:
```ini
[Unit]
Description=Content Agent System
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/content-agent-system
Environment="OPENROUTER_API_KEY=your_key"
ExecStart=/path/to/venv/bin/streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and Start**
```bash
sudo systemctl enable content-agent
sudo systemctl start content-agent
```

---

## ☁️ AWS Deployment

### Option 1: EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.small or larger
   - Open port 8501

2. **Setup**
```bash
ssh ubuntu@your-instance

# Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip git

# Clone and setup
git clone https://github.com/yourusername/content-agent-system.git
cd content-agent-system
./deploy.sh

# Run
streamlit run app.py --server.address=0.0.0.0
```

3. **Use systemd for persistence** (see above)

### Option 2: ECS (Docker)

1. Push image to ECR
2. Create ECS task definition
3. Configure service with environment variables
4. Deploy

---

## 🔧 Google Cloud Platform

### Cloud Run

1. **Enable Cloud Run API**
2. **Deploy**
```bash
gcloud run deploy content-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENROUTER_API_KEY=your_key
```

### App Engine

Create `app.yaml`:
```yaml
runtime: python311
entrypoint: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

env_variables:
  OPENROUTER_API_KEY: "your_key_here"
```

Deploy:
```bash
gcloud app deploy
```

---

## 🌊 DigitalOcean

### App Platform

1. **Create App**
   - Link GitHub repository
   - Select "Python" as type

2. **Configure**
   - Run Command: `streamlit run app.py --server.port=8080 --server.address=0.0.0.0`
   - Add environment variable: `OPENROUTER_API_KEY`

3. **Deploy**

### Droplet (VM)

Same as AWS EC2 steps above.

---

## 🔐 Security Best Practices

### Environment Variables
- ✅ Always use environment variables for API keys
- ✅ Never commit `.env` or `secrets.toml`
- ✅ Use platform-specific secret management

### Network Security
- ✅ Use HTTPS in production
- ✅ Configure firewall rules
- ✅ Limit API access if needed

### Application Security
- ✅ Keep dependencies updated
- ✅ Use authentication if needed (Streamlit auth)
- ✅ Monitor API usage and costs

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics
- Logs in dashboard
- Resource usage tracking

### Other Platforms
- Use platform-specific monitoring
- Set up logging
- Track API usage via OpenRouter dashboard

---

## 🐛 Troubleshooting

### Port Issues
```bash
# Check if port is in use
lsof -i :8501

# Use different port
streamlit run app.py --server.port=8502
```

### Memory Issues
- Increase instance size
- Optimize vector store caching
- Use smaller embedding models

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

### API Key Issues
```bash
# Test API key
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta-llama/llama-3.1-8b-instruct:free","messages":[{"role":"user","content":"test"}]}'
```

---

## 🎯 Platform Comparison

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| Streamlit Cloud | ✅ Yes | ⭐⭐⭐⭐⭐ | Quick demos, prototypes |
| Railway | ✅ Limited | ⭐⭐⭐⭐ | Side projects, startups |
| Heroku | ✅ Limited | ⭐⭐⭐⭐ | Traditional apps |
| HF Spaces | ✅ Yes | ⭐⭐⭐⭐ | ML community, sharing |
| Docker | ➖ Depends | ⭐⭐⭐ | Any platform, flexibility |
| AWS/GCP | ✅ Limited | ⭐⭐ | Production, scale |

---

## 📚 Additional Resources

- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Need help?** Check [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) or open an issue on GitHub.
