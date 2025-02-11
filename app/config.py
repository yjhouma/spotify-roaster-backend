from pydantic_settings import BaseSettings
from functools import cache

class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    FRONTEND_URL: str

    
    class Config:
        env_file = ".env"

# @cache
def get_settings():
    return Settings()