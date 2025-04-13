import pytest
from app.data.repository import MessageRepository


# Create a fixture for the repository using SQLite in-memory database.
@pytest.fixture
def repository():
    # Using in-memory SQLite ensures each test starts with a fresh database.
    repo = MessageRepository(db_url="sqlite:///:memory:")
    repo.create_tables()  # Initialize the tables before each test.
    return repo


def test_save_message(repository):
    """
    Test that saving a message correctly assigns an ID,
    stores the correct content and subject, and sets a timestamp.
    """
    content = "Hello, testing data layer!"
    subject = "nut.test"
    message = repository.save_message(content, subject)

    # Verify the message is saved with an ID and proper fields.
    assert message.id is not None, "Message ID should be set after saving"
    assert message.content == content, "Content should match the input"
    assert message.subject == subject, "Subject should match the input"
    assert message.timestamp is not None, "A timestamp should be assigned"


def test_get_all_messages(repository):
    """
    Test that get_all_messages returns all messages saved in the database.
    """
    # Save a couple of messages.
    repository.save_message("Message 1", "nut.topic1")
    repository.save_message("Message 2", "nut.topic2")

    messages = repository.get_all_messages()
    assert isinstance(messages, list), "The result should be a list"
    assert len(messages) == 2, "There should be exactly 2 messages saved"


def test_get_messages_by_subject(repository):
    """
    Test that filtering messages by subject returns only those that match.
    """
    # Save messages with different subjects.
    repository.save_message("Message 1", "nut.topic1")
    repository.save_message("Message 2", "nut.topic1")
    repository.save_message("Message 3", "nut.topic2")

    topic1_messages = repository.get_messages_by_subject("nut.topic1")
    assert isinstance(topic1_messages, list), "Filtered result should be a list"
    assert len(topic1_messages) == 2, "There should be 2 messages with subject 'nut.topic1'"

    # Confirm all retrieved messages have the expected subject.
    for message in topic1_messages:
        assert message.subject == "nut.topic1", "Each message should have subject 'nut.topic1'"
