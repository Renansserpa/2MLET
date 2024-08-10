from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ProductionScrapedData(Base):
    __tablename__ = "producao_scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    ano = Column(Integer)
    quantity = Column(String(255), nullable=True)