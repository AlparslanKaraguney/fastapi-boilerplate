from datetime import datetime, timedelta

from sqlmodel import Field

from app.core.auth.functions import (
    JWTBase,
    create_jwt_token,
    verify_password,
)
from app.core.models.base import ModelCore
from app.settings import settings

from .schemas import Tokens


class RevokedToken(ModelCore, table=True):
    expiration_date: datetime
    token: str = Field(unique=True)
    username: str

    @staticmethod
    def is_revoked(refresh_token: str) -> bool:
        """
        Check if the refresh token was previously revoked (blacklisted)
        """
        # TODO: Create a relationship between User and RevokedToken
        if RevokedToken.get_one(key=RevokedToken.token, value=refresh_token):
            return True
        return False


class User(ModelCore, table=True):
    username: str
    hashed_password: str
    is_verified: bool = False

    @staticmethod
    def authenticate_user(username: str, password: str) -> Tokens | None:
        # Validate the username exist
        if not (user := User.get_one(key=User.username, value=username)):
            return None

        # Verify password
        # TODO: Add register verification (by email for example)
        if not verify_password(password, user.hashed_password):
            return None

        # Create the pair of tokens
        jwt_base = JWTBase(
            id=user.id,
            sub=username,
            role="",
        )
        access_token = create_jwt_token(jwt_base)
        refresh_token = create_jwt_token(jwt_base, refresh=True)

        tokens = Tokens(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
        )

        return tokens
