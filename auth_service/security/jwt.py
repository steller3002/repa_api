import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from auth_service.settings import JWTSettings

jwt_settings = JWTSettings()

def create_access_token(user_id: str, user_data: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': now + timedelta(jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if user_data: payload.update(user_data)
    return jwt.encode(payload, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)


def create_refresh_token(user_id: str, jti: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'jti': jti,
        'exp': now + timedelta(jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")