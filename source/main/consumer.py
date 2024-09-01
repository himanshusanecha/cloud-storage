from fastapi import FastAPI
from services.file_service import FileService
import threading

file_service = FileService()

app = FastAPI()

def start_consumer():
    try:
        # Start consuming messages from RabbitMQ
        file_service.consume_messages()
    except Exception as e:
        print(f"Error in consumer: {e}")

@app.on_event("startup")
def startup_event():
    # Start the consumer in a separate thread
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    print("Consumer thread started.")
