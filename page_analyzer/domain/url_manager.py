import uuid

from sqlalchemy import select, desc, insert, asc

from page_analyzer.entities.schemas.url_schema import UrlSchema
from page_analyzer.infrastructure.database.db_dependency import DBDependency
from page_analyzer.infrastructure.database.models import Urls


class UrlManager:
    def __init__(self) -> None:
        self._db = DBDependency()
        self.url_model = Urls

    async def get_url_by_id(self, url_id: uuid.UUID):
        async with self._db.db_session() as session:
            query = (
                select(
                    self.url_model.id,
                    self.url_model.name,
                    self.url_model.created_at
                )
                .where(self.url_model.id == url_id)
                .order_by(desc(self.url_model.created_at))
            )
            result = await session.execute(query)
            return UrlSchema(**result.mappings().first())

    async def get_url_by_name(self, name: str):
        async with self._db.db_session() as session:
            query = (
                select(
                    self.url_model.id,
                    self.url_model.name,
                    self.url_model.created_at
                )
                .where(self.url_model.name == name)
                .order_by(desc(self.url_model.created_at))
            )
            result = (await session.execute(query)).mappings().first()
            if result is None:
                return None
            return UrlSchema(**result)

    # async def get_all_notes_by_url(self, url_id: uuid.UUID):
    #     async with self._db.db_session() as session:
    #         query = (
    #             select(
    # 
    #             )
    #         )
    # 
    async def add_url(self, name: str):
        async with self._db.db_session() as session:
            query = insert(self.url_model).values(name=name).returning(
                self.url_model)
            result = (await session.execute(query)).scalar_one()
            await session.commit()
            return UrlSchema.model_validate(result, from_attributes=True)

    async def get_all_urls(self):
        async with self._db.db_session() as session:
            query = (
                select(self.url_model).order_by(asc(self.url_model.created_at))
            )
            results_urls = await session.execute(query)
            await session.commit()
            urls = results_urls.scalars().all()
            return [
                UrlSchema.model_validate(
                    url,
                    from_attributes=True)
                for url in urls
            ]
