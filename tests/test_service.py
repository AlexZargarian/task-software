from unittest.mock import MagicMock
from app.service.processor import MessageProcessor


class TestMessageProcessor:

    def setup_method(self):
        self.mock_repository = MagicMock()
        self.processor = MessageProcessor(repository=self.mock_repository)

    def test_process_valid_message(self):
        # Arrange
        subject = "nut.test"
        message = b'{"key": "value"}'
        self.mock_repository.save_message.return_value.id = 1
        self.mock_repository.save_message.return_value.timestamp.isoformat.return_value = "2023-01-01T00:00:00"

        # Act
        result = self.processor.process_message(subject, message)

        # Assert
        self.mock_repository.save_message.assert_called_once()
        assert result["status"] == "processed"
        assert result["subject"] == "nut.test"
        assert result["content"] == '{"key": "value"}'

    def test_process_empty_message(self):
        # Arrange
        subject = "nut.test"
        message = b'   '

        # Act
        result = self.processor.process_message(subject, message)

        # Assert
        self.mock_repository.save_message.assert_not_called()
        assert result["status"] == "error"
        assert "Empty message" in result["error"]