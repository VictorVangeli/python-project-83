from alembic import command
from alembic.config import Config
from sqlalchemy import text

from page_analyzer.infrastructure.database.db_dependency import DBDependency


def test_prod_clean_db():
    db = DBDependency()
    engine = db.engine

    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def main():
    test_prod_clean_db()
