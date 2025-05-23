import httpx
from bs4 import BeautifulSoup

from page_analyzer.entities.schemas.url_schema import ParsedUrlSchema


async def parse_url(url: str) -> ParsedUrlSchema:
    """
    Выполняет запрос по URL и извлекает:
    - статус-код
    - <title>
    - <h1>
    - <meta name="description">

    Если <h1> отсутствует, пытается извлечь его из iframe.
    """
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        response = await client.get(url)
        html = response.text

        parsed_data = BeautifulSoup(html, 'html.parser')

        # fallback на iframe, если нет h1
        if not parsed_data.find('h1'):
            iframe = parsed_data.find('iframe')
            if iframe and iframe.get('src'):
                iframe_response = await client.get(iframe['src'])
                iframe_data = BeautifulSoup(iframe_response.text, 'html.parser')
                parsed_data.append(iframe_data)

        title = parsed_data.title.string.strip() if parsed_data.title else None
        h1_tag = parsed_data.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else None
        description_tag = parsed_data.find('meta', attrs={'name': 'description'})
        description = description_tag.get('content', '').strip() if description_tag else None

        return ParsedUrlSchema(
            status_code=response.status_code,
            title=title,
            h1=h1,
            description=description,
        )
