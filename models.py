from sqlalchemy import Column, Integer, String, Boolean, Boolean, ForeignKey
from database import Base

# Table for tasks
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String, nullable = False)
    status = Column(String, nullable = False)
    done = Column(Boolean, default = False)