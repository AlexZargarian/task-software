import json
from datetime import datetime
from app.data.repository import MessageRepository


class MessageProcessor:
    def __init__(self, repository: MessageRepository = None):
        self.repository = repository or MessageRepository()

    def process_message(self, subject: str, message_data: bytes) -> dict:
        """
        Process an incoming message:
          1. Decode and check if the content is not empty.
          2. Determine processing status based on JSON validity:
              - "processed" for valid JSON.
              - "processed_raw" for invalid JSON.
          3. Try saving the message using the repository.
          4. Return a dictionary containing processing details or an error.
        """
        # Step 1: Decode message and check for empty content.
        try:
            content = message_data.decode('utf-8')
            if not content.strip():
                raise ValueError("Empty message content")
        except Exception as e:
            return {
                "subject": subject,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

        # Step 2: Determine status based on JSON validity.
        try:
            json.loads(content)
            status = "processed"
        except json.JSONDecodeError:
            status = "processed_raw"

        # Step 3: Try to save the message. Catch exceptions such as repository errors.
        try:
            saved_message = self.repository.save_message(content, subject)
            return {
                "id": saved_message.id,
                "subject": subject,
                "content": content,
                "timestamp": saved_message.timestamp.isoformat(),
                "status": status
            }
        except Exception as e:
            return {
                "subject": subject,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
