from urllib.parse import urlparse

import httpx
import validators
from flask import flash, redirect, url_for

from page_analyzer.domain.url_manager import UrlManager
from page_analyzer.domain.url_presentation import UrlPresentation
from page_analyzer.entities.enums.message_enums import ErrorsEnum, MessageEnum
from page_analyzer.entities.schemas.url_schema import CheckSchema
from page_analyzer.utils.url_parse import parse_url


class UrlService:
    def __init__(
        self,
    ):
        self.url_manager = UrlManager()
        self.url_presentation = UrlPresentation()

    @staticmethod
    def show_index():
        """
        Отображает главную страницу сайта.

        :return: Отрендеренный шаблон 'index.html'.
        :rtype: Response
        """
        return UrlPresentation.render_index(template_name="index.html")

    def validate_and_add_url(self, name: str):
        """
        Валидирует URL и добавляет его в базу данных.

        :param name: URL для валидации.
        :type name: str
        :returns: Результат валидации или None, если успешно добавлено.
        :rtype: Union[str, None]
        """
        normalized_name = self.prepare_url(name)
        validation_result, existing_url = self._validate_url(
            name=normalized_name
        )

        if validation_result is not True:
            if existing_url:
                flash(message=validation_result, category="danger")
                return redirect(
                    url_for(
                        "app_route.show_data_for_url", url_id=existing_url.id
                    )
                )
            else:
                flash(message=validation_result, category="danger")
                list_urls = self.url_manager.get_all_urls()
                template_name = "index.html"
                code = 422
                return self.url_presentation.render_add_data_for_url_page(
                    template_name=template_name, list_urls=list_urls, code=code
                )

        url_id = self.url_manager.add_url(name=normalized_name)
        flash(message=MessageEnum.CONFIRM_ADD_URL.value, category="success")
        return redirect(
            url_for("app_route.show_data_for_url", url_id=url_id.id)
        )

    def _validate_url(self, name: str):
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
            return ErrorsEnum.MISSING_URL.value, None
        if not validators.url(name):
            return ErrorsEnum.INCORRECT_URL.value, None
        if existing_url := self.url_manager.get_url_by_name(name=name):
            return MessageEnum.EXISTING_URL.value, existing_url
        if len(name) > 255:
            return ErrorsEnum.INCORRECT_LENGTH_OF_URL.value, None
        return True, None

    @staticmethod
    def prepare_url(name: str) -> str:
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

    def show_data_for_url(self, url_id: int):
        """
        Получает данные для URL по его идентификатору из базы данных и выводит
        всю доступную информацию: информацию о ссылке и о проверках, которые
        проводились, если такие проверки проводились.

        :param url_id: Идентификатор URL, для которого нужно получить данные.
        :type url_id: int
        :returns: Результат обработки данных.
        """
        if self.url_manager.get_url_by_id(url_id=url_id):
            url_full_data = self.url_manager.get_all_records_by_url(
                url_id=url_id
            )
            return self.url_presentation.render_data_for_url(
                template_name="show_data_for_url.html",
                url_data=url_full_data.url_data,
                checks_data=url_full_data.checks_data,
            )
        return self.url_presentation.render_data_for_url(
            template_name="404.html"
        )

    def show_all_url(self):
        """
        Показывает все добавленные в базу данных URL.

        :returns: HTML-шаблон со списком всех URL.
        :rtype: str
        """
        return self.url_presentation.render_data_for_all_url(
            urls=self.url_manager.get_all_urls()
        )

    def check_url(self, url_id: int):
        """
        Проверяет URL по ID и сохраняет результаты парсинга.
        """
        try:
            url_data = self.url_manager.get_url_by_id(url_id=url_id)
            parsed_data = parse_url(url_data.name)
            if (
                parsed_data.status_code
                and parsed_data.status_code > 500
                or parsed_data.status_code == 404
            ):
                flash(ErrorsEnum.ERROR_CHECK.value, "danger")
            else:
                self.url_manager.add_check_result_for_url(
                    CheckSchema(**parsed_data.model_dump(), url_id=url_id)
                )
                flash(
                    message=MessageEnum.SUCCESS_CHECK.value, category="success"
                )
        except httpx.RequestError:
            flash(ErrorsEnum.ERROR_CHECK.value, "danger")
        except Exception:
            flash(ErrorsEnum.ERROR_CHECK.value, "danger")

        return redirect(
            url_for(endpoint="app_route.show_data_for_url", url_id=url_id)
        )
