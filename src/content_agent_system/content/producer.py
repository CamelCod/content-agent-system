"""Content producer for orchestrating content generation."""

from typing import Any, Dict, List, Optional

from content_agent_system.agents.base import BaseAgent
from content_agent_system.rag.knowledge_base import KnowledgeBase
from content_agent_system.rag.retriever import Retriever


class ContentProducer:
    """Orchestrates content production using agents and RAG."""

    def __init__(
        self,
        agents: List[BaseAgent],
        knowledge_base: Optional[KnowledgeBase] = None,
    ) -> None:
        """Initialize the content producer.

        Args:
            agents: List of agents to use for content production
            knowledge_base: Optional knowledge base for RAG
        """
        self.agents = {agent.name: agent for agent in agents}
        self.knowledge_base = knowledge_base
        self.retriever = Retriever(knowledge_base) if knowledge_base is not None else None

    async def produce(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        use_rag: bool = False,
    ) -> Dict[str, Any]:
        """Produce content using specified agent.

        Args:
            agent_name: Name of the agent to use
            input_data: Input data for the agent
            use_rag: Whether to use RAG for context enrichment

        Returns:
            Generated content and metadata

        Raises:
            ValueError: If agent not found or RAG requested but not available
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found")

        agent = self.agents[agent_name]

        # Enhance input with RAG context if requested
        if use_rag:
            if not self.retriever:
                raise ValueError("RAG requested but no knowledge base available")

            query = input_data.get("topic", "")
            relevant_docs = self.retriever.retrieve(query, top_k=3)
            input_data["context"] = " ".join([doc.content for doc in relevant_docs])

        # Generate content
        result = await agent.process(input_data)

        return result

    def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the producer.

        Args:
            agent: Agent to add
        """
        self.agents[agent.name] = agent

    def remove_agent(self, agent_name: str) -> bool:
        """Remove an agent from the producer.

        Args:
            agent_name: Name of agent to remove

        Returns:
            True if agent was removed, False otherwise
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False

    def list_agents(self) -> List[str]:
        """List all available agents.

        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    def __repr__(self) -> str:
        """String representation of the content producer."""
        return f"ContentProducer(agents={len(self.agents)}, has_kb={self.knowledge_base is not None})"
