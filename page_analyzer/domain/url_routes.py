import uuid

from flask import Blueprint

from page_analyzer.domain.url_service import UrlService
from page_analyzer.entities.forms.url_forms import UrlForm

app_route = Blueprint('app_route', __name__)


@app_route.route('/')
async def index():
    return await UrlService.show_index()


@app_route.post('/add-url')
async def add_data_for_url():
    url = UrlForm().url.data
    return await UrlService().validate_and_add_url(name=url)


@app_route.route('/urls')
async def show_all_urls():
    return await UrlService().show_all_url()


@app_route.get('/urls/<int:url_id>')
async def show_data_for_url(url_id: int):
    return await UrlService().show_data_for_url(url_id=url_id)

@app_route.post('/urls/<int:url_id>/checks')
async def check_particular_url(url_id: int):
    return await UrlService().check_url(url_id=url_id)