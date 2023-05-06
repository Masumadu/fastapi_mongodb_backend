from datetime import datetime, timedelta

import jwt
import pytz
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError

from app.core.exceptions import AppException
from app.enums import TokenTypeEnum
from config import settings

UTC = pytz.UTC


class JwtAuthentication(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AppException.Unauthorized(
                    error_message="invalid authentication scheme"
                )
            decoded_token = self.decode_token(credentials.credentials)
            if decoded_token.get("token_type") != TokenTypeEnum.access_token.value:
                raise AppException.Unauthorized(error_message="access token required")
            return decoded_token.get("id")

    # noinspection PyMethodMayBeStatic
    def get_token(self, user_id: str):
        token_expiration = datetime.now() + timedelta(minutes=5)
        access_token = self.generate_token(
            user_id=user_id,
            token_type=TokenTypeEnum.access_token.value,
            expiration=str(token_expiration),
        )
        refresh_token = self.generate_token(
            user_id=user_id,
            token_type=TokenTypeEnum.refresh_token.value,
            expiration=str(token_expiration + timedelta(minutes=30)),
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_token(self, refresh_token: str):
        token = self.decode_token(token=refresh_token)
        if token.get("token_type") != TokenTypeEnum.refresh_token.value:
            raise AppException.OperationError(error_message="refresh token required")
        token = self.get_token(token.get("user_id"))

        return token

    # noinspection PyMethodMayBeStatic
    def generate_token(self, user_id: str, token_type: str, expiration: str):
        payload = {"id": user_id, "token_type": token_type, "expires": expiration}
        token = jwt.encode(
            payload=payload, key=settings.secret_key, algorithm=settings.jwt_algorithm
        )
        return token

    # noinspection PyMethodMayBeStatic
    def decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(
                jwt=token, key=settings.secret_key, algorithms=[settings.jwt_algorithm]
            )
        except PyJWTError as exc:
            raise AppException.Unauthorized(error_message=f"{exc}")
        token_expiration = datetime.strptime(
            decoded_token.get("expires"), "%Y-%m-%d %H:%M:%S.%f"
        ).replace(tzinfo=UTC)
        if UTC.localize(datetime.now()) > token_expiration:
            raise AppException.ExpiredTokenException(error_message="token has expired")
        return decoded_token
