from typing import NamedTuple

from page_analyzer.entities.schemas.url_schema import CheckSchema, UrlSchema


class UrlDataWithChecksTuple(NamedTuple):
    url_data: UrlSchema
    checks_data: list[CheckSchema]
