from datetime import datetime

from pydantic import BaseModel
from pydantic_collections import BaseCollectionModel

from app.utils.encoders import ObjectIdStr


class ResourceSchema(BaseModel):
    id: ObjectIdStr
    title: str
    content: str
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True


class ResourceSchemaCollection(BaseCollectionModel[ResourceSchema]):
    pass


class CreateResourceSchema(BaseModel):
    title: str
    content: str


class UpdateResourceSchema(BaseModel):
    title: str = None
    content: str = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
