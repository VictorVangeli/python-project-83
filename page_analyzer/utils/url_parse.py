import httpx
from bs4 import BeautifulSoup

from page_analyzer.entities.schemas.url_schema import ParsedUrlSchema


async def parse_url(url: str) -> ParsedUrlSchema:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        status_code = response.status_code
        parsed_data = BeautifulSoup(response.text, 'html.parser')

        title = parsed_data.title.string.strip() if parsed_data.title else None
        h1_tag = parsed_data.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else None
        description_tag = parsed_data.find('meta', attrs={'name': 'description'})
        description = description_tag.get('content',
                                          '').strip() if description_tag else None

        return ParsedUrlSchema(
            status_code=status_code,
            title=title,
            h1=h1,
            description=description,
        )
