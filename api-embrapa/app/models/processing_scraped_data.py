from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ProcessingScrapedData(Base):
    __tablename__ = "processamento_scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    cultivo = Column(String(255), index=True, nullable=True)
    quantidade = Column(String(255), nullable=True)
    ano = Column(Integer)
    classificacao_uva = Column(String(255), nullable=True)