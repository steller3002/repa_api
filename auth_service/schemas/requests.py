from pydantic import BaseModel, EmailStr, Field

MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64
MAX_EMAIL_LENGTH = 128

class RegisterRequest(BaseModel):
    email: EmailStr = Field(max_length=MAX_EMAIL_LENGTH)
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
    password_confirm: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)

class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=MAX_EMAIL_LENGTH)
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)

class RefreshRequest(BaseModel):
    refresh_token: str