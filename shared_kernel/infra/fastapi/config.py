from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DRIVER: ClassVar[str] = "sqlite"
    DATABASE: ClassVar[str] = "measurements.db"

    SQLALCHEMY_DATABASE_URL: ClassVar[str] = f"{DRIVER}:///{DATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
