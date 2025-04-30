from sqlalchemy import select, desc, insert

from page_analyzer.entities.named_tupples.urls_tupple import \
    UrlDataWithChecksTuple
from page_analyzer.entities.schemas.url_schema import UrlSchema, CheckSchema
from page_analyzer.entities.schemas.url_schema import UrlWithLastCheckSchema
from page_analyzer.infrastructure.database.db_dependency import DBDependency
from page_analyzer.infrastructure.database.models import Urls, UrlChecks


class UrlManager:
    def __init__(self) -> None:
        self._db = DBDependency()
        self.url_model = Urls
        self.checks_model = UrlChecks

    async def get_url_by_id(self, url_id: int):
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

    async def get_all_notes_by_url(self, url_id: int):
        async with self._db.db_session() as session:
            checks_query = (
                select(
                    self.checks_model,
                )
                .where(self.checks_model.url_id == url_id)
                .order_by(desc(self.checks_model.id))
            )

            result_checks = await session.execute(checks_query)
            checks = result_checks.scalars().all()

            url_data_query = (
                select(
                    self.url_model
                )
                .where(self.url_model.id == url_id)
            )

            result_url_data = await session.execute(url_data_query)
            url_data = result_url_data.scalar_one()

            return UrlDataWithChecksTuple(
                url_data=UrlSchema.model_validate(
                    url_data,
                    from_attributes=True
                ),
                checks_data=[
                    CheckSchema.model_validate(check, from_attributes=True)
                    for check in checks
                ],
            )

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
                select(
                    self.url_model.id,
                    self.url_model.name,
                    self.url_model.created_at,
                    self.checks_model.status_code,
                    self.checks_model.created_at.label("last_check"),
                )
                .outerjoin(self.checks_model,
                           self.url_model.id == self.checks_model.url_id)
                .distinct(self.url_model.id)
                .order_by(
                    desc(self.url_model.id), 
                    desc(self.checks_model.created_at)
                )
            )

            results_urls = await session.execute(query)
            await session.commit()
            urls = results_urls.all()

            return [
                UrlWithLastCheckSchema.model_validate(
                    url,
                    from_attributes=True)
                for url in urls
            ]

    async def add_check_result_for_url(self, url_data: CheckSchema):
        async with self._db.db_session() as session:
            query = (
                insert(
                    self.checks_model
                )
                .values(**url_data.model_dump(exclude_none=True))
            )
            await session.execute(query)
            await session.commit()
