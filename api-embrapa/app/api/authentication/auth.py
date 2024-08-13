from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users_db import User
from app.core.database import SessionLocal
from app.api.authentication.schemas import Token
from app.api.authentication.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter()
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, db: Session = Depends(get_db)):
    # Verifica se a combinacao de usuario e senha fornecidos no formulario de login sao validos e retorna um JWT caso positivo
    #
    # Arguments:
    #   form_data: É um parâmetro contendo a credencial fornecida no formulario de login
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}