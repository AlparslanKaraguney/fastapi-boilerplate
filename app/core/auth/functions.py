from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTBase(BaseModel):
    exp: datetime = None
    scopes: str = None
    sub: str
    id: int
    role: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(
    data: JWTBase, expiration_delta: timedelta = None, refresh: bool = False
) -> str:

    if refresh:
        data.scopes = "refresh_token"
        expiration_delta = timedelta(
            minutes=settings.refresh_token_expire_days
        )
    else:
        data.scopes = "access_token"
        expiration_delta = timedelta(
            minutes=settings.access_token_expire_minutes
        )

    data.exp = datetime.utcnow() + expiration_delta

    return jwt.encode(
        data.dict(), settings.secret_key, algorithm=settings.algorithm
    )


#  TODO: def create_refresh_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_admin(token: str = Depends(oauth2_scheme)) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token invalid")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")


def verify_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("scopes") == "refresh_token":
            return payload
        else:
            # Refresh token invalid
            return None
    except jwt.ExpiredSignatureError:
        # Refresh token expired
        return None
    except jwt.JWTError:
        # Refresh token invalid
        return None
