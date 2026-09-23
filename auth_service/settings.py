from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"

class DbSettings(BaseSettings):
    DATABASE: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH,
                                      env_prefix='DB_',
                                      extra='ignore')

    @property
    def connection_string(self) -> str:
        return (f'postgresql://{self.USER}:{self.PASSWORD}'
                f'@{self.HOST}:{self.PORT}/{self.DATABASE}')


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH,
                                      env_prefix='JWT_',
                                      extra='ignore')