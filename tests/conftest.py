"""Common test fixtures and utilities."""

import pytest


@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "id": "test_doc",
        "content": "This is test content for the knowledge base.",
        "metadata": {"source": "test", "type": "sample"},
    }


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing."""
    from content_agent_system.agents.base import AgentConfig

    return AgentConfig(
        name="test_agent",
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
    )
