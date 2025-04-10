# service_layer/processor.py

from data_layer.db import save_message
from datetime import datetime

def process_message(message: str):
    if not message:
        print("Error: Received an empty message!")
        return

    # Process message: add a timestamp.
    processed_message = {
        "content": message,
        "timestamp": datetime.utcnow()
    }

    print("Processed message:", processed_message)
    save_message(processed_message)
