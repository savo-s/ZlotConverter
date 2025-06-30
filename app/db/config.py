from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Currency Wallet API"
    database_url: str = "sqlite:///./database.db"
    jwt_secret: str = "secret_key"
    jwt_algorithm: str = "HS256"
    cache_timeout: int = 300  # 5 minutes in seconds


settings = Settings()
