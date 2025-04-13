from unittest.mock import MagicMock
from app.service.processor import MessageProcessor

class TestMessageProcessor:
    def setup_method(self):
        self.mock_repository = MagicMock()
        self.processor = MessageProcessor(repository=self.mock_repository)

    def test_process_valid_message(self):
        # Arrange: Create a valid JSON message.
        subject = "nut.test"
        message = b'{"key": "value"}'
        self.mock_repository.save_message.return_value.id = 1
        self.mock_repository.save_message.return_value.timestamp.isoformat.return_value = "2023-01-01T00:00:00"

        # Act
        result = self.processor.process_message(subject, message)

        # Assert
        self.mock_repository.save_message.assert_called_once()
        assert result["status"] == "processed"
        assert result["subject"] == subject
        assert result["content"] == '{"key": "value"}'

    def test_process_empty_message(self):
        # Arrange: Message that is only whitespace.
        subject = "nut.test"
        message = b'   '

        # Act
        result = self.processor.process_message(subject, message)

        # Assert: Ensure the repository is not called and an error is returned.
        self.mock_repository.save_message.assert_not_called()
        assert result["status"] == "error"
        assert "Empty message" in result["error"]

    def test_process_invalid_json(self):
        # Arrange: A message that is not valid JSON.
        # Using a string missing the closing brace ensures invalid JSON.
        subject = "nut.test"
        message = b'{"key": "value"'
        self.mock_repository.save_message.return_value.id = 2
        self.mock_repository.save_message.return_value.timestamp.isoformat.return_value = "2023-01-01T00:00:00"

        # Act: The JSON parsing should fail and fall into the JSONDecodeError branch.
        result = self.processor.process_message(subject, message)

        # Assert
        self.mock_repository.save_message.assert_called_once()
        # Because the message is invalid JSON, we expect "processed_raw".
        assert result["status"] == "processed_raw"
        assert result["content"] == message.decode('utf-8')

    def test_process_message_exception(self):
        # Arrange: Simulate an exception (e.g., a database error) during saving.
        subject = "nut.test"
        message = b'some text'
        self.mock_repository.save_message.side_effect = Exception("DB error")

        # Act
        result = self.processor.process_message(subject, message)

        # Assert: Verify that the error is captured and returned.
        assert result["status"] == "error"
        assert "DB error" in result["error"]
