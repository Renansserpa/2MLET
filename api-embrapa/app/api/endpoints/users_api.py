from pydantic import EmailStr
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
import pandas as pd
from typing import Optional
from http import HTTPStatus
from app.scrapper.scrap import scrap_producao, scrap_processamento, scrap_comercializacao, scrap_importacao, \
    scrap_exportacao
from app.core.database import SessionLocal
from app.models.production_scraped_data import ProductionScrapedData
from app.models.comercialization_scraped_data import ComercializationScrapedData
from app.models.processing_scraped_data import ProcessingScrapedData
from app.models.import_scraped_data import ImportScrapedData
from app.models.export_scraped_data import ExportScrapedData
from app.models.users_db import User
from app.api.authentication.schemas import Message, UserPublic, UserSchema
from app.api.authentication.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter()
CurrentUser = Annotated[User, Depends(get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create', status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Realiza o método POST no endpoint /users/create para criar um usuario
    # no banco de dados
    #
    # Arguments:
    #   user: É um parâmetro contendo as informaces do usuario desejado
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered.',
            )
    hashed_password = get_password_hash(user.password)
    new_db_user = User(
        email=user.email,
        password=hashed_password,
    )
    db.add(new_db_user)
    db.commit()
    db.refresh(new_db_user)

    return new_db_user

@router.get('/query', status_code=HTTPStatus.OK)
def query_user(email: EmailStr, db: Session = Depends(get_db)):
    # Realiza o método GET no endpoint /users/query para obter informacoes de um usuario
    #   no banco de dados
    #
    # Arguments:
    #   email: É um parâmetro contendo o e-mail do usuario desejado
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email is not registered.',
        )
    return db_user

@router.put('/update/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Realiza o método PUT no endpoint /users/update/{user_id} para atualizar um usuario
    #   no banco de dados
    #
    # Arguments:
    #   user_id: É um parâmetro contendo o id de banco de dados do usuario desejado
    #   user: É um parâmetro contendo as novas propriedades desejadas para o usuario em questao
    #   current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )
    old_user = db.query(User).filter(User.email == user.email).first()
    db.delete(old_user)
    db.commit()
    new_user = User(
        email = user.email,
        password = get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    return new_user

@router.delete('/delete/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Realiza o método DELETE no endpoint /users/delete/{user_id} para deletar um usuario
    #   no banco de dados
    #
    # Arguments:
    #   user_id: É um parâmetro contendo o id de banco de dados do usuario desejado
    #   current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    old_user = db.query(User).filter(User.id == user_id).first()
    db.delete(old_user)
    db.commit()

    return {'message': 'User deleted'}

