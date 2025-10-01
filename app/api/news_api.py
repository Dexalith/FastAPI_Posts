from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Query

from app.auth.depencies import get_current_author, get_post_check_owner
from app.news.schemas import PostOut, PostCreate, PostUpdate, PaginationPosts
from app.news.models import Author, Post
from app.configuration_db.db_client import async_db


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("", response_model=List[PostOut])
async def get_list_posts(
        pagination: PaginationPosts = Depends(),
        published_only: bool = Query(False),
        session: AsyncSession = Depends(async_db.get_session)
):
    query = select(Post)

    if published_only:
        pub_query = query.where(Post.is_published == True)

    result = await session.execute(
        pub_query
        .offset(pagination.offset)
        .limit(pagination.size)
        .order_by(Post.created_at.desc())
    )
    posts = result.scalars().all()
    return posts


@router.get("/published", response_model=List[PostOut])
async def get_published_posts(
        session: AsyncSession = Depends(async_db.get_session)
):
    query = select(Post).where(Post.is_published == True)
    result = await session.execute(query)
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostOut)
async def get_post_id(
        post_id: int,
        session: AsyncSession = Depends(async_db.get_session)
):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()  # Получаем один объект или None

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена"
        )
    return post


@router.post("", response_model=PostOut)
async def create_post(
        post_data: PostCreate,
        current_author: Author = Depends(get_current_author),
        session: AsyncSession = Depends(async_db.get_session)
):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_author.id
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(
        post_data: PostUpdate,
        post: Post = Depends(get_post_check_owner),
        session: AsyncSession = Depends(async_db.get_session)
):
    if post is None:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value) # Динамически обновляем данные

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(get_post_check_owner),
    session: AsyncSession = Depends(async_db.get_session)
):

    if post is None:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    # 2. Удаляем его
    await session.delete(post)
    await session.commit()
    # Тело ответа не возвращается, статус 204 говорит сам за себя.