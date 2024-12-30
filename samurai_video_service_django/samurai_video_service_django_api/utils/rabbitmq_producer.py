import json
import time
from .rabbitmq_channel import RabbitMQChannel


def publish_to_queue(message, queue_name, retries=3, delay=7):

    connection, channel = RabbitMQChannel.create_channel()
    channel.queue_declare(queue=queue_name, durable=False, passive=False)

    for attempt in range(retries):
        try:
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=None,
                mandatory=True
            )
            if channel.is_open:
                print(f"Message sent successfully: {message}")
                return True
            time.sleep(delay)
        except Exception as e:
            print(f"Error publishing message: {e}")
            time.sleep(delay)

    print(f"Failed to send message after {retries} attempts: {message}")
    return False
