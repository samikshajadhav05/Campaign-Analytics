import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./campaigns.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String)
    clicks = Column(Integer)
    cost = Column(Float)
    impressions = Column(Integer)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)