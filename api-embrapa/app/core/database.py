from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

SENHA_BD = os.environ['SENHA_BD']
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+mysqlconnector://root:{SENHA_BD}@localhost:3306/root")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)