from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class StorageEvent(Base):
    __tablename__ = "storage_events"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)