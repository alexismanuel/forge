from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class ORMClient:
    DEFAULT_POOL_SIZE = 5
    DEFAULT_MAX_OVERFLOW = 0
    _engine: AsyncEngine | None
    _session_maker: async_sessionmaker[AsyncSession] | None

    def __init__(self, db_url: str, engine_pool_size: int | None = None, max_overflow: int | None = None) -> None:
        self.db_url = db_url
        self.engine_pool_size = engine_pool_size or self.DEFAULT_POOL_SIZE
        self.max_overflow = max_overflow or self.DEFAULT_MAX_OVERFLOW
        self._engine = None
        self._session_maker = None

    @property
    def engine(self) -> AsyncEngine:
        if self._engine:
            return self._engine
        self._engine = create_async_engine(
            self.db_url,
            pool_pre_ping=True,
            pool_size=self.engine_pool_size,
            max_overflow=self.max_overflow,
        )
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        if self._session_maker:
            return self._session_maker
        self._session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
        return self._session_maker

    async def close(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

