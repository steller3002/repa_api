from datetime import datetime

from sqlalchemy import String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.models.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    jti: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)