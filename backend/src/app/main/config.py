from os import environ
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn

BASE_DIR = Path(__file__).parent.parent.parent.parent


class AppConfig(BaseModel):
    allow_origins: list[str] = Field(
        alias="APP_ALLOW_ORIGINS",
        default=["*"],
    )
    docs_url: str = Field(alias="APP_DOCS_URL", default="/docs")
    openapi_url: str = Field(alias="APP_OPENAPI_URL", default="/openapi.json")
    prefix: str = Field(alias="APP_PREFIX_API", default="/api")
    documents_dir: Path = Field(
        alias="APP_DOCUMENTS_PATH", default=Path(BASE_DIR / "documents")
    )
    max_document_size: int = Field(default=10485760)
    allowed_extensions: set[str] = Field(
        default={
            ".pdf",
            ".txt",
            ".md",
            ".log",
            ".json",
            ".csv",
            ".xml",
            ".docx",
            ".rtf",
        }
    )


class BotConfig(BaseModel):
    token: str = Field(alias="BOT_TOKEN")


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT", default=6379)
    num_db: int = Field(alias="REDIS_NUM_DB", default=1)


class JWTConfig(BaseModel):
    expire_at_seconds: int = Field(
        alias="JWT_EXPIRE_TIME_SECONDS", default=1800
    )
    alghorithm: str = "RS256"
    public_key: Path = BASE_DIR / "private_keys" / "jwt-public.pem"
    private_key: Path = BASE_DIR / "private_keys" / "jwt-private.pem"


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    username: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def database_dsn(self) -> str:
        return str(
            PostgresDsn.build(  # pyright: ignore
                scheme="postgresql+asyncpg",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.database,
            )
        )


class SqlaConfig(BaseModel):
    echo: bool = Field(alias="SQLA_ECHO", default=False)
    pool_size: int = Field(alias="SQLA_POOL_SIZE", default=15)
    max_overflow: int = Field(alias="SQLA_MAX_OVERFLOW", default=15)


class LoggingConfig(BaseModel):
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = Field(alias="LOG_LEVEL", default="INFO")


class SaluteConfig(BaseModel):
    auth_basic: str = Field(alias="SALUTE_AUTH_BASIC")
    rq_uid: str = Field(alias="SALUTE_RQ_UID")


class OpenRouterConfig(BaseModel):
    api_key: str = Field(
        alias="OPENROUTER_API_KEY",)
    model: str = Field(default="deepseek/deepseek-chat-v3.1")
    base_url: str = Field(default="https://openrouter.ai/api/v1")


class RAGConfig(BaseModel):
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)
    top_k: int = Field(default=5)
    vector_db_path: Path = Field(default=Path(BASE_DIR / "./vector_db"))
    indexing_interval: int = Field(default=60)


class WhisperConfig(BaseModel   ):
    groq_api_key: str = Field(alias="GROQ_API_KEY")


class Config(BaseModel):
    app: AppConfig = Field(
        default_factory=lambda: AppConfig(**environ)  # pyright: ignore
    )
    bot: BotConfig = Field(
        default_factory=lambda: BotConfig(**environ)  # pyright: ignore
    )
    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig(**environ)  # pyright: ignore
    )
    jwt: JWTConfig = Field(
        default_factory=lambda: JWTConfig(**environ)  # pyright: ignore
    )
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**environ)  # pyright: ignore
    )
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**environ)  # pyright: ignore
    )
    openrouter: OpenRouterConfig = Field(
        default_factory=lambda: OpenRouterConfig(**environ)  # pyright: ignore
    )
    sqla: SqlaConfig = Field(default_factory=lambda: SqlaConfig(**environ))  # pyright: ignore
    salute: SaluteConfig = Field(
        default_factory=lambda: SaluteConfig(**environ)  # pyright: ignore
    )
    rag: RAGConfig = Field(
        default_factory=lambda: RAGConfig(**environ)  # pyright: ignore
    )
    whisper: WhisperConfig = Field(
        default_factory=lambda: WhisperConfig(**environ)  # pyright: ignore
    )
