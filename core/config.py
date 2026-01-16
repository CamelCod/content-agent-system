"""Configuration module for content agent system."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Free/Cheap Models
MODELS = {
    "free": "meta-llama/llama-3.1-8b-instruct:free",
    "cheap": "openai/gpt-3.5-turbo",
    "quality": "anthropic/claude-3-haiku",
}

DEFAULT_MODEL = MODELS["free"]

# Paths
KNOWLEDGE_BASE_DIR = "./knowledge_bases"
VECTOR_STORE_DIR = "./vector_stores"

# Quality Threshold
MIN_SCORE = 8.0

# Content Lenses
LENSES = ["incentives", "processes", "constraints", "narratives", "feedback", "metrics"]

# Objectives
OBJECTIVES = [
    "establish_credibility",
    "diagnose_failure",
    "translate_complexity",
    "reframe_belief",
    "advisory_perspective",
    "operator_insight"
]

# Signature Phrases
SIGNATURE_PHRASES = [
    "Systems beat skill",
    "Incentives create behavior",
    "Execution is a design problem",
]

# Core Thesis
CORE_THESIS = (
    "Systems beat skill. Incentives, processes, constraints, narratives, "
    "feedback loops, and metrics shape behavior more than individual capability."
)

# Voice Guidelines
VOICE_GUIDELINES = {
    "tone": "Clear, slightly contrarian, calm, practical",
    "style": "Grounded in lived experience",
    "banned": ["motivational language", "buzzwords", "emojis", "questions at end", "CTAs"],
    "format": "Short paragraphs (1-2 lines), declarative statements"
}
