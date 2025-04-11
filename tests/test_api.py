import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from app.api.subscriber import NutsSubscriber
from app.service.processor import MessageProcessor


class TestNutsSubscriber:

    def setup_method(self):
        self.mock_processor = MagicMock(spec=MessageProcessor)
        self.mock_nats_client = AsyncMock()
        self.subscriber = NutsSubscriber(processor=self.mock_processor, nats_url="nats://localhost:4222")

    @pytest.mark.asyncio
    @patch('app.api.subscriber.nats.connect', new_callable=AsyncMock)
    async def test_connect(self, mock_connect):
        mock_connect.return_value = self.mock_nats_client

        await self.subscriber.connect()

        mock_connect.assert_called_once_with("nats://localhost:4222")
        assert self.subscriber.client == self.mock_nats_client

    @pytest.mark.asyncio
    @patch('app.api.subscriber.nats.connect', new_callable=AsyncMock)
    async def test_subscribe(self, mock_connect):
        mock_connect.return_value = self.mock_nats_client
        self.mock_nats_client.subscribe = AsyncMock()

        await self.subscriber.subscribe(["nut.test", "nut.another"])

        mock_connect.assert_called_once()
        assert self.mock_nats_client.subscribe.call_count == 2

    @pytest.mark.asyncio
    async def test_message_handler(self):
        self.subscriber.client = self.mock_nats_client
        mock_msg = MagicMock()
        mock_msg.subject = "nut.test"
        mock_msg.data = b'{"key": "value"}'
        mock_msg.reply = "reply_subject"

        self.mock_processor.process_message.return_value = {
            "id": 1,
            "subject": "nut.test",
            "content": '{"key": "value"}',
            "timestamp": "2023-01-01T00:00:00",
            "status": "processed"
        }

        await self.subscriber._message_handler(mock_msg)

        self.mock_processor.process_message.assert_called_once_with("nut.test", b'{"key": "value"}')
        self.mock_nats_client.publish.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.api.subscriber.nats.connect', new_callable=AsyncMock)
    async def test_unsubscribe(self, mock_connect):
        mock_subscription1 = AsyncMock()
        mock_subscription2 = AsyncMock()
        self.subscriber.subscriptions = [mock_subscription1, mock_subscription2]

        await self.subscriber.unsubscribe()

        mock_subscription1.unsubscribe.assert_called_once()
        mock_subscription2.unsubscribe.assert_called_once()
        assert self.subscriber.subscriptions == []

    @pytest.mark.asyncio
    @patch('app.api.subscriber.nats.connect', new_callable=AsyncMock)
    async def test_close(self, mock_connect):
        self.subscriber.client = self.mock_nats_client
        self.subscriber.unsubscribe = AsyncMock()

        await self.subscriber.close()

        self.subscriber.unsubscribe.assert_called_once()
        self.mock_nats_client.close.assert_called_once()
