from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./netfaultlab.db")
    cors_origins: List[str] = Field(default=["http://localhost:8000"])
    log_level: str = Field(default="INFO")

    class Config:
        env_prefix = "NETFAULTLAB_"

@lru_cache()
def get_settings() -> Settings:
    return Settings()