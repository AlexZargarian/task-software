import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from app.data.models import Base, Message


class MessageRepository:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/nutsdb")
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Initialize the database tables"""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def save_message(self, content: str, subject: str) -> Message:
        """Save a message to the database"""
        message = Message(content=content, subject=subject)
        with self.get_session() as session:
            session.add(message)
            session.commit()
            session.refresh(message)
        return message

    def get_all_messages(self):
        """Retrieve all messages from the database"""
        with self.get_session() as session:
            return session.query(Message).all()

    def get_messages_by_subject(self, subject: str):
        """Retrieve messages with a specific subject"""
        with self.get_session() as session:
            return session.query(Message).filter(Message.subject == subject).all()