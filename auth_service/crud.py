from datetime import datetime

from sqlalchemy.orm import Session

from auth_service.models.refresh_token import RefreshToken


def save_refresh_token(
        db: Session,
        user_id: str,
        jti: str,
        expires_at: datetime,
) -> None:
    refresh_token = RefreshToken(
        user_id=user_id,
        jti=jti,
        expires_at=expires_at,
    )
    db.add(refresh_token)
    db.flush()