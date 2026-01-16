"""Base agent class for content production agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str = Field(..., description="Name of the agent")
    model: str = Field(default="gpt-4", description="LLM model to use")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens to generate")


class BaseAgent(ABC):
    """Base class for all content production agents."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.name = config.name

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and generate output.

        Args:
            input_data: Input data for the agent

        Returns:
            Output data from the agent
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data.

        Args:
            input_data: Input data to validate

        Returns:
            True if input is valid, False otherwise
        """
        pass

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name={self.name})"
