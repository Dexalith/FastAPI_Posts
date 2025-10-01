import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECRET_KEY = os.environ['SECRET_KEY']
# ALGORITHM = os.environ['ALGORITHM']

class AppConfig(BaseSettings):
    project_name: str = "posts"
    app_host: str = "localhost"
    app_port: int = 8082

    cors_origins: list = ["*"]

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        extra="allow"
    )

class Config(BaseSettings):
    db_name: str = "your_db"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_username: str = "username"
    db_password: str = "password"
    db_logs: bool = False
    sqlalchemy_pool_size: int = 5
    sqlalchemy_pool_max_overflow: int = 10

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        extra="allow"
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class Setting(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_minutes_life: int = 30

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        extra="allow",
    )

settings = Setting() #  type: ignore
postgres_config = Config() # type: ignore
app_config = AppConfig()  # type: ignore