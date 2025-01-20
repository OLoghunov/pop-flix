from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    KINOPOISK_API_KEY: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
Config = Settings()