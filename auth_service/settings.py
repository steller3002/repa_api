from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseSettings):
    DATABASE: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='DB_')

    @property
    def connection_string(self) -> str:
        return (f'postgresql://{self.USER}:{self.PASSWORD}'
                f'@{self.HOST}:{self.PORT}/{self.DATABASE}')