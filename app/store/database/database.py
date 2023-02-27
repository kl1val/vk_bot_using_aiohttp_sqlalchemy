from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.store.database import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None
        self.schema = "postgresql+asyncpg://"
        self.user: str = self.app.config.database.user
        self.pass_: str = self.app.config.database.password
        self.host: str = self.app.config.database.host
        self.port: int = self.app.config.database.port
        self.data_base: str = self.app.config.database.database
        self.url_ = f"{self.schema}{self.user}:{self.pass_}@{self.host}:{self.port}/{self.data_base}"


    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(self.url_, echo=False, future=True)
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
