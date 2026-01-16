"""Content writer agent for generating written content."""

from typing import Any, Dict

from content_agent_system.agents.base import AgentConfig, BaseAgent


class ContentWriterAgent(BaseAgent):
    """Agent specialized in writing content based on context and requirements."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the content writer agent.

        Args:
            config: Agent configuration
        """
        super().__init__(config)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content based on input.

        Args:
            input_data: Input containing topic, context, and requirements

        Returns:
            Generated content
        """
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data")

        topic = input_data.get("topic", "")
        context = input_data.get("context", "")
        style = input_data.get("style", "informative")

        # Placeholder for actual LLM integration
        content = f"Generated content about {topic} in {style} style with context: {context}"

        return {
            "content": content,
            "metadata": {
                "agent": self.name,
                "topic": topic,
                "style": style,
            },
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data.

        Args:
            input_data: Input data to validate

        Returns:
            True if input is valid
        """
        return "topic" in input_data
