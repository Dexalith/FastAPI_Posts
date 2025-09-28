from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth.utils import verify_token
from app.configuration_db.db_client import async_db
from app.news.models import Author, Post


security = HTTPBearer()


async def get_current_author(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(async_db.get_session)
) -> Author:
    """
        Зависимость, которая:
        1. Извлекает JWT токен из заголовка Authorization
        2. Проверяет его валидность
        3. Извлекает author_id из payload
        4. Находит автора в БД и возвращает его объект
    """
    token = credentials.credentials

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный или истекший токен'
        )

    author_id = payload.get('sub')
    if author_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is missing subject"'
        )

    result = await session.execute(
        select(Author).where(Author.id == author_id)
    )
    author = result.scalar_one_or_none()

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Автор не найден"
        )

    if not author.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Автор не активен"
        )

    return author


async def get_post_check_owner(
        post_id: int,
        current_author: Author = Depends(get_current_author),
        session: AsyncSession = Depends(async_db.get_session)
) -> Post:
    """
        Зависимость, которая:
        1. Находит пост по ID
        2. Проверяет, что текущий автор - владелец поста
        3. Возвращает пост если все ок, иначе кидает исключение
    """

    result = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )

    if post.author_id != current_author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете только свой пост изменять"
        )
    return post