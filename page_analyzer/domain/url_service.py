import uuid
from urllib.parse import urlparse

from flask import flash, redirect, url_for, render_template

from page_analyzer.domain.url_manager import UrlManager
from page_analyzer.entities.enums.message_enums import ErrorsEnum, MessageEnum
from page_analyzer.entities.schemas.url_schema import BaseName


class UrlService:
    def __init__(
            self,
    ):
        self.url_manager = UrlManager()

    @staticmethod
    async def show_index():
        return render_template('index.html')

    async def validate_and_add_url(self, name: str):
        validation_result = await self._validate_url(name=name)

        if validation_result is not True:
            flash(message=validation_result, category='danger')
            return redirect(
                url_for('app_route.index'))

        normalized_name = await self.prepare_url(name)
        url_id = await self.url_manager.add_url(name=normalized_name)
        flash(message=MessageEnum.CONFIRM_ADD_URL.value, category='success')
        return redirect(
            url_for('app_route.show_data_for_url', url_id=url_id.id))

    async def _validate_url(self, name: str) -> str | bool:
        if not name:
            return ErrorsEnum.MISSING_URL.value
        if not BaseName.model_validate({'name': name}):
            return ErrorsEnum.INCORRECT_URL.value
        if await self.url_manager.get_url_by_name(name=name):
            return ErrorsEnum.EXISTING_URL.value
        if len(name) > 255:
            return ErrorsEnum.INCORRECT_LENGTH_OF_URL.value
        return True

    @staticmethod
    async def prepare_url(name: str) -> str:
        parsed = urlparse(name)
        normalized_name = f"{parsed.scheme}://{parsed.netloc}"
        return normalized_name

    async def show_data_for_url(self, url_id: int):
        url_full_data = await self.url_manager.get_all_notes_by_url(url_id=url_id)
        url_data = url_full_data.url_data
        checks_data = url_full_data.checks_data
        return render_template(
            template_name_or_list='show_data_for_url.html',
            url_data=url_data,
            checks_data=checks_data,
        )

    async def show_all_url(self):
        urls = await self.url_manager.get_all_urls()
        return render_template(
            template_name_or_list='show_all_urls.html',
            urls=urls,
        )

    async def check_url(self, url_id: int):
        url_data = await self.url_manager.add_check_result_for_url(url_id=url_id)
        return redirect(
            url_for(endpoint='app_route.show_data_for_url', url_id=url_id)
        )