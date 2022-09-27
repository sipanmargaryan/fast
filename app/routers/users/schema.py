from enum import Enum

from pydantic import BaseModel


class UpdateType(str, Enum):
    vote = 'vote'
    comment = 'comment'
    post = 'post'


class GenerateUserVectorRequest(BaseModel):
    categories: list[str]


class UpdateUserVectorRequest(BaseModel):
    user_id: str
    content_id: str
    update_type: UpdateType


class UserVector(BaseModel):
    vector: list
