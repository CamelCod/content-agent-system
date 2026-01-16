"""
Content Agent System - AI-powered content production system with RAG knowledge base.
"""

__version__ = "0.1.0"

from content_agent_system.agents.base import BaseAgent
from content_agent_system.rag.knowledge_base import KnowledgeBase
from content_agent_system.content.producer import ContentProducer

__all__ = [
    "BaseAgent",
    "KnowledgeBase",
    "ContentProducer",
]
