"""Tests for base agent."""

import pytest

from content_agent_system.agents.base import AgentConfig, BaseAgent


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    async def process(self, input_data):
        """Process input."""
        return {"result": "mock_result"}

    def validate_input(self, input_data):
        """Validate input."""
        return True


def test_agent_config():
    """Test agent configuration."""
    config = AgentConfig(name="test_agent", model="gpt-4", temperature=0.7)
    assert config.name == "test_agent"
    assert config.model == "gpt-4"
    assert config.temperature == 0.7


def test_base_agent_initialization():
    """Test base agent initialization."""
    config = AgentConfig(name="test_agent")
    agent = MockAgent(config=config)
    assert agent.name == "test_agent"
    assert agent.config.name == "test_agent"


@pytest.mark.asyncio
async def test_agent_process():
    """Test agent processing."""
    config = AgentConfig(name="test_agent")
    agent = MockAgent(config=config)
    result = await agent.process({"test": "data"})
    assert result == {"result": "mock_result"}


def test_agent_repr():
    """Test agent string representation."""
    config = AgentConfig(name="test_agent")
    agent = MockAgent(config=config)
    assert "MockAgent" in repr(agent)
    assert "test_agent" in repr(agent)
