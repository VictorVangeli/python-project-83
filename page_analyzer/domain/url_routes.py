import uuid

from flask import Blueprint

from page_analyzer.domain.url_service import UrlService
from page_analyzer.entities.forms.url_forms import UrlForm

app_route = Blueprint('app_route', __name__)


@app_route.route('/')
async def index():
    """
    Отображает главную страницу приложения.
    """
    return await UrlService.show_index()


@app_route.post('/add-url')
async def add_data_for_url():
    """
    Добавляет данные для URL.
    """
    url = UrlForm().url.data
    return await UrlService().validate_and_add_url(name=url)


@app_route.route('/urls')
async def show_all_urls():
    """
    Отображает список всех добавленных URL-адресов с информацией о последней
    проведенной проверке.
    """
    return await UrlService().show_all_url()


@app_route.get('/urls/<int:url_id>')
async def show_data_for_url(url_id: int):
    """
    Показывает данные для указанного URL по его ID.

    :param url_id: ID URL, для которого нужно показать данные.  
    :type url_id: int  
    """
    return await UrlService().show_data_for_url(url_id=url_id)

@app_route.post('/urls/<int:url_id>/checks')
async def check_particular_url(url_id: int):
    """
    Проверяет состояние конкретной URL по её ID.

    :param url_id: Идентификатор URL, который необходимо проверить.
    :type url_id: int
    """
    return await UrlService().check_url(url_id=url_id)