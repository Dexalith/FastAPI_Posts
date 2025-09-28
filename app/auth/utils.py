from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.configuration_db.conf import settings


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated=['auto']
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_minutes_life)
    to_encode.update({'exp': expire})

    create_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return create_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None