import pika
from .rabbitmq_channel import RabbitMQChannel
from ..services.process_video_translation_request import process_video_translation_request


def start_consumer():
    print("im here ")
    channel = RabbitMQChannel.create_channel()

    channel.queue_declare(queue='video_translation', passive=True)


    channel.basic_consume(queue='video_translation', on_message_callback=process_video_translation_request)

    try:
        print("Starting consumer...")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped by user.")
        channel.stop_consuming()
    finally:
        RabbitMQChannel.close_channel()
        print("Connection closed.")
