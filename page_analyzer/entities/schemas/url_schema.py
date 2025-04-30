import datetime
import uuid

from pydantic import BaseModel, HttpUrl


class BaseName(BaseModel):
    name: HttpUrl

class UrlSchema(BaseName):
    id: uuid.UUID
    created_at: datetime.date