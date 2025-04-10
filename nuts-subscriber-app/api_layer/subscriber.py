# api_layer/subscriber.py

import time
from service_layer.processor import process_message

def subscribe_to_nuts():
    # Simulated subscription loop for the Nuts service.
    while True:
        # Simulate receiving a message.
        message = "Example message from Nuts service"
        print("Received message:", message)
        process_message(message)
        # Wait for 5 seconds before checking for the next message.
        time.sleep(5)

if __name__ == "__main__":
    subscribe_to_nuts()
