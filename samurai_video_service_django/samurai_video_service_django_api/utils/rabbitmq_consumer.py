import threading
from .rabbitmq_channel import RabbitMQChannel
from ..services.process_video_translation_request import process_video_translation_request


def start_consumer():

    connection, channel = RabbitMQChannel.create_channel()
    try:
        channel.queue_declare(queue='video_translation', passive=True)

        channel.basic_consume(queue='video_translation', on_message_callback=process_video_translation_request)
        print("Starting consumer...")
        channel.start_consuming()
    except Exception as e:
        print(f"Consumer encountered an error: {e}")
    finally:
        RabbitMQChannel.close_channel(connection, channel)
        print("Consumer connection closed.")
