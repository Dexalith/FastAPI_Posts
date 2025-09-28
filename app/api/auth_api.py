from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth.utils import hash_password, verify_password, create_token
from app.news.models import Author
from app.auth.schemas import AuthorOut, AuthorCreate, Token, AuthorLogin
from app.configuration_db.db_client import async_db


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
async def register_author(
        author_data: AuthorCreate,
        session: AsyncSession = Depends(async_db.get_session)
):
    existing_author = await session.execute(
        select(Author).where(
            (Author.email == author_data.email) | (Author.username == author_data.username)
        )
    )
    if existing_author.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор с таким никнеймом и почтой уже существует"
        )
    hashed_password = hash_password(author_data.password)

    db_author = Author(
        username=author_data.username,
        email=author_data.email,
        hashed_password=hashed_password
    )

    session.add(db_author)
    await session.commit()
    await session.refresh(db_author)

    return db_author


@router.post("/login", response_model=Token)
async def login_author(
        author_data: AuthorLogin,
        session: AsyncSession = Depends(async_db.get_session)
):
    result = await session.execute(
        select(Author).where(Author.email == author_data.email)
    )
    author = result.scalar_one_or_none()

    if not author or not verify_password(
        author_data.password,
        author.hashed_password # type: ignore
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль или почта'
        )

    if not author.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Автор не активен'
        )

    access_token = create_token(
        data={'sub': str(author.id)}
    )
    return Token(access_token=access_token)