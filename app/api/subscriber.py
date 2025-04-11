import json
import nats
import os
from typing import List

from app.service.processor import MessageProcessor


class NutsSubscriber:
    def __init__(self, processor: MessageProcessor = None, nats_url: str = None):
        self.processor = processor or MessageProcessor()
        self.nats_url = nats_url or os.getenv("NATS_URL", "nats://nats:4222")
        self.client = None
        self.subscriptions = []

    async def connect(self):
        """Connect to the NATS server"""
        self.client = await nats.connect(self.nats_url)
        print(f"Connected to NATS server at {self.nats_url}")

    async def subscribe(self, subjects: List[str]):
        """
        Subscribe to the specified subjects
        """
        if not self.client:
            await self.connect()

        for subject in subjects:
            subscription = await self.client.subscribe(subject, cb=self._message_handler)
            self.subscriptions.append(subscription)
            print(f"Subscribed to {subject}")

    async def _message_handler(self, msg):
        """Handle incoming messages"""
        subject = msg.subject
        data = msg.data
        print(f"Received message on {subject}")

        # Process message using the service layer
        result = self.processor.process_message(subject, data)

        # If the message has a reply subject, respond
        if msg.reply:
            response = json.dumps(result).encode()
            await self.client.publish(msg.reply, response)

    async def unsubscribe(self):
        """Unsubscribe from all subjects"""
        for subscription in self.subscriptions:
            await subscription.unsubscribe()
        self.subscriptions = []

    async def close(self):
        """Close the connection"""
        if self.client:
            await self.unsubscribe()
            await self.client.close()