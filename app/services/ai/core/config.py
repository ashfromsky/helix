from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
from enum import Enum


class AIProvider(str, Enum):
    DEEPSEEK = "deepseek"  # OpenRouter (free with key)
    OLLAMA = "ollama"  # local (free with key)
    GROQ = "groq"  # Groq (free with key)
    DEMO = "demo"  # built-in mocks (without AI)


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="HELIX_"
    )

    # provider selection (by default demo mode)
    AI_PROVIDER: AIProvider = Field(
        default=AIProvider.DEMO,
        description="AI provider to use (deepseek, ollama, groq, demo)"
    )

    # DeepSeek (OpenRouter)
    OPENROUTER_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenRouter API key for DeepSeek"
    )
    OPENROUTER_MODEL: str = Field(
        default="deepseek/deepseek-chat",
        description="Model to use on OpenRouter"
    )

    # Ollama (local version)
    OLLAMA_HOST: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL"
    )
    OLLAMA_MODEL: str = Field(
        default="llama3",
        description="Ollama model name"
    )

    # Groq
    GROQ_API_KEY: Optional[str] = Field(
        default=None,
        description="Groq API key"
    )
    GROQ_MODEL: str = Field(
        default="llama-3.1-70b-versatile",
        description="Groq model name"
    )

    # general settings
    AI_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="AI temperature (0.0 - 2.0)"
    )
    AI_MAX_TOKENS: int = Field(
        default=2000,
        gt=0,
        description="Maximum tokens in response"
    )
    AI_TIMEOUT: int = Field(
        default=30,
        gt=0,
        description="Request timeout in seconds"
    )

    AI_AUTO_FALLBACK: bool = Field(
        default=True,
        description="Auto fallback to demo mode if AI fails"
    )

# singleton pattern btw
ai_settings = AISettings()