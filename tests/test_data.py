import pytest
from unittest.mock import MagicMock
from app.service.processor import MessageProcessor


class TestMessageProcessor:

    def setup_method(self):
        self.mock_repository = MagicMock()
        self.processor = MessageProcessor(repository=self.mock_repository)

    def test_process_valid_message(self):
        subject = "nut.test"
        message = b'{"key": "value"}'
        self.mock_repository.save_message.return_value.id = 1
        self.mock_repository.save_message.return_value.timestamp.isoformat.return_value = "2023-01-01T00:00:00"

        result = self.processor.process_message(subject, message)

        self.mock_repository.save_message.assert_called_once()
        assert result["status"] == "processed"
        assert result["subject"] == subject
        assert result["content"] == '{"key": "value"}'

    def test_process_empty_message(self):
        subject = "nut.test"
        message = b'   '

        result = self.processor.process_message(subject, message)

        self.mock_repository.save_message.assert_not_called()
        assert result["status"] == "error"
        assert "Empty message" in result["error"]

    def test_process_invalid_json(self):
        subject = "nut.test"
        message = b'{not a real json}'
        self.mock_repository.save_message.return_value.id = 2
        self.mock_repository.save_message.return_value.timestamp.isoformat.return_value = "2023-01-01T00:00:00"

        result = self.processor.process_message(subject, message)

        self.mock_repository.save_message.assert_called_once()
        assert result["status"] == "processed_raw"
        assert result["content"] == "{not a real json}"

    def test_process_message_with_whitespace(self):
        subject = "nut.test"
        message = b'    '

        result = self.processor.process_message(subject, message)

        self.mock_repository.save_message.assert_not_called()
        assert result["status"] == "error"
        assert "Empty message" in result["error"]

    def test_process_message_exception(self):
        subject = "nut.test"
        message = b'some text'
        self.mock_repository.save_message.side_effect = Exception("DB down")

        result = self.processor.process_message(subject, message)

        assert result["status"] == "error"
        assert "DB down" in result["error"]
