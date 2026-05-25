from sqlalchemy import create_engine
from typing import Annotated
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the environment")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping = True)

Sessionlocal = sessionmaker(autoflush = False, autocommit = False, bind = engine) 

def get_db():
    db = Sessionlocal()
    try: 
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session,  Depends(get_db)]