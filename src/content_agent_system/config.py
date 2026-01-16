"""Configuration management for the content agent system."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API Keys
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")

    # Model Settings
    default_model: str = Field(default="gpt-4", description="Default LLM model")
    temperature: float = Field(default=0.7, description="Default temperature")
    max_tokens: int = Field(default=2000, description="Default max tokens")

    # Knowledge Base Settings
    kb_collection_name: str = Field(
        default="content_kb", description="Knowledge base collection name"
    )
    kb_embedding_model: str = Field(
        default="text-embedding-ada-002", description="Embedding model for KB"
    )

    # System Settings
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")


# Global settings instance
settings = Settings()
