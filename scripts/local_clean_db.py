from sqlalchemy import delete

from page_analyzer.infrastructure.database.db_dependency import DBDependency
from page_analyzer.infrastructure.database.models import Urls


def local_clean_db():
    with DBDependency().db_session() as session:
        clean_db_query = delete(Urls)
        session.execute(clean_db_query)
        session.commit()


def main():
    local_clean_db()
