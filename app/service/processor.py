import json
from datetime import datetime
from app.data.repository import MessageRepository


class MessageProcessor:
    def __init__(self, repository: MessageRepository = None):
        self.repository = repository or MessageRepository()

    def process_message(self, subject: str, message_data: bytes) -> dict:
        """
        Process an incoming message:
        1. Validate the message
        2. Transform if needed
        3. Save to database

        Returns a dict with the processed message info
        """
        # Decode message
        try:
            # Try to parse as JSON if it's in that format
            content = message_data.decode('utf-8')
            # Optional: could do more validation here

            # Check if content is empty
            if not content.strip():
                raise ValueError("Empty message content")

            # Save to database
            saved_message = self.repository.save_message(content, subject)

            return {
                "id": saved_message.id,
                "subject": subject,
                "content": content,
                "timestamp": saved_message.timestamp.isoformat(),
                "status": "processed"
            }
        except json.JSONDecodeError:
            # If not valid JSON, just store as raw text
            content = message_data.decode('utf-8')
            saved_message = self.repository.save_message(content, subject)

            return {
                "id": saved_message.id,
                "subject": subject,
                "content": content,
                "timestamp": saved_message.timestamp.isoformat(),
                "status": "processed_raw"
            }
        except Exception as e:
            # Log error but don't save invalid messages
            return {
                "subject": subject,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }