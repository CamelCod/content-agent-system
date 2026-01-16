# Setup & Deployment Checklist

Step-by-step checklist to get your Content Agent System up and running.

---

## 📋 Phase 1: Initial Setup

### Prerequisites
- [ ] Python 3.11+ installed
  ```bash
  python --version  # Should show 3.11 or higher
  ```
- [ ] Git installed
  ```bash
  git --version
  ```
- [ ] Text editor or IDE ready
- [ ] Terminal/command line access

---

## 🔑 Phase 2: API Key Setup

### Get OpenRouter API Key
- [ ] Go to [OpenRouter](https://openrouter.ai)
- [ ] Sign up for free account
- [ ] Navigate to [API Keys](https://openrouter.ai/keys)
- [ ] Click "Create Key"
- [ ] Copy your API key
- [ ] Save it securely (you'll need it multiple times)

**💡 Tip**: Free tier includes access to Llama 3.1 8B model

---

## 📦 Phase 3: Repository Setup

### Clone & Configure
- [ ] Clone the repository
  ```bash
  git clone https://github.com/CamelCod/content-agent-system.git
  cd content-agent-system
  ```

- [ ] Run setup script
  ```bash
  chmod +x setup_repo.sh
  ./setup_repo.sh
  ```

- [ ] Configure `.env` file
  ```bash
  nano .env  # or use your editor
  ```
  Add:
  ```
  OPENROUTER_API_KEY=your_actual_key_here
  ```

- [ ] Configure Streamlit secrets
  ```bash
  nano .streamlit/secrets.toml
  ```
  Add:
  ```toml
  OPENROUTER_API_KEY = "your_actual_key_here"
  ```

---

## 🔧 Phase 4: Dependencies Installation

### Install Python Packages
- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  # Linux/Mac
  source venv/bin/activate
  
  # Windows
  venv\Scripts\activate
  ```

- [ ] Upgrade pip
  ```bash
  pip install --upgrade pip
  ```

- [ ] Install requirements
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify installation
  ```bash
  pip list | grep -E "streamlit|langchain|chromadb"
  ```

---

## 📚 Phase 5: Knowledge Base Setup (Optional)

### Add Content to Knowledge Base
- [ ] Create sample content files
  ```bash
  # Voice and style guide
  echo "Write clearly and concisely..." > knowledge_bases/voice_and_style/style_guide.md
  ```

- [ ] Add examples (optional)
  - [ ] LinkedIn post examples → `knowledge_bases/examples/linkedin_posts/`
  - [ ] Blog samples → `knowledge_bases/examples/blog_samples/`
  - [ ] Article samples → `knowledge_bases/examples/article_samples/`

- [ ] Add reference materials (optional)
  - [ ] Content frameworks → `knowledge_bases/content_framework/`
  - [ ] Reference docs → `knowledge_bases/reference/`

**💡 Tip**: System works without knowledge base, but RAG improves quality

---

## ✅ Phase 6: Local Testing

### Test Core Components
- [ ] Test imports
  ```bash
  python -c "from core.config import OPENROUTER_API_KEY; print('API Key:', 'SET' if OPENROUTER_API_KEY else 'NOT SET')"
  ```

- [ ] Test knowledge base
  ```bash
  python -c "from core.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); print('Knowledge base initialized')"
  ```

- [ ] Test agents
  ```bash
  python -c "from agents.linkedin_agent import LinkedInAgent; agent = LinkedInAgent(); print('Agent initialized')"
  ```

### Run Web Interface
- [ ] Start Streamlit
  ```bash
  streamlit run app.py
  ```

- [ ] Open browser to `http://localhost:8501`

- [ ] Test LinkedIn generator
  - [ ] Enter a topic
  - [ ] Select lens and objective
  - [ ] Click "Generate Post"
  - [ ] Verify content appears
  - [ ] Check validation score

- [ ] Test calendar mode
  - [ ] Switch to "Calendar Mode"
  - [ ] Select a calendar entry
  - [ ] Generate post
  - [ ] Verify output

- [ ] Test content history
  - [ ] Navigate to "Content History"
  - [ ] Verify generated posts appear
  - [ ] Test copy/delete functions

### Test Batch Processor
- [ ] Run batch processor
  ```bash
  python batch_processor.py
  ```

- [ ] Verify JSON output created
  ```bash
  ls -l week_2_4_results.json
  ```

- [ ] Check results
  ```bash
  cat week_2_4_results.json | head -20
  ```

---

## 🚀 Phase 7: Deployment Preparation

### Choose Deployment Platform
- [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Select platform:
  - [ ] Streamlit Cloud (recommended for beginners)
  - [ ] Railway
  - [ ] Heroku
  - [ ] Hugging Face Spaces
  - [ ] Docker
  - [ ] Local network

### Pre-Deployment Checks
- [ ] All tests passing locally
- [ ] `.env` not committed to git
  ```bash
  git status  # Should NOT show .env or secrets.toml
  ```
- [ ] `.gitignore` properly configured
- [ ] Requirements.txt up to date
- [ ] README.md reviewed

---

## 🌐 Phase 8: Deploy to Streamlit Cloud

### Streamlit Cloud Deployment
- [ ] Commit changes to git
  ```bash
  git add .
  git commit -m "Ready for deployment"
  ```

- [ ] Push to GitHub
  ```bash
  git remote add origin https://github.com/yourusername/content-agent-system.git
  git push -u origin main
  ```

- [ ] Go to [share.streamlit.io](https://share.streamlit.io)

- [ ] Connect GitHub repository

- [ ] Configure app
  - [ ] Repository: `yourusername/content-agent-system`
  - [ ] Branch: `main`
  - [ ] Main file: `app.py`

- [ ] Add secrets
  - [ ] Click "Advanced settings"
  - [ ] Add to Secrets:
    ```toml
    OPENROUTER_API_KEY = "your_actual_key_here"
    ```

- [ ] Click "Deploy"

- [ ] Wait for deployment (2-5 minutes)

- [ ] Test deployed app
  - [ ] Open app URL
  - [ ] Test all features
  - [ ] Generate sample content
  - [ ] Verify validation works

---

## ✨ Phase 9: Post-Deployment

### Verification
- [ ] App loads without errors
- [ ] All navigation pages work
- [ ] Content generation works
- [ ] Validation scores appear
- [ ] Content history persists in session

### Monitoring
- [ ] Check Streamlit Cloud analytics
- [ ] Monitor API usage at [OpenRouter dashboard](https://openrouter.ai/activity)
- [ ] Set up usage alerts (optional)

### Share
- [ ] Copy app URL
- [ ] Share with team/users
- [ ] Document any customizations

---

## 🔧 Phase 10: Customization (Optional)

### Customize Content
- [ ] Adjust voice guidelines in `core/config.py`
- [ ] Modify signature phrases
- [ ] Update content calendar in `batch_processor.py`
- [ ] Add custom lenses/objectives

### Customize UI
- [ ] Update theme in `.streamlit/config.toml`
- [ ] Modify page title/icon in `app.py`
- [ ] Add custom branding

### Optimize Performance
- [ ] Pre-build vector store
- [ ] Cache knowledge base in session
- [ ] Adjust model selection defaults

---

## 📊 Success Criteria

All systems go when:
- ✅ Web UI loads without errors
- ✅ Can generate LinkedIn posts
- ✅ Validation scores 8.0+ for good content
- ✅ Batch processor completes successfully
- ✅ Content history works
- ✅ Calendar mode functional
- ✅ Deployed and accessible online

---

## 🐛 Troubleshooting

### Common Issues

**Import errors**
```bash
pip install --upgrade -r requirements.txt
```

**API key not found**
- Check `.env` has correct format
- Check `.streamlit/secrets.toml` exists
- Verify no spaces around `=` in `.env`

**Vector store errors**
```bash
rm -rf vector_stores/
# Restart app to rebuild
```

**Streamlit deployment fails**
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`
- Check logs in Streamlit Cloud dashboard

**Port already in use**
```bash
# Use different port
streamlit run app.py --server.port=8502
```

---

## 📚 Next Steps

After setup:
1. Read [QUICK_START_PRODUCTION.md](QUICK_START_PRODUCTION.md) for production tips
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment options
3. Explore calendar customization for your content schedule
4. Add your own knowledge base content for better RAG

---

## 🆘 Getting Help

- **Documentation**: README.md, DEPLOYMENT.md
- **Issues**: [GitHub Issues](https://github.com/CamelCod/content-agent-system/issues)
- **API**: [OpenRouter Docs](https://openrouter.ai/docs)
- **Streamlit**: [Streamlit Docs](https://docs.streamlit.io)

---

**Status Check**: If all boxes are checked, you're ready to generate content! 🎉
