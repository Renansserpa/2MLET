from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from app.models.users_db import User
from app.core.database import SessionLocal
from app.api.authentication.schemas import TokenData
from app.api.authentication.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    # Cria um JWT com base nas informacoes contidas no arquivo .env (importadas atraves da constante settings)
    #   Algoritmo: HS256
    #   Tempo de duracao: 30 minutos
    #
    # Arguments:
    #   data: É um parâmetro contendo informacoes desejadas para serem incluidas no JWT (no caso, o email do usuario)
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    # Cria um hash a partir do algoritmo argon2 para a senha desejada
    #
    # Arguments:
    #   password: É um parâmetro contendo a senha
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    # Verifica se o hash da senha em texto puro eh o mesmo que o hash sendo fornecido
    #
    # Arguments:
    #   plain_password: É um parâmetro contendo a senha desejada
    #   hashed_password: É um parâmetro contendo o hash desejado (a ser comparado com o hash a ser calculado
    #                       baseado na senha fornecida no parâmetro anterior)
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Verifica se o usuario existe no Banco de dados e se o JWT do mesmo ainda eh valido
    #
    # Arguments:
    #   token: É um parâmetro contendo as informacoes do token JWT do usuario
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    db_user = db.query(User).filter(User.email == token_data.email).first()
    if not db_user:
        raise credentials_exception

    return db_user