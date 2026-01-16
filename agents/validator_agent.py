"""Content validation agent."""

import re
from typing import Dict, Tuple

from langchain_openai import ChatOpenAI

from core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
    MIN_SCORE,
)
from core.prompts import VALIDATION_PROMPT


class ValidatorAgent:
    """Agent for validating content quality."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize validator agent.
        
        Args:
            model: Model to use for validation
        """
        self.model = model
        
        # Initialize LLM with OpenRouter
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base=OPENROUTER_BASE_URL,
            temperature=0.3,
            max_tokens=1000
        )
        
    def validate(
        self,
        content: str,
        content_type: str,
        target_words: str
    ) -> Tuple[float, str, int]:
        """Validate content quality.
        
        Args:
            content: Content to validate
            content_type: Type (LinkedIn, Blog, Article)
            target_words: Target word count range
            
        Returns:
            Tuple of (score, feedback, word_count)
        """
        # Quick checks for banned elements
        # Use a more robust emoji detection pattern
        emoji_pattern = r'[\U0001F300-\U0001F9FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U00002600-\U000027BF]'
        has_emoji = bool(re.search(emoji_pattern, content))
        ends_with_question = content.strip().endswith('?')
        
        # Count words
        word_count = len(content.split())
        
        # Format prompt
        prompt = VALIDATION_PROMPT.format(
            content=content,
            content_type=content_type,
            target_words=target_words
        )
        
        # Get validation from LLM
        try:
            response = self.llm.invoke(prompt)
            validation_text = response.content
            
            # Parse score
            score = self._parse_score(validation_text)
            
            # Add penalties for quick checks
            if has_emoji:
                score = max(0, score - 2.0)
                validation_text += "\n- PENALTY: Contains emojis (-2.0)"
                
            if ends_with_question:
                score = max(0, score - 1.0)
                validation_text += "\n- PENALTY: Ends with question (-1.0)"
                
            return score, validation_text, word_count
            
        except Exception as e:
            return 0.0, f"Error during validation: {e}", word_count
            
    def _parse_score(self, validation_text: str) -> float:
        """Parse score from validation response.
        
        Args:
            validation_text: Raw validation response
            
        Returns:
            Parsed score (0-10)
        """
        # Look for SCORE: pattern
        match = re.search(r'SCORE:\s*(\d+\.?\d*)', validation_text)
        if match:
            try:
                score = float(match.group(1))
                return min(10.0, max(0.0, score))
            except ValueError:
                pass
                
        # Default to failing score if can't parse
        return 0.0
        
    def is_passing(self, score: float) -> bool:
        """Check if score meets minimum threshold.
        
        Args:
            score: Validation score
            
        Returns:
            True if score >= MIN_SCORE
        """
        return score >= MIN_SCORE
        
    def validate_with_retry(
        self,
        content: str,
        content_type: str,
        target_words: str,
        max_retries: int = 3
    ) -> Dict:
        """Validate content with automatic retry logic.
        
        Args:
            content: Content to validate
            content_type: Type (LinkedIn, Blog, Article)
            target_words: Target word count range
            max_retries: Maximum validation attempts
            
        Returns:
            Dict with validation results
        """
        for attempt in range(max_retries):
            score, feedback, word_count = self.validate(
                content, content_type, target_words
            )
            
            if self.is_passing(score):
                return {
                    "passed": True,
                    "score": score,
                    "feedback": feedback,
                    "word_count": word_count,
                    "attempts": attempt + 1
                }
                
        # Final attempt failed
        return {
            "passed": False,
            "score": score,
            "feedback": feedback,
            "word_count": word_count,
            "attempts": max_retries
        }
