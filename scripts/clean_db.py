import asyncio

from sqlalchemy import delete

from page_analyzer.infrastructure.database.db_dependency import DBDependency
from page_analyzer.infrastructure.database.models import Urls


async def clean_db():
    async with DBDependency().db_session() as session:
        clean_db_query = delete(Urls)
        await session.execute(clean_db_query)
        await session.commit()

def main():
    asyncio.run(clean_db())