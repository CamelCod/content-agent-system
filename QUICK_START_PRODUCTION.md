# Quick Start: Production Deployment

Get your Content Agent System deployed to production in 5 minutes.

---

## 🚀 5-Minute Deployment (Streamlit Cloud)

The fastest path to production.

### Prerequisites
- GitHub account
- OpenRouter API key ([get free key](https://openrouter.ai/keys))
- 5 minutes

---

## Step 1: Fork & Clone (1 min)

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR_USERNAME/content-agent-system.git
cd content-agent-system
```

---

## Step 2: Get API Key (1 min)

1. Visit [OpenRouter Keys](https://openrouter.ai/keys)
2. Sign up (free)
3. Create new key
4. Copy key to clipboard

---

## Step 3: Deploy to Streamlit Cloud (2 min)

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Click "New app"**
3. **Fill in**:
   - Repository: `YOUR_USERNAME/content-agent-system`
   - Branch: `main`
   - Main file path: `app.py`
4. **Click "Advanced settings"**
5. **Add to Secrets**:
   ```toml
   OPENROUTER_API_KEY = "paste_your_key_here"
   ```
6. **Click "Deploy"**

---

## Step 4: Test (1 min)

Once deployed (takes 2-3 minutes):

1. **Open your app** (URL shown in dashboard)
2. **Navigate to "LinkedIn Generator"**
3. **Test generation**:
   - Topic: "Why process beats talent"
   - Lens: "processes"
   - Objective: "diagnose_failure"
   - Click "Generate Post"
4. **Verify**: Content appears with validation score

---

## ✅ You're Live!

Your content agent system is now:
- ✅ Deployed to production
- ✅ Accessible via URL
- ✅ Using free AI models
- ✅ Ready to generate content

**Your app URL**: `https://YOUR_APP_NAME.streamlit.app`

---

## 🎯 Next: Customize

### Add Your Content Calendar

Edit `batch_processor.py`:

```python
CONTENT_CALENDAR = [
    {
        "week": 1,
        "post_number": 1,
        "topic": "Your custom topic",
        "lens": "incentives",
        "objective": "establish_credibility"
    },
    # Add more...
]
```

### Add Knowledge Base

```bash
# Add your content
echo "Your style guide" > knowledge_bases/voice_and_style/guide.md
echo "Example post" > knowledge_bases/examples/linkedin_posts/example1.md

# Commit and push
git add knowledge_bases/
git commit -m "Add knowledge base"
git push

# Streamlit Cloud will auto-redeploy
```

### Customize Voice

Edit `core/config.py`:

```python
SIGNATURE_PHRASES = [
    "Your custom phrase",
    "Another signature line",
]

CORE_THESIS = "Your core thesis about content/systems"
```

---

## 🔧 Production Configuration

### Model Selection

**Default (Free)**
```python
DEFAULT_MODEL = MODELS["free"]  # Llama 3.1 8B
```

**Upgrade for Quality**
```python
DEFAULT_MODEL = MODELS["quality"]  # Claude Haiku
```

### Validation Threshold

**Stricter**
```python
MIN_SCORE = 9.0  # Only top-tier content
```

**More Lenient**
```python
MIN_SCORE = 7.5  # Allow more content through
```

### RAG Settings

**More Context**
```python
# In knowledge_base.py get_context()
chunks = self.search(query, k=10)  # More chunks
```

**Longer Chunks**
```python
# In knowledge_base.py build_vector_store()
chunk_size=2000,  # Larger chunks
chunk_overlap=400
```

---

## 📊 Production Monitoring

### Streamlit Cloud

**Built-in Analytics**
- Users count
- Page views
- Session duration
- Error logs

**Access**: App dashboard → Analytics tab

### OpenRouter

**API Usage**
- Token consumption
- Cost tracking
- Model performance

**Access**: [OpenRouter Activity](https://openrouter.ai/activity)

---

## 🔒 Production Security

### Required

✅ **API Keys**
- Always use Streamlit secrets
- Never commit `.env`
- Rotate keys periodically

✅ **Access Control**
- Streamlit Cloud: Configure app visibility
- Enterprise: Add authentication

✅ **Monitoring**
- Set up usage alerts
- Monitor error logs
- Track API costs

### Optional

🔐 **Add Authentication**

Install:
```bash
pip install streamlit-authenticator
```

Add to `app.py`:
```python
import streamlit_authenticator as stauth

# Configure authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

---

## 🚀 Scaling

### Performance Optimization

**1. Pre-build Vector Store**
```python
# Run once locally
from core.knowledge_base import KnowledgeBase
kb = KnowledgeBase()
kb.build_vector_store()

# Commit vector_stores/ (remove from .gitignore)
git add vector_stores/
git commit -m "Pre-built vector store"
git push
```

**2. Cache Knowledge Base**
```python
@st.cache_resource
def get_knowledge_base():
    kb = KnowledgeBase()
    kb.load_vector_store()
    return kb
```

**3. Optimize Models**
- Use "cheap" model for validation
- Use "quality" model only for final generation
- Batch API calls when possible

### Horizontal Scaling

**Multiple Deployments**
```bash
# Create multiple apps for different use cases
- content-agent-linkedin  # LinkedIn only
- content-agent-blog      # Blog only
- content-agent-batch     # Batch processing only
```

**Load Balancing**
- Use Railway/Heroku for auto-scaling
- Deploy to multiple regions
- Use CDN for static assets

---

## 💰 Cost Management

### Free Tier Limits

**Streamlit Cloud**
- 1 app (free)
- Unlimited viewers
- 1GB RAM

**OpenRouter**
- Free models: Llama 3.1 8B (unlimited)
- Paid models: ~$0.15 per 1M tokens

### Cost Optimization

**1. Use Free Models**
```python
DEFAULT_MODEL = MODELS["free"]  # Always free
```

**2. Limit Retries**
```python
max_retries = 2  # Instead of 3
```

**3. Reduce Context**
```python
# Use fewer RAG chunks
context = kb.get_context(topic, lens, objective, k=3)  # Instead of 5
```

**4. Cache Aggressively**
```python
@st.cache_data(ttl=3600)
def generate_cached(topic, lens, objective):
    # Cache for 1 hour
    pass
```

### Monitoring Costs

**Daily Check**
```bash
# Check OpenRouter dashboard
https://openrouter.ai/activity

# Set up budget alerts
https://openrouter.ai/settings
```

---

## 🔄 Updates & Maintenance

### Auto-Update Setup

**Streamlit Cloud**
- Automatically redeploys on `git push`
- No manual action needed
- Check deploy logs for errors

**Process**
```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push

# Streamlit auto-deploys in 2-3 minutes
```

### Dependency Updates

**Monthly Check**
```bash
pip list --outdated

# Update specific packages
pip install --upgrade streamlit langchain

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 📈 Production Metrics

### Track These KPIs

**Usage**
- Posts generated per day
- Unique users
- Validation pass rate

**Quality**
- Average validation score
- Retry rate
- User satisfaction

**Performance**
- Generation time
- API response time
- Error rate

**Cost**
- API cost per post
- Monthly total cost
- Cost per user

---

## 🎓 Production Best Practices

### Content Quality

✅ **Always validate**
- Don't skip validation
- Review low-scoring content
- Iterate on prompts

✅ **Use RAG**
- Populate knowledge base
- Update regularly
- Track which content helps

✅ **Monitor output**
- Review generated content
- Collect feedback
- Refine over time

### System Reliability

✅ **Error handling**
- Graceful degradation
- User-friendly error messages
- Fallback options

✅ **Logging**
- Track generation attempts
- Log validation scores
- Monitor API usage

✅ **Backups**
- Export content regularly
- Backup knowledge base
- Version control everything

---

## 🆘 Production Support

### Common Issues

**Slow generation**
- Switch to faster model
- Reduce RAG chunks
- Check API latency

**High costs**
- Use free models
- Reduce retries
- Cache more aggressively

**Quality issues**
- Improve knowledge base
- Adjust prompts
- Increase validation threshold

### Getting Help

- **Docs**: Check README.md, DEPLOYMENT.md
- **Logs**: Streamlit Cloud → Manage app → Logs
- **API**: OpenRouter dashboard → Activity
- **Community**: GitHub Issues

---

## 🎉 Success!

Your content agent system is now:
- ✅ **Live in production**
- ✅ **Generating quality content**
- ✅ **Monitored and optimized**
- ✅ **Ready to scale**

---

## 📚 Further Reading

- [DEPLOYMENT.md](DEPLOYMENT.md) - Advanced deployment options
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Detailed setup guide
- [README.md](README.md) - Full documentation

---

**Pro Tip**: Start with free models, validate quality, then upgrade to paid models only if needed. Most use cases work great with Llama 3.1 8B! 🚀
