import pika

rabbitmq_config = {
    'host': 'localhost',  # Adjust to your RabbitMQ server address
    'queue_name': 'file_chunks_queue',  # The queue name from which to consume
}

class ProducerService:
    def __init__(self):
        # Establish a connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_config['host']))
        self.channel = self.connection.channel()
        
        # Declare the queue
        self.channel.queue_declare(queue=rabbitmq_config['queue_name'])

    def produce_message(self, message):
        # Convert the message to a string (or JSON if needed)
        message_body = str(message)
        
        # Publish the message to the RabbitMQ queue
        self.channel.basic_publish(
            exchange='',
            routing_key=rabbitmq_config['queue_name'],
            body=message_body
        )

    def close(self):
        # Close the connection
        if self.connection:
            self.connection.close()