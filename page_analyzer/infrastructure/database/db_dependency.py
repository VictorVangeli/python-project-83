from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from page_analyzer.core.Base.singleton import Singleton
from page_analyzer.core.settings import get_db_settings


class DBDependency(Singleton):
    def __init__(self) -> None:
        self._engine = create_engine(
            url=get_db_settings(),
            echo=False,
        )
        self._session_factory = sessionmaker(bind=self._engine, autoflush=False)

    @property
    def db_session(self) -> sessionmaker[Session]:
        return self._session_factory

    @property
    def engine(self):
        return self._engine
