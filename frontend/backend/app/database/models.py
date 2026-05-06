from sqlalchemy import Column, String, Integer
from app.database.connection import Base

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    status = Column(String, default="NEW")


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer)
    current_state = Column(String)
    budget_ceiling = Column(Integer)
    scheduled_time = Column(String)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer)
    sender = Column(String)
    subject = Column(String)
    body = Column(String)
    intent = Column(String)
