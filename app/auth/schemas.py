from pydantic import  BaseModel, Field, EmailStr
from uuid import UUID

class AuthorCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class AuthorOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class AuthorLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"