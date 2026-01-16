"""LinkedIn content generation agent."""

import random
from typing import Dict, Optional

from langchain_openai import ChatOpenAI

from core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
    CORE_THESIS,
    SIGNATURE_PHRASES,
)
from core.prompts import LINKEDIN_PROMPT
from core.knowledge_base import KnowledgeBase


class LinkedInAgent:
    """Agent for generating LinkedIn posts (150-250 words)."""
    
    def __init__(self, model: str = DEFAULT_MODEL, knowledge_base: Optional[KnowledgeBase] = None):
        """Initialize LinkedIn agent.
        
        Args:
            model: Model to use for generation
            knowledge_base: Optional knowledge base for RAG
        """
        self.model = model
        self.knowledge_base = knowledge_base or KnowledgeBase()
        
        # Initialize LLM with OpenRouter
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base=OPENROUTER_BASE_URL,
            temperature=0.7,
            max_tokens=1000
        )
        
    def generate(
        self,
        topic: str,
        lens: str,
        objective: str,
        use_rag: bool = True
    ) -> str:
        """Generate a LinkedIn post.
        
        Args:
            topic: Post topic
            lens: Primary content lens
            objective: Content objective
            use_rag: Whether to use RAG for context
            
        Returns:
            Generated LinkedIn post
        """
        # Get context from knowledge base if enabled
        context = ""
        if use_rag:
            try:
                context = self.knowledge_base.get_context(topic, lens, objective, k=3)
            except Exception as e:
                print(f"Warning: Could not retrieve context: {e}")
                context = "No context available."
        else:
            context = "No context available."
            
        # Select random signature phrase
        signature_phrase = random.choice(SIGNATURE_PHRASES)
        
        # Format prompt
        prompt = LINKEDIN_PROMPT.format(
            core_thesis=CORE_THESIS,
            topic=topic,
            lens=lens,
            objective=objective,
            context=context,
            signature_phrase=signature_phrase
        )
        
        # Generate content
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            return content
        except Exception as e:
            raise Exception(f"Error generating LinkedIn post: {e}")
            
    def generate_from_calendar(self, calendar_entry: Dict) -> str:
        """Generate post from calendar entry.
        
        Args:
            calendar_entry: Dict with topic, lens, objective keys
            
        Returns:
            Generated LinkedIn post
        """
        return self.generate(
            topic=calendar_entry["topic"],
            lens=calendar_entry["lens"],
            objective=calendar_entry["objective"]
        )
