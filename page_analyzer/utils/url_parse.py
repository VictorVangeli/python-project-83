import requests
from bs4 import BeautifulSoup

from page_analyzer.entities.schemas.url_schema import ParsedUrlSchema


def parse_url(url: str) -> ParsedUrlSchema:
    response = requests.get(url, timeout=10)
    html = response.text

    parsed_data = BeautifulSoup(html, "html.parser")

    if not parsed_data.find("h1"):
        iframe = parsed_data.find("iframe")
        if iframe and iframe.get("src"):
            try:
                iframe_response = requests.get(iframe["src"], timeout=10)
                iframe_data = BeautifulSoup(
                    iframe_response.text, features="html.parser"
                )
                parsed_data.append(iframe_data)
            except requests.RequestException:
                pass

    title = parsed_data.title.string.strip() if parsed_data.title else None
    h1_tag = parsed_data.find("h1")
    h1 = h1_tag.text.strip() if h1_tag else None
    description_tag = parsed_data.find(
        name="meta", attrs={"name": "description"}
    )
    description = (
        description_tag.get(key="content", default="").strip()
        if description_tag
        else None
    )

    return ParsedUrlSchema(
        status_code=response.status_code,
        title=title,
        h1=h1,
        description=description,
    )
