import datetime

from pydantic import BaseModel


class BaseID(BaseModel):
    id: int | None = None


class BaseName(BaseModel):
    name: str


class BaseCreatedAt(BaseModel):
    created_at: datetime.date | None = None


class BaseStatusCode(BaseModel):
    status_code: int | None = None


class UrlSchema(BaseID, BaseName, BaseCreatedAt):
    pass


class UrlWithLastCheckSchema(BaseID, BaseName, BaseStatusCode):
    last_check: datetime.date | None = None


class ParsedUrlSchema(BaseStatusCode):
    h1: str | None = None
    title: str | None = None
    description: str | None = None
    

class CheckSchema(BaseID, ParsedUrlSchema, BaseCreatedAt):
    url_id: int | None = None

