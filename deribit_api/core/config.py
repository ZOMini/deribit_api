from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    postgres_db: str = Field(...)
    postgres_user: str = Field(...)
    postgres_password: str = Field(...)
    postgres_host: str = Field(...)
    postgres_port: int = Field(...)
    data_base: str = ''
    data_base_sync: str = ''

    main_timeout: float = Field(...)
    max_connections: int = Field(...)

    currencies_url: str = Field(...)
    currencies: list = Field(...)

    debug: bool = Field(...)
    scheduler_interval: int = Field(...)

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()  # type: ignore[call-arg]
settings.data_base = f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}'
settings.data_base_sync = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}'
