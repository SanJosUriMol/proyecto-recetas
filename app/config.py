from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "mistralai/mistral-7b-instruct"

    class Config:
        env_file = ".env"

settings = Settings()
