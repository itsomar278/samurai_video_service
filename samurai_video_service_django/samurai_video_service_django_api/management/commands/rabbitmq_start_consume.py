import threading
from django.core.management import BaseCommand
from ...utils.rabbitmq_consumer import start_consumer


class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer to listen for video translation requests'

    def handle(self, *args, **kwargs):
        thread = threading.Thread(target=start_consumer)
        thread.start()
        self.stdout.write(self.style.SUCCESS('Successfully started RabbitMQ consumer in a separate thread.'))
