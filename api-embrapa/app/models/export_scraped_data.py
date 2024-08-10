from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ExportScrapedData(Base):
    __tablename__ = "exportacao_scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    paises = Column(String(255), index=True)
    valor = Column(String(255), nullable=True)
    ano = Column(Integer)
    quantity = Column(String(255), nullable=True)
    classificacao_derivado = Column(String(255), nullable=True)