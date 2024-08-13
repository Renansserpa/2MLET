from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Especifica o arquivo contendo as informacoes necessarias para geracao do token JWT
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    SECRET_KEY: str
    ALGORITHM: str # Algoritmo utilizado para geracao dos tokens JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int # Tempo de expiracao (em minutos) dos tokens JWT
    DATABASE_URL: str
