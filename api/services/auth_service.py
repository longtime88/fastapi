from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy.orm import Session

from ..core.config import ALGORITHM, SECRET_KEY
from ..deps import bcrypt_context
from ..models import User
from ..repositories import user_repository


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass

  ##wenn user registriert wird, wird überprüft ob der name schon existert hat
def register_user(db: Session, username: str, password: str) -> User:
    if user_repository.get_by_username(db, username):
        raise UserAlreadyExistsError

    return user_repository.create(
        db,
        username=username,
        hashed_password=bcrypt_context.hash(password),
    )


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = user_repository.get_by_username(db, username)
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        raise InvalidCredentialsError
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    expires = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def login(db: Session, username: str, password: str) -> str:
    user = authenticate_user(db, username, password)
    return create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=30),
    )
