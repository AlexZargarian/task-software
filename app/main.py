import asyncio
import signal
import os
from app.api.subscriber import NutsSubscriber
from app.service.processor import MessageProcessor
from app.data.repository import MessageRepository


async def main():
    # Initialize the layers
    repository = MessageRepository()
    processor = MessageProcessor(repository)
    subscriber = NutsSubscriber(processor)

    # Create database tables if they don't exist
    repository.create_tables()

    # Get subjects from environment or use default
    subjects = os.getenv("SUBSCRIBE_SUBJECTS", "nut.>").split(",")

    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(subscriber)))

    # Connect and subscribe
    await subscriber.connect()
    await subscriber.subscribe(subjects)

    print(f"Nuts subscriber is running. Listening to: {subjects}")

    # Keep the application running
    while True:
        await asyncio.sleep(1)


async def shutdown(subscriber):
    print("Shutting down...")
    await subscriber.close()
    print("Shutdown complete")
    asyncio.get_event_loop().stop()


if __name__ == "__main__":
    asyncio.run(main())