from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from enum import Enum


class AIProvider(str, Enum):
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"
    GROQ = "groq"
    DEMO = "demo"


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore", env_prefix="HELIX_")

    # Provider selection
    AI_PROVIDER: AIProvider = Field(default=AIProvider.DEMO, description="AI provider to use")

    # DeepSeek (OpenRouter)
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, description="OpenRouter API key")
    OPENROUTER_MODEL: str = Field(default="deepseek/deepseek-chat", description="DeepSeek model")

    # Ollama
    OLLAMA_HOST: str = Field(default="http://localhost:11434", description="Ollama server URL")
    OLLAMA_MODEL: str = Field(default="llama3", description="Ollama model")

    # Groq
    GROQ_API_KEY: Optional[str] = Field(default=None, description="Groq API key")
    GROQ_MODEL: str = Field(default="llama-3.1-70b-versatile", description="Groq model")

    # General settings
    AI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    AI_MAX_TOKENS: int = Field(default=2000, gt=0)
    AI_TIMEOUT: int = Field(default=30, gt=0)
    AI_AUTO_FALLBACK: bool = Field(default=True)

    CHAOS_ENABLED: bool = False
    CHAOS_ERROR_RATE: float = 0.1
    CHAOS_LATENCY_RATE: float = 0.15
    CHAOS_MIN_DELAY: int = 500
    CHAOS_MAX_DELAY: int = 2000


ai_settings = AISettings()
