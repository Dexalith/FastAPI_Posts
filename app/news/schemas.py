from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthorOut(BaseModel):
    id: UUID
    username: str

    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    updated_at: datetime


class PostOut(BaseModel):
    title: str
    content: str
    author: AuthorOut
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginationPosts(BaseModel):
    page: int = Field(1, ge=1, description='Номер страницы')
    size: int = Field(20, ge=1, le=100, description='Постов на странице')

    @property
    def offset(self) -> int:
        return (self.page -1) * self.size