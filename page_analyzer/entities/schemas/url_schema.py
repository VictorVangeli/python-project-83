import datetime

from pydantic import BaseModel, HttpUrl


class BaseID(BaseModel):
    id: int


class BaseName(BaseModel):
    name: HttpUrl


class BaseCreatedAt(BaseModel):
    created_at: datetime.date

class BaseStatusCode(BaseModel):
    status_code: int | None = None

class UrlSchema(BaseID, BaseName, BaseCreatedAt):
    pass

class UrlWithLastCheckSchema(BaseID, BaseName, BaseStatusCode):
    last_check: datetime.date | None = None

class CheckSchema(BaseID, BaseStatusCode, BaseCreatedAt):
    url_id: int | None = None
    h1: str | None = None
    title: str | None = None
    description: str | None = None
