from sqlalchemy import desc, insert, select

from page_analyzer.entities.named_tupples.urls_tupple import (
    UrlDataWithChecksTuple,
)
from page_analyzer.entities.schemas.url_schema import (
    CheckSchema,
    UrlSchema,
    UrlWithLastCheckSchema,
)
from page_analyzer.infrastructure.database.db_dependency import DBDependency
from page_analyzer.infrastructure.database.models import UrlChecks, Urls


class UrlManager:
    def __init__(self) -> None:
        self._db = DBDependency()
        self.url_model = Urls
        self.checks_model = UrlChecks

    def get_url_by_id(self, url_id: int):
        """
        Возвращает полностью объект добавленного URL по его идентификатору или
        None.

        :param self: Экземпляр менеджера URL-адресов.
        :param url_id: Идентификатор URL.
        :type url_id: int
        :returns: Информация о URL в виде схемы UrlSchema или None.
        :rtype: UrlSchema or None
        """
        with self._db.db_session() as session:
            query = select(self.url_model).where(self.url_model.id == url_id)
            result = (session.execute(query)).scalar_one_or_none()
            if result is None:
                return None
            return UrlSchema.model_validate(result, from_attributes=True)

    def get_url_by_name(self, name: str):
        """
        Возвращает URL по указанной ссылке или None.

        :param self: Экземпляр менеджера URL-адресов.
        :param name: URL, которое нужно найти.
        :type name: str
        :returns: Схема URL, соответствующая заданному имени, или None, если URL
            не найден.
        :rtype: UrlSchema or None
        """
        with self._db.db_session() as session:
            query = select(self.url_model).where(self.url_model.name == name)
        result = (session.execute(query)).scalar_one_or_none()
        if result is None:
            return None
        return UrlSchema.model_validate(result, from_attributes=True)

    def get_all_records_by_url(self, url_id: int) -> UrlDataWithChecksTuple:
        """
        Возвращает все записи для конкретного URL и информацию о добавленном
        URL.

        :param self: Экземпляр менеджера URL-адресов.
        :param url_id: Идентификатор URL для поиска заметок.
        :type url_id: int

        :returns: Именованный кортеж, содержащий данные URL и список проверок.
        :rtype: UrlDataWithChecksTuple
        """
        with self._db.db_session() as session:
            checks_query = (
                select(
                    self.checks_model,
                )
                .where(self.checks_model.url_id == url_id)
                .order_by(desc(self.checks_model.id))
            )

            result_checks = session.execute(checks_query)
            checks = result_checks.scalars().all()

            url_data_query = select(self.url_model).where(
                self.url_model.id == url_id
            )

            result_url_data = session.execute(url_data_query)
            url_data = result_url_data.scalar_one()

            return UrlDataWithChecksTuple(
                url_data=UrlSchema.model_validate(
                    url_data, from_attributes=True
                ),
                checks_data=[
                    CheckSchema.model_validate(check, from_attributes=True)
                    for check in checks
                ],
            )

    def add_url(self, name: str) -> UrlSchema:
        """
        Добавляет URL в базу данных.

        :param self: Экземпляр менеджера URL-адресов.
        :param name: Имя URL.
        :type name: str
        :returns: Информация о добавленном URL.
        :rtype: UrlSchema
        """
        with self._db.db_session() as session:
            query = (
                insert(self.url_model)
                .values(name=name)
                .returning(self.url_model)
            )
            result = (session.execute(query)).scalar_one()
            session.commit()
            return UrlSchema.model_validate(result, from_attributes=True)

    def get_all_urls(self) -> list[UrlWithLastCheckSchema]:
        """
        Получает список всех URL, включая информацию о последней проверке
        (статус код и дата).


        :return: Список объектов `UrlWithLastCheckSchema`, содержащих URL и
            информацию о последней проверке.
        :rtype: List[UrlWithLastCheckSchema]
        """
        with self._db.db_session() as session:
            query = (
                select(
                    self.url_model.id,
                    self.url_model.name,
                    self.url_model.created_at,
                    self.checks_model.status_code,
                    self.checks_model.created_at.label("last_check"),
                )
                .outerjoin(
                    self.checks_model,
                    self.checks_model.url_id == self.url_model.id,
                )  # noqa
                .distinct(self.url_model.id)
                .order_by(
                    desc(self.url_model.id), desc(self.checks_model.created_at)
                )
            )

            results_urls = session.execute(query)
            session.commit()
            urls = results_urls.all()

            return [
                UrlWithLastCheckSchema.model_validate(url, from_attributes=True)
                for url in urls
            ]

    def add_check_result_for_url(self, url_data: CheckSchema):
        """
        Добавляет результат проверки для указанного URL.

        :param self: Экземпляр менеджера URL-адресов.
        :param url_data: Данные для добавления результата проверки.
            Содержит информацию о URL и его состоянии.
        :type url_data: CheckSchema
        """
        with self._db.db_session() as session:
            query = insert(self.checks_model).values(
                **url_data.model_dump(exclude_none=True)
            )
            session.execute(query)
            session.commit()
