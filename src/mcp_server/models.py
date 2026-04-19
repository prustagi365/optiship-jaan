from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./optiship-jaan.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
