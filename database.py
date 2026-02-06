from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://todo_user:todo@localhost/todo_db")
# DATABASE_URL = "postgresql://todo_user:todo@db:5432/todo_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
