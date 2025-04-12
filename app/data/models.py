from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    subject = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message(id={self.id}, subject='{self.subject}', timestamp={self.timestamp})>"