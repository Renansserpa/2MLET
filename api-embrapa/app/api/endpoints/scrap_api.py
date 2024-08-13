from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from sqlalchemy.orm import Session
from app.scrapper.scrap import scrap_producao, scrap_processamento, scrap_comercializacao, scrap_importacao, scrap_exportacao 
from app.core.database import SessionLocal
from app.models.production_scraped_data import ProductionScrapedData
from app.models.comercialization_scraped_data import ComercializationScrapedData    
from app.models.processing_scraped_data import ProcessingScrapedData
from app.models.import_scraped_data import ImportScrapedData
from app.models.export_scraped_data import ExportScrapedData
from app.api.authentication.security import get_current_user
from app.models.users_db import User
import pandas as pd
from typing import Optional

router = APIRouter()
CurrentUser = Annotated[User, Depends(get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/producao')
def api_scrape_producao(current_user: CurrentUser, ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/producao para iniciar o scrap e pegar os dados
    # da aba produção no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #  current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_producao()
    else:
        data = scrap_producao()
    
    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape production data')
    
    print(data.head())  # Imprimir os primeiros valores para depuração
    
    for _, row in data.iterrows():
        db_data = ProductionScrapedData(
            titulo=row['Produto'],
            ano=row['ano'],
            quantidade=row['Quantidade (L.)'],
            tipo_produto=row['tipo_produto']
        )
        db.add(db_data)
    db.commit()
    
    return {"message": "Production data scraped and stored successfully"}

@router.post('/comercializacao')
def api_scrap_comercializacao(current_user: CurrentUser, ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/comercializacao para iniciar o scrap e pegar os dados
    # da aba comercialização no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #  current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    data = scrap_comercializacao()

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape comercialization data')
    
    print(data.head())
    
    for _, row in data.iterrows():
        db_data = ComercializationScrapedData(
            titulo=row['Produto'],
            ano=row['ano'],
            quantidade=row['Quantidade (L.)']
        )
        db.add(db_data)
    db.commit()
    
    return {'message": "Comercialization data scraped and stored successfully'}

@router.post('/processamento')
def api_scrap_processamento(current_user: CurrentUser, ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/processamento para iniciar o scrap e pegar os dados
    # da aba processamento no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #  current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados


    data =  scrap_processamento()

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape processing data')
    
    print(data.head())


    for _, row in data.iterrows():
        db_data = ProcessingScrapedData(
            cultivo=row['Cultivar'],
            quantidade=row['Quantidade (Kg)'],
            ano=row['ano'],
            classificacao_uva=row['classificacao_uva']
        )
        db.add(db_data)
    db.commit()

    return {'message": "Processing data scraped and stored successfully'}

@router.post('/importacao')
def api_scrap_importacao(current_user: CurrentUser, ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/importacao para iniciar o scrap e pegar os dados
    # da aba importação no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #  current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    data =  scrap_importacao()

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape importacao data')
    
    print(data.head())

    for _, row in data.iterrows():
        db_data = ImportScrapedData(
            paises=row['Países'],
            valor=row['Valor (US$)'],
            ano=row['ano'],
            quantidade=row['Quantidade (Kg)'],
            classificacao_derivado=row['classificacao_derivado']
        )
        db.add(db_data)
    db.commit()
    return {'message": "Importacao data scraped and stored successfully'}


@router.post('/exportacao')
def api_scrap_exportacao(current_user: CurrentUser, ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/exportacao para iniciar o scrap e pegar os dados
    # da aba exportação no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #  current_user: É um parâmetro contendo o usuario atual logado na API (se nao estiver logado nao sera possivel
    #        utilizar o metodo)
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    data =  scrap_exportacao()

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape exportacao data')
    
    print(data.head())

    for _, row in data.iterrows():
        db_data = ExportScrapedData(
            paises=row['Países'],
            valor=row['Valor (US$)'],
            ano=row['ano'],
            quantidade=row['Quantidade (Kg)'],
            classificacao_derivado=row['classificacao_derivado']
        )
        db.add(db_data)
    db.commit()
    return {'message": "Importacao data scraped and stored successfully'}
