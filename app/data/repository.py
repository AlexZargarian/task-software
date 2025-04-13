import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.data.models import Base, Message

class MessageRepository:
    def __init__(self, db_url=None):
        # Use the provided db_url or fall back to the environment variable,
        # with a default PostgreSQL connection.
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/nutsdb")
        self.engine = create_engine(self.db_url)
        # Set expire_on_commit=False so that instances remain accessible after commit.
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False
        )

    def create_tables(self):
        """Initialize the database tables."""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        Provide a transactional scope around a series of operations.
        This ensures that any changes made to the database are properly committed
        or rolled back in case of errors.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save_message(self, content: str, subject: str) -> Message:
        """
        Save a message to the database.

        This method creates a new Message instance, adds it to the session, flushes the session
        to persist the changes (assigning a primary key), and refreshes the instance.
        """
        message = Message(content=content, subject=subject)
        with self.get_session() as session:
            session.add(message)
            session.flush()   # Flush pending changes to assign a primary key.
            session.refresh(message)
        return message

    def get_all_messages(self):
        """Retrieve all messages from the database."""
        with self.get_session() as session:
            return session.query(Message).all()

    def get_messages_by_subject(self, subject: str):
        """Retrieve messages with a specific subject."""
        with self.get_session() as session:
            return session.query(Message).filter(Message.subject == subject).all()
