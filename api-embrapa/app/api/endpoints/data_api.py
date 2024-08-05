from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from typing import Optional, List
from app.models.production_scraped_data import ProductionScrapedData
from app.models.comercialization_scraped_data import ComercializationScrapedData    
from app.models.processing_scraped_data import ProcessingScrapedData
from app.models.import_scraped_data import ImportScrapedData
from app.models.export_scraped_data import ExportScrapedData


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/producao')
def getProducao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método get no endpoint /producao para gerar um JSON com todos os anos dísponiveis
    # da tabela producao_scraped_data
    # Arguments:
    #   ano: É um parâmetro opcional, para caso você deseje consultar os dados de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        producao_data = db.query(ProductionScrapedData).all()
    else:
        producao_data = db.query(ProductionScrapedData).filter(ProductionScrapedData.ano == ano).all()
    if not producao_data:
        return "Sua tabela está vazia, cadastre os dados no banco com o endpoint /scrap/producao", 
    return producao_data
    
@router.get('/processamento')
def getProcessamento(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método get no endpoint /processamento para gerar um JSON com todos os anos dísponiveis
    # da tabela processamento_scraped_data
    # Arguments:
    #   ano: É um parâmetro opcional, para caso você deseje consultar os dados de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    
    if ano is None:
        processamento_data = db.query(ProcessingScrapedData).all()
    else:
        processamento_data = db.query(ProcessingScrapedData).filter(ProcessingScrapedData.ano == ano).all()
    if not processamento_data:
        return "Sua tabela está vazia, cadastre os dados no banco com o endpoint /scrap/producao", 
    return processamento_data

@router.get('/comercializacao')
def getComercializacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método get no endpoint /comercializacao para gerar um JSON com todos os anos dísponiveis
    # da tabela comercializacao_scraped_data
    # Arguments:
    #   ano: É um parâmetro opcional, para caso você deseje consultar os dados de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    
    if ano is None:
        comercializacao_data = db.query(ComercializationScrapedData).all()
    else:
        comercializacao_data = db.query(ComercializationScrapedData).filter(ComercializationScrapedData.ano == ano).all()
    if not comercializacao_data:
        return "Sua tabela está vazia, cadastre os dados no banco com o endpoint /scrap/comercializacao", 
    return comercializacao_data


@router.get('/importacao')
def getImportacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método get no endpoint /importacao para gerar um JSON com todos os anos dísponiveis
    # da tabela importacao_scraped_data
    # Arguments:
    #   ano: É um parâmetro opcional, para caso você deseje consultar os dados de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados

    if ano is None:
        importacao_data = db.query(ImportScrapedData).all()
    else:
        importacao_data = db.query(ImportScrapedData).filter(ImportScrapedData.ano == ano).all()
    if not importacao_data:
        return "Sua tabela está vazia, cadastre os dados no banco com o endpoint /scrap/importacao", 
    return importacao_data

@router.get('/exportacao')
def getExportacao(ano: Optional[int] = Query(None), db: Session = Depends(get_db)):
    # Realiza o método get no endpoint /exportacao para gerar um JSON com todos os anos dísponiveis
    # da tabela exportacao_scraped_data
    # Arguments:
    #   ano: É um parâmetro opcional, para caso você deseje consultar os dados de um ano específico, caso o valor 
    #        seja nulo, será adicionado todos os anos disponíveis 
    #   db: É apenas um parâmetro para que seja possível iniciar a sessão no banco de dados
    
    if ano is None:
        exportacao_data = db.query(ExportScrapedData).all()
    else:
        exportacao_data = db.query(ExportScrapedData).filter(ExportScrapedData.ano == ano).all()
    if not exportacao_data:
        return "Sua tabela está vazia, cadastre os dados no banco com o endpoint /scrap/exportacao", 
    return exportacao_data
