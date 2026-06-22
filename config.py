import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # API Keys
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"  # openai or ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Telegram
    TG_BOT_TOKEN: str = ""
    TG_CHAT_ID: str = ""

    # SIP / PBX
    SIP_HOST: str = "127.0.0.1"
    SIP_PORT: int = 5060
    SIP_USER: str = "huginn"
    SIP_PASSWORD: str = ""

    # App Settings
    DETECTION_THRESHOLD: float = 0.7
    LOG_LEVEL: str = "INFO"

    # Data paths
    DB_PATH: str = "data/huginn.db"
    AUDIO_DIR: str = "data/audio"

settings = Settings()
