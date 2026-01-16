# Getting Started

This guide will help you get started with the Content Agent System.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CamelCod/content-agent-system.git
cd content-agent-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e ".[dev]"
```

## Configuration

1. Copy the example environment file:
```bash
cp config/.env.example .env
```

2. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_key_here
```

## Quick Start

### Using the CLI

Run the example workflow:
```bash
content-agent
```

Or directly:
```bash
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
        content="AI is transforming content creation."
    ))
    
    # Create an agent
    config = AgentConfig(name="writer", model="gpt-4")
    agent = ContentWriterAgent(config=config)
    
    # Create a content producer
    producer = ContentProducer(agents=[agent], knowledge_base=kb)
    
    # Generate content
    result = await producer.produce(
        agent_name="writer",
        input_data={"topic": "AI in content"},
        use_rag=True
    )
    
    print(result["content"])

asyncio.run(main())
```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=content_agent_system --cov-report=html
```

## Code Quality

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

## Next Steps

- Check out [examples/basic_usage.py](../examples/basic_usage.py) for more examples
- Read the [Architecture](architecture.md) documentation
- Explore the [API Reference](api.md)
