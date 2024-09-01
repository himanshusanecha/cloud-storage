import pika

# RabbitMQ configuration
rabbitmq_config = {
    'host': 'localhost',  # Adjust to your RabbitMQ server address
    'queue_name': 'file_chunks_queue',  # The queue name from which to consume
}

class ConsumerService:
    def __init__(self):
        # Establish a connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_config['host'],port=5672))
        self.channel = self.connection.channel()

        # Declare the queue to ensure it exists
        self.channel.queue_declare(queue=rabbitmq_config['queue_name'])