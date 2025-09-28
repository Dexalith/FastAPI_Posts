from sqlalchemy import Boolean, BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Самое главное: определяем связь (relationship)
    # Это не колонка в БД, а высокоуровневое представление связи для ORM
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    # Это позволит потом делать так: user.posts чтобы получить все посты пользователя


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    author: Mapped["Author"] = relationship("Author", back_populates="posts")
