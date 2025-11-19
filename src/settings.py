from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Project Settings
    (from 'docker-compose.yml')
    """

    database_driver: str = Field(alias="DATABASE_DRIVER", default="postgresql")
    
    database_username: str = Field(
        alias="DATABASE_USERNAME", 
        default="user" 
    )
    database_password: str = Field(
        alias="DATABASE_PASSWORD", 
        default="password" 
    )
    database_host: str = Field(
        alias="DATABASE_HOST", 
        default="database" 
    )
    database_port: int = Field(
        alias="DATABASE_PORT", 
        default=5432
    )
    database_name: str = Field(
        alias="DATABASE_NAME", 
        default="db" 
    )


settings = Settings()

