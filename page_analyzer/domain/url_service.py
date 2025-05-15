from urllib.parse import urlparse

import httpx
import validators
from flask import flash, redirect, url_for, render_template

from page_analyzer.domain.url_manager import UrlManager
from page_analyzer.entities.enums.message_enums import ErrorsEnum, MessageEnum
from page_analyzer.entities.schemas.url_schema import CheckSchema
from page_analyzer.utils.url_parse import parse_url


class UrlService:
    def __init__(
            self,
    ):
        self.url_manager = UrlManager()

    @staticmethod
    async def show_index():
        """
        Отображает главную страницу сайта.

        :return: Отрендеренный шаблон 'index.html'.  
        :rtype: Response
        """
        return render_template('index.html')

    async def validate_and_add_url(self, name: str):
        """
        Валидирует URL и добавляет его в базу данных.

        :param name: URL для валидации.
        :type name: str
        :returns: Результат валидации или None, если успешно добавлено.
        :rtype: Union[str, None]
        """
        normalized_name = await self.prepare_url(name)
        validation_result = await self._validate_url(name=normalized_name)

        if validation_result is not True:
            flash(message=validation_result, category='danger')
            return redirect(
                url_for('app_route.index'))

        url_id = await self.url_manager.add_url(name=normalized_name)
        flash(message=MessageEnum.CONFIRM_ADD_URL.value, category='success')
        return redirect(
            url_for('app_route.show_data_for_url', url_id=url_id.id))

    async def _validate_url(self, name: str) -> str | bool:
        """
        Валидирует URL.

        Проверяет существование, корректность и длину URL.

        :param name: URL для валидации.
        :type name: str
        :return: Возвращает True, если URL прошел все проверки, или 
            соответствующее значение из ErrorsEnum в противном случае.
        :rtype: bool | str
        """
        if not name:
            return ErrorsEnum.MISSING_URL.value
        if not validators.url(name):
            return ErrorsEnum.INCORRECT_URL.value
        if await self.url_manager.get_url_by_name(name=name):
            return ErrorsEnum.EXISTING_URL.value
        if len(name) > 255:
            return ErrorsEnum.INCORRECT_LENGTH_OF_URL.value
        return True

    @staticmethod
    async def prepare_url(name: str) -> str:
        """  
        Подготовка базового URL из полного URL.  

        :param name: Полный URL для обработки.  
        :type name: str  
        :returns: Базовый URL в виде "scheme://netloc".  
        :rtype: str  
        """
        parsed = urlparse(name)
        normalized_name = f"{parsed.scheme}://{parsed.netloc}"
        return normalized_name

    async def show_data_for_url(self, url_id: int):
        """
        Получает данные для URL по его идентификатору из базы данных и выводит
        всю доступную информацию: информацию о ссылке и о проверках, которые
        проводились, если такие проверки проводились.

        :param url_id: Идентификатор URL, для которого нужно получить данные.
        :type url_id: int
        :returns: Результат обработки данных.
        """
        if await self.url_manager.get_url_by_id(url_id=url_id):
            url_full_data = await self.url_manager.get_all_notes_by_url(
                url_id=url_id)
            response = render_template(
                template_name_or_list='show_data_for_url.html',
                url_data=url_full_data.url_data,
                checks_data=url_full_data.checks_data,
            )
        else:
            response = render_template("404.html")
        return response

    async def show_all_url(self):
        """
        Показывает все добавленные в базу данных URL.

        :returns: HTML-шаблон со списком всех URL.
        :rtype: str
        """
        urls = await self.url_manager.get_all_urls()
        return render_template(
            template_name_or_list='show_all_urls.html',
            urls=urls,
        )

    async def check_url(self, url_id: int):
        """
        Проверяет URL по переданному ID и обновляет информацию о нем, если
        получилось спарсить информацию.

        :param url_id: ID URL для проверки.
        :type url_id: int
        :returns: Перенаправление на страницу с данными о URL.
        :rtype: RedirectResponse
        :raises httpx.RequestError: Если возникает ошибка при запросе к URL.
        """
        url_data = await self.url_manager.get_url_by_id(url_id=url_id)
        try:
            parsed_data = await parse_url(url=url_data.name)
            await self.url_manager.add_check_result_for_url(
                CheckSchema(**parsed_data.model_dump(), url_id=url_id))
        except httpx.RequestError as e:
            flash(ErrorsEnum.ERROR_CHECK.value, 'danger')
        return redirect(
            url_for(endpoint='app_route.show_data_for_url', url_id=url_id)
        )
