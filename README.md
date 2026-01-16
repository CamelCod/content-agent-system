# Content Agent System

**AI-Powered Content Production System with RAG Knowledge Base**

A production-ready content generation system that creates LinkedIn posts, blog articles, and long-form content using AI agents with RAG (Retrieval-Augmented Generation), quality validation, and batch processing.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32-red.svg)

---

## 🎯 Core Features

- **RAG Knowledge Base**: ChromaDB vector store with HuggingFace embeddings for context-aware generation
- **Multiple Content Types**: LinkedIn posts (150-250 words), blog posts (800-1500 words), articles (1000-2000 words)
- **Quality Validation**: Automated scoring system with 8.0+ threshold enforcement
- **Batch Processing**: Generate multiple posts from pre-defined content calendar
- **Web Interface**: Full-featured Streamlit UI with calendar integration
- **Production Ready**: Deployment configs for Streamlit Cloud, Heroku, Railway, and more

---

## 🏗️ Architecture

### Core Thesis
> "Systems beat skill. Incentives, processes, constraints, narratives, feedback loops, and metrics shape behavior more than individual capability."

### Components

```
content-agent-system/
├── core/
│   ├── config.py          # Configuration and constants
│   ├── prompts.py         # Prompt templates
│   └── knowledge_base.py  # RAG implementation
├── agents/
│   ├── linkedin_agent.py  # LinkedIn post generator
│   ├── blog_agent.py      # Blog post generator
│   ├── article_agent.py   # Article generator
│   └── validator_agent.py # Quality validation
├── knowledge_bases/       # RAG knowledge sources
│   ├── voice_and_style/
│   ├── content_framework/
│   ├── reference/
│   └── examples/
├── app.py                 # Streamlit web UI
└── batch_processor.py     # Batch content generation
```

### Content Lenses
- **Incentives**: What drives behavior
- **Processes**: How work gets done
- **Constraints**: What limits action
- **Narratives**: Stories people tell
- **Feedback**: Information loops
- **Metrics**: What gets measured

### Objectives
- Establish credibility
- Diagnose failure modes
- Translate complexity
- Reframe beliefs
- Advisory perspective
- Operator insights

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenRouter API key ([get one here](https://openrouter.ai/keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CamelCod/content-agent-system.git
cd content-agent-system
```

2. **Run setup script**
```bash
./setup_repo.sh
```

3. **Configure API key**
```bash
# Edit .env
echo "OPENROUTER_API_KEY=your_key_here" > .env

# For Streamlit
echo "OPENROUTER_API_KEY = \"your_key_here\"" > .streamlit/secrets.toml
```

4. **Install dependencies**
```bash
./deploy.sh
```

5. **Run the application**
```bash
streamlit run app.py
```

The web interface will open at `http://localhost:8501`

---

## 📖 Usage

### Web Interface

**LinkedIn Post Generator**
- Custom topics with lens and objective selection
- Calendar mode for pre-defined posts
- Real-time validation with quality scores
- Content history with copy/delete

**Blog & Article Generators**
- Longer-form content generation
- Multi-lens analysis
- Structured output with sections
- RAG-enhanced context

**Batch Processor**
- Generate multiple posts from calendar
- Automatic retry on validation failure
- Progress tracking
- JSON export of results

### Command Line

**Generate single post**
```python
from agents.linkedin_agent import LinkedInAgent
from agents.validator_agent import ValidatorAgent

agent = LinkedInAgent()
content = agent.generate(
    topic="Process theater in organizations",
    lens="processes",
    objective="diagnose_failure"
)

validator = ValidatorAgent()
score, feedback, word_count = validator.validate(content, "LinkedIn", "150-250")
print(f"Score: {score}/10")
```

**Run batch processor**
```bash
python batch_processor.py
```

---

## 🎨 Content Calendar

The system includes a pre-defined content calendar for Weeks 2-4:

| Week | Post | Topic | Lens | Objective |
|------|------|-------|------|-----------|
| 2 | 4 | Process theater | processes | diagnose_failure |
| 2 | 5 | Motivation as tax | incentives | reframe_belief |
| 2 | 6 | Metrics optimization | metrics | translate_complexity |
| 3 | 7 | Good people, bad systems | constraints | reframe_belief |
| 3 | 8 | 3 things that change behavior | feedback | operator_insight |
| 3 | 9 | Hidden cost of misaligned incentives | incentives | diagnose_failure |
| 4 | 10 | Advisory approach | narratives | advisory_perspective |
| 4 | 11 | Optimization without alignment | processes | diagnose_failure |
| 4 | 12 | Rational resistance | constraints | reframe_belief |

---

## 🎯 Voice Guidelines

The system enforces these voice characteristics:

✅ **Required**
- Clear, slightly contrarian, calm, practical
- Grounded in lived experience
- Short paragraphs (1-2 lines)
- Declarative statements

❌ **Banned**
- Motivational language
- Buzzwords
- Emojis
- Questions at end
- CTAs (calls-to-action)

---

## 🔧 Configuration

### Models

The system supports multiple models via OpenRouter:

```python
MODELS = {
    "free": "meta-llama/llama-3.1-8b-instruct:free",
    "cheap": "openai/gpt-3.5-turbo",
    "quality": "anthropic/claude-3-haiku",
}
```

### RAG Settings

```python
# Vector store settings
chunk_size = 1500
chunk_overlap = 300
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval settings
k = 5  # Number of chunks to retrieve
```

### Validation

```python
MIN_SCORE = 8.0  # Minimum passing score
max_retries = 3  # Attempts per post
```

---

## 📦 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides.

### Streamlit Cloud (Recommended)

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add `OPENROUTER_API_KEY` to secrets
4. Deploy!

### Other Platforms

- **Heroku**: Uses `Procfile` and `runtime.txt`
- **Railway**: Auto-detects Streamlit app
- **Hugging Face Spaces**: Uses `requirements.txt`
- **Docker**: See DEPLOYMENT.md for Dockerfile

---

## 🧪 Testing

The system includes comprehensive validation:

```bash
# Test knowledge base
python -c "from core.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); kb.load_vector_store()"

# Test agent generation
python -c "from agents.linkedin_agent import LinkedInAgent; agent = LinkedInAgent()"

# Test validation
python -c "from agents.validator_agent import ValidatorAgent; v = ValidatorAgent()"

# Run batch processor
python batch_processor.py
```

---

## 📁 Knowledge Base

Add your content to these directories:

- `knowledge_bases/voice_and_style/`: Writing style guides
- `knowledge_bases/content_framework/`: Content frameworks
- `knowledge_bases/reference/`: Reference materials
- `knowledge_bases/examples/`: Example content

Supported formats: `.md`, `.txt`

The RAG system will automatically index all files.

---

## 🔒 Security

- Never commit `.env` or `.streamlit/secrets.toml`
- API keys are loaded from environment variables
- Vector stores are local and not committed

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- UI powered by [Streamlit](https://streamlit.io)
- Embeddings by [HuggingFace](https://huggingface.co)
- Vector store by [ChromaDB](https://www.trychroma.com)
- LLM routing by [OpenRouter](https://openrouter.ai)

---

## 📞 Support

- Documentation: [DEPLOYMENT.md](DEPLOYMENT.md), [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- Issues: [GitHub Issues](https://github.com/CamelCod/content-agent-system/issues)
- Quick Start: [QUICK_START_PRODUCTION.md](QUICK_START_PRODUCTION.md)

---

**Built with systems thinking. Powered by AI. Ready for production.** ✨
