"""Blog post generation agent."""

import random
from typing import Optional

from langchain_openai import ChatOpenAI

from core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
    CORE_THESIS,
    SIGNATURE_PHRASES,
)
from core.prompts import BLOG_PROMPT
from core.knowledge_base import KnowledgeBase


class BlogAgent:
    """Agent for generating blog posts (800-1500 words)."""
    
    def __init__(self, model: str = DEFAULT_MODEL, knowledge_base: Optional[KnowledgeBase] = None):
        """Initialize blog agent.
        
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
            max_tokens=2500
        )
        
    def generate(
        self,
        topic: str,
        lens: str,
        objective: str,
        use_rag: bool = True
    ) -> str:
        """Generate a blog post.
        
        Args:
            topic: Post topic
            lens: Primary content lens
            objective: Content objective
            use_rag: Whether to use RAG for context
            
        Returns:
            Generated blog post
        """
        # Get context from knowledge base if enabled
        context = ""
        if use_rag:
            try:
                context = self.knowledge_base.get_context(topic, lens, objective, k=5)
            except Exception as e:
                print(f"Warning: Could not retrieve context: {e}")
                context = "No context available."
        else:
            context = "No context available."
            
        # Select random signature phrase
        signature_phrase = random.choice(SIGNATURE_PHRASES)
        
        # Format prompt
        prompt = BLOG_PROMPT.format(
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
            raise Exception(f"Error generating blog post: {e}")
