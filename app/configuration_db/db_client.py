import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.configuration_db.conf import postgres_config

logger = logging.getLogger(__name__)

class AsyncDb:
    def __init__(
    self,
    db_url: str,
    echo: bool,
    pool_size: int,
    max_overflow: int):
        self.engine = create_async_engine(
            url=db_url, echo=echo,
            pool_size=pool_size, max_overflow=max_overflow
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as err:
            logger.error(f"Got sqlalchemy error: {type(err)} - {str(err)}")
            await session.rollback()
            raise
        finally:
            await session.close()

async_db = AsyncDb(
    db_url=postgres_config.db_url,
    echo=postgres_config.db_logs,
    pool_size=postgres_config.sqlalchemy_pool_size,
    max_overflow=postgres_config.sqlalchemy_pool_max_overflow,
)