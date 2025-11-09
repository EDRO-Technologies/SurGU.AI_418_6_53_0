from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.protocols.transaction_manager import TransactionManager
from app.infrastructure.sqla_persistance.transaction_manager import (
    SqlaTransactionManager,
)
from app.main.config import Config


class SqlaProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(
            url=config.postgres.database_dsn,
            echo=config.sqla.echo,
            pool_size=config.sqla.pool_size,
            max_overflow=config.sqla.max_overflow,
        )

    @provide(scope=Scope.APP)
    def provide_async_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    def provide_sqla_uow(
        self, async_session_maker: async_sessionmaker[AsyncSession]
    ) -> TransactionManager:
        return SqlaTransactionManager(async_session_maker=async_session_maker)
