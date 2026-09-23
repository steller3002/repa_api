import uuid
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from auth_service.crud import save_refresh_token
from auth_service.models.refresh_token import RefreshToken
from auth_service.security.jwt import jwt_settings, create_access_token, create_refresh_token, decode_token
from auth_service.security.password import hash_password, verify_password

from auth_service.database import get_db
from auth_service.models.user import User
from auth_service.schemas.requests import RegisterRequest, LoginRequest, RefreshRequest
from auth_service.schemas.responses import TokenResponse

app = FastAPI()

@app.post("/register")
def register(
        request: RegisterRequest,
        db: Session = Depends(get_db)
) -> TokenResponse:
    if request.password != request.password_confirm:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Password not confirmed")

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email already registered")

    password_hash = hash_password(request.password)
    new_user = User(
        email=request.email,
        password_hash=password_hash,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(user_id=new_user.id,
                                       user_data={'email': request.email})

    jti = str(uuid.uuid4())
    refresh_token = create_refresh_token(user_id=new_user.id, jti=jti)

    expires_at = datetime.now(timezone.utc) + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    save_refresh_token(db=db, user_id=new_user.id, jti=jti, expires_at=expires_at)

    db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@app.post("/login")
def login(
        login_request: LoginRequest,
        db: Session = Depends(get_db)
) -> TokenResponse:
    existing_user = db.query(User).filter(User.email == login_request.email).first()

    if not existing_user or not verify_password(login_request.password, existing_user.password_hash):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = create_access_token(user_id=str(existing_user.id),
                                       user_data={'email': existing_user.email})

    jti = str(uuid.uuid4())
    refresh_token = create_refresh_token(user_id=str(existing_user.id), jti=jti)

    expires_at = datetime.now(timezone.utc) + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    save_refresh_token(db=db, user_id=str(existing_user.id), jti=jti, expires_at=expires_at)

    db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@app.post('/refresh')
def refresh(
        refresh_request: RefreshRequest,
        db: Session = Depends(get_db)
) -> TokenResponse:
    decoded_token = decode_token(refresh_request.refresh_token)
    if decoded_token.get('type') != 'refresh':
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect refresh token")

    jti = decoded_token.get('jti')
    user_id = decoded_token.get('user_id')
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authorized")

    stored_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not stored_token or stored_token.revoked:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token revoked or not found")

    stored_token.revoked = True
    new_jti = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_refresh_token = create_refresh_token(user_id=user_id, jti=new_jti)
    save_refresh_token(db=db, user_id=user_id, jti=new_jti, expires_at=expires_at)

    user_data = {'email': user.email}
    new_access_token = create_access_token(user_id=user_id, user_data=user_data)

    db.commit()
    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
