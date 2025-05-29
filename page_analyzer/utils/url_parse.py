import requests
from bs4 import BeautifulSoup

from page_analyzer.entities.schemas.url_schema import ParsedUrlSchema


def fetch_html(url: str) -> tuple[str, int]:
    response = requests.get(url, timeout=10)
    return response.text, response.status_code


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def try_append_iframe(parsed_data: BeautifulSoup) -> None:
    if parsed_data.find("h1"):
        return

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


def extract_title(parsed_data: BeautifulSoup) -> str | None:
    return parsed_data.title.string.strip() if parsed_data.title else None


def extract_h1(parsed_data: BeautifulSoup) -> str | None:
    h1_tag = parsed_data.find("h1")
    return h1_tag.text.strip() if h1_tag else None


def extract_description(parsed_data: BeautifulSoup) -> str | None:
    description_tag = parsed_data.find(
        name="meta", attrs={"name": "description"}
    )
    return (
        description_tag.get("content", "").strip() if description_tag else None
    )


def parse_url(url: str) -> ParsedUrlSchema:
    html, status_code = fetch_html(url)
    parsed_data = parse_html(html)
    try_append_iframe(parsed_data)
    title = extract_title(parsed_data)
    h1 = extract_h1(parsed_data)
    description = extract_description(parsed_data)

    return ParsedUrlSchema(
        status_code=status_code,
        title=title,
        h1=h1,
        description=description,
    )
