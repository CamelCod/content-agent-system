"""Tests for content producer."""

import pytest

from content_agent_system.agents.base import AgentConfig
from content_agent_system.agents.writer import ContentWriterAgent
from content_agent_system.content.producer import ContentProducer
from content_agent_system.rag.knowledge_base import Document, KnowledgeBase


def test_content_producer_initialization():
    """Test content producer initialization."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])
    assert "writer" in producer.list_agents()


def test_content_producer_with_kb():
    """Test content producer with knowledge base."""
    kb = KnowledgeBase()
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent], knowledge_base=kb)
    assert producer.knowledge_base is not None
    assert producer.retriever is not None


@pytest.mark.asyncio
async def test_produce_content():
    """Test producing content."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])

    result = await producer.produce(
        agent_name="writer",
        input_data={"topic": "test"},
    )
    assert "content" in result


@pytest.mark.asyncio
async def test_produce_content_with_rag():
    """Test producing content with RAG."""
    kb = KnowledgeBase()
    kb.add_document(Document(id="doc1", content="Test context"))

    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent], knowledge_base=kb)

    result = await producer.produce(
        agent_name="writer",
        input_data={"topic": "test"},
        use_rag=True,
    )
    assert "content" in result


@pytest.mark.asyncio
async def test_produce_with_invalid_agent():
    """Test producing content with invalid agent name."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])

    with pytest.raises(ValueError):
        await producer.produce(
            agent_name="nonexistent",
            input_data={"topic": "test"},
        )


@pytest.mark.asyncio
async def test_produce_with_rag_no_kb():
    """Test producing content with RAG but no knowledge base."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])

    with pytest.raises(ValueError):
        await producer.produce(
            agent_name="writer",
            input_data={"topic": "test"},
            use_rag=True,
        )


def test_add_agent():
    """Test adding an agent."""
    producer = ContentProducer(agents=[])
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer.add_agent(agent)
    assert "writer" in producer.list_agents()


def test_remove_agent():
    """Test removing an agent."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])

    removed = producer.remove_agent("writer")
    assert removed is True
    assert "writer" not in producer.list_agents()


def test_remove_nonexistent_agent():
    """Test removing a nonexistent agent."""
    producer = ContentProducer(agents=[])
    removed = producer.remove_agent("nonexistent")
    assert removed is False


def test_content_producer_repr():
    """Test content producer string representation."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)
    producer = ContentProducer(agents=[agent])
    assert "ContentProducer" in repr(producer)
