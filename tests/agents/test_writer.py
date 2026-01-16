"""Tests for content writer agent."""

import pytest

from content_agent_system.agents.base import AgentConfig
from content_agent_system.agents.writer import ContentWriterAgent


def test_writer_agent_initialization():
    """Test writer agent initialization."""
    config = AgentConfig(name="writer", model="gpt-4")
    agent = ContentWriterAgent(config=config)
    assert agent.name == "writer"


@pytest.mark.asyncio
async def test_writer_agent_process():
    """Test writer agent processing."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)

    input_data = {"topic": "AI", "context": "test context", "style": "technical"}
    result = await agent.process(input_data)

    assert "content" in result
    assert "metadata" in result
    assert "AI" in result["content"]


@pytest.mark.asyncio
async def test_writer_agent_invalid_input():
    """Test writer agent with invalid input."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)

    with pytest.raises(ValueError):
        await agent.process({})


def test_writer_agent_validate_input():
    """Test writer agent input validation."""
    config = AgentConfig(name="writer")
    agent = ContentWriterAgent(config=config)

    assert agent.validate_input({"topic": "test"}) is True
    assert agent.validate_input({}) is False
