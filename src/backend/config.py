from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # REQ-SEC-02: LLM API keys must be stored in .env
    openai_api_key: str = "your-openai-key"
    gemini_api_key: str = "your-gemini-key"
    
    # App Config
    pc_name: str = "My-Workstation"
    api_key: str = "DEV-SECRET-KEY-123"
    db_path: str = "remote_controller.db"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # REQ-AI-05: Privacy Mode Default
    privacy_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
