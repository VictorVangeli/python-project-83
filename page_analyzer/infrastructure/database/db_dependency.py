from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker, 
                                    create_async_engine)

from page_analyzer.core.Base.singleton import Singleton
from page_analyzer.core.settings import get_settings


class DBDependency(Singleton):
    def __init__(self) -> None:
        self._engine = create_async_engine(url=get_settings().DATABASE_URL)
        self._session_factory = async_sessionmaker(bind=self._engine, 
                                                   expire_on_commit=False,
                                                   autocommit=False)

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
