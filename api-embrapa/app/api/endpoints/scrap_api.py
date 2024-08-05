from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.scraping.scrap import scrap_producao, scrap_processamento, scrap_comercializacao, scrap_importacao, scrap_exportacao 
from app.core.database import SessionLocal
from app.models.production_scraped_data import ProductionScrapedData
from app.models.comercialization_scraped_data import ComercializationScrapedData    
from app.models.processing_scraped_data import ProcessingScrapedData
from app.models.import_scraped_data import ImportScrapedData
from app.models.export_scraped_data import ExportScrapedData
import pandas as pd
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/producao')
def api_scrape_producao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/producao para iniciar o scrap e pegar os dados
    # da aba produção no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_producao(None, None)
    else:
        data = scrap_producao(ano, ano)
    
    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape production data')
    
    print(data.head())  # Imprimir os primeiros valores para depuração
    
    for _, row in data.iterrows():
        db_data = ProductionScrapedData(
            title=row['Produto'],
            year=row['ano'],
            quantity=row['Quantidade (L.)']
        )
        db.add(db_data)
    db.commit()
    
    return {"message": "Production data scraped and stored successfully"}

@router.post('/comercializacao')
def api_scrap_comercializacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/comercializacao para iniciar o scrap e pegar os dados
    # da aba comercialização no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_comercializacao(None, None)
    else:
        data = scrap_comercializacao(ano, ano)

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape comercialization data')
    
    print(data.head())
    
    for _, row in data.iterrows():
        db_data = ComercializationScrapedData(
            title=row['Produto'],
            year=row['ano'],
            quantity=row['Quantidade (L.)']
        )
        db.add(db_data)
    db.commit()
    
    return {'message": "Comercialization data scraped and stored successfully'}

@router.post('/processamento')
def api_scrap_processamento(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/processamento para iniciar o scrap e pegar os dados
    # da aba processamento no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_processamento(None, None)
    else:
        data =  scrap_processamento(ano, ano)

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
def api_scrap_importacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/importacao para iniciar o scrap e pegar os dados
    # da aba importação no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_importacao(None, None)
    else:
        data =  scrap_importacao(ano, ano)

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape importacao data')
    
    print(data.head())

    for _, row in data.iterrows():
        db_data = ImportScrapedData(
            paises=row['Países'],
            valor=row['Valor (US$)'],
            ano=row['ano'],
            quantity=row['Quantidade (Kg)'],
            classificacao_derivado=row['classificacao_derivado']
        )
        db.add(db_data)
    db.commit()
    return {'message": "Importacao data scraped and stored successfully'}


@router.post('/exportacao')
def api_scrap_exportacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método post no endpoint /scrap/exportacao para iniciar o scrap e pegar os dados
    # da aba exportação no site da Embrapa, para salvar esses dados em um banco
    #
    # Arguments:
    #   ano: É um parâmetro opcional para caso você deseje fazer um scrap de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        data = scrap_exportacao(None, None)
    else:
        data =  scrap_exportacao(ano, ano)

    if data.empty:
        raise HTTPException(status_code=400, detail='Failed to scrape exportacao data')
    
    print(data.head())

    for _, row in data.iterrows():
        db_data = ExportScrapedData(
            paises=row['Países'],
            valor=row['Valor (US$)'],
            ano=row['ano'],
            quantity=row['Quantidade (Kg)'],
            classificacao_derivado=row['classificacao_derivado']
        )
        db.add(db_data)
    db.commit()
    return {'message": "Importacao data scraped and stored successfully'}