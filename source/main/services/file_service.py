from services.consumer_service import ConsumerService
from services.publisher_service import ProducerService
import uuid
import base64
from confluent_kafka import KafkaError
import pika
import json

# RabbitMQ configuration
rabbitmq_config = {
    'host': 'localhost',  # Adjust to your RabbitMQ server address
    'queue_name': 'file_chunks_queue',  # The queue name from which to consume
}

class FileService:
    
    def __init__(self):
        self.consumer_service = ConsumerService()
        self.producer_service = ProducerService()
        
    def produce_message(self, id, chunk_num, chunk, filename, path, parent_folder):
        user_id = "himanshu"
        path = "/home/tik/files"
        parent_folder = "files"
        
        encoded_chunk = base64.b64encode(chunk).decode("utf-8")
        
        message = {
            "id": str(id),
            "user_id": user_id,
            "path": path,
            "parent_folder": parent_folder,
            "chunk": encoded_chunk,
            "filename": filename,
            "chunk_num": chunk_num
        }
        
        message = json.dumps(message)
        
        # Sending the message to RabbitMQ
        self.producer_service.produce_message(message=message)
        
    def consume_messages(self):
        # Define the callback function for processing messages
        def callback(ch, method, properties, body):
            body = body.decode("utf-8")
            json_body = json.loads(body)
            encoded_chunk = json_body["chunk"]
            decoded_chunk = base64.b64decode(encoded_chunk.encode("utf-8"))
            file_path = json_body['path'] + '/' + json_body['id'] + '_' + str(json_body["chunk_num"])
            print(file_path)
            with open(file_path, "wb") as file:
                file.write(decoded_chunk)
            
           

        # Set up the consumer
        self.consumer_service.channel.basic_consume(
            queue=rabbitmq_config['queue_name'],
            on_message_callback=callback,
            auto_ack=True
        )

        print("Starting to consume from RabbitMQ queue...")
        try:
            # Start consuming
            self.consumer_service.channel.start_consuming()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("Consumer interrupted. Closing connection...")