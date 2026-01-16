# Content Agent System

AI-powered content production system with RAG (Retrieval-Augmented Generation) knowledge base.

## 🚀 Features

- **Modular Agent System**: Extensible AI agents for various content production tasks
- **RAG Integration**: Knowledge base with retrieval-augmented generation for context-aware content
- **Multi-Agent Support**: Coordinate multiple specialized agents for complex workflows
- **Type-Safe**: Built with Pydantic for robust data validation
- **Async Support**: Asynchronous processing for efficient content generation
- **Extensible Architecture**: Easy to add custom agents, vector stores, and LLM providers

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/CamelCod/content-agent-system.git
cd content-agent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e ".[dev]"
```

## 🔧 Configuration

Create a `.env` file in the project root:

```bash
cp config/.env.example .env
```

Add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
```

## 🎯 Quick Start

### Using the CLI

```bash
# Run the example workflow
content-agent

# Or directly
python -m content_agent_system.cli
```

### Using as a Library

```python
import asyncio
from content_agent_system.agents import AgentConfig, ContentWriterAgent
from content_agent_system.content import ContentProducer
from content_agent_system.rag import KnowledgeBase, Document

async def main():
    # Create a knowledge base
    kb = KnowledgeBase()
    kb.add_document(Document(
        id="doc1",
        content="AI is transforming content creation with intelligent agents."
    ))
    
    # Create an agent
    config = AgentConfig(name="writer", model="gpt-4", temperature=0.7)
    agent = ContentWriterAgent(config=config)
    
    # Create a content producer
    producer = ContentProducer(agents=[agent], knowledge_base=kb)
    
    # Generate content with RAG
    result = await producer.produce(
        agent_name="writer",
        input_data={"topic": "AI in content creation", "style": "informative"},
        use_rag=True
    )
    
    print(result["content"])

asyncio.run(main())
```

## 📚 Documentation

- [Getting Started Guide](docs/getting_started.md)
- [Architecture Overview](docs/architecture.md)
- [Examples](examples/basic_usage.py)

## 🏗️ Project Structure

```
content-agent-system/
├── src/content_agent_system/
│   ├── agents/          # AI agents for content production
│   │   ├── base.py      # Base agent class
│   │   └── writer.py    # Content writer agent
│   ├── rag/             # RAG knowledge base system
│   │   ├── knowledge_base.py  # Document storage
│   │   └── retriever.py       # Document retrieval
│   ├── content/         # Content production orchestration
│   │   └── producer.py  # Content producer
│   ├── utils/           # Utility functions
│   ├── config.py        # Configuration management
│   └── cli.py           # Command-line interface
├── tests/               # Test suite
├── examples/            # Example scripts
├── docs/                # Documentation
└── config/              # Configuration files
```

## 🧪 Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=content_agent_system --cov-report=html
```

## 🛠️ Development

### Code Quality

Format code:
```bash
black src/ tests/
```

Lint code:
```bash
ruff check src/ tests/
```

Type checking:
```bash
mypy src/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🔮 Future Roadmap

- [ ] Integration with ChromaDB for production vector storage
- [ ] Streaming content generation
- [ ] Multi-modal content support (images, audio)
- [ ] Advanced agent orchestration patterns
- [ ] Web API interface
- [ ] More specialized agent types
- [ ] Performance optimization and caching
