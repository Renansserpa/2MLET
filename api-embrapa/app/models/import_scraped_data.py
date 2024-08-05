from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ImportScrapedData(Base):
    __tablename__ = "importacao_scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    paises = Column(String(255), index=True)
    valor = Column(String(255), nullable=True)
    ano = Column(Integer)
    quantity = Column(String(255), nullable=True)
    classificacao_derivado = Column(String(255), nullable=True) 