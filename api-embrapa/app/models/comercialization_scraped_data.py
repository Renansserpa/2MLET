from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ComercializationScrapedData(Base):
    __tablename__ = "comercializacao_scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), index=True)
    ano = Column(Integer)
    quantidade = Column(String(255), nullable=True)