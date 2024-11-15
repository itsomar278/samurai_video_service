import pika
from django.core.management.base import BaseCommand
from ...services.process_video_translation_request import process_video_translation_request

class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer for video translation requests.'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        channel = connection.channel()

        try:
            channel.queue_delete(queue='video_translation')
        except pika.exceptions.ChannelClosedByBroker:
            pass

        channel.queue_declare(queue='video_translation', durable=True)

        # Add an exchange declaration if necessary
        # channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        # channel.queue_bind(exchange='direct_logs', queue='video_translation')

        # Set up the consumer
        channel.basic_consume(queue='video_translation', on_message_callback=process_video_translation_request)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Consumer stopped.")
            channel.stop_consuming()
        finally:
            connection.close()
