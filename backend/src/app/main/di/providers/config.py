from dishka import Provider, Scope, from_context, provide
from dishka.dependency_source.composite import CompositeDependencySource

from app.main.config import (
    AppConfig,
    BotConfig,
    Config,
    JWTConfig,
    OpenRouterConfig,
    RAGConfig,
    RedisConfig,
    SaluteConfig,
    SqlaConfig,
    WhisperConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP
    config: CompositeDependencySource = from_context(Config)

    @provide
    def provide_appconfig(self, config: Config) -> AppConfig:
        return config.app

    @provide
    def provide_botconfig(self, config: Config) -> BotConfig:
        return config.bot

    @provide
    def provide_redisconfig(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def provide_sqlaconfig(self, config: Config) -> SqlaConfig:
        return config.sqla

    @provide
    def provide_jwtconfig(self, config: Config) -> JWTConfig:
        return config.jwt

    @provide
    def provide_openrouterconfig(self, config: Config) -> OpenRouterConfig:
        return config.openrouter

    @provide
    def provide_ragconfig(self, config: Config) -> RAGConfig:
        return config.rag

    @provide
    def provide_saluteconfig(self, config: Config) -> SaluteConfig:
        return config.salute

    @provide(scope=Scope.APP)
    def provide_whisper_config(self, config: Config) -> WhisperConfig:
        return config.whisper
