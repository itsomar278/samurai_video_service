import threading
from django.core.management import BaseCommand
from ...utils.rabbitmq_consumer import start_consumer


class Command(BaseCommand):
    help = 'Starts multiple RabbitMQ consumers to listen for video translation requests'

    def add_arguments(self, parser):
        # Allow specifying the number of consumers to start via the command line
        parser.add_argument(
            '--threads',
            type=int,
            default=5,  # Default to 5 threads if not specified
            help='Number of consumer threads to start'
        )

    def handle(self, *args, **kwargs):
        num_threads = kwargs['threads']
        self.stdout.write(f'Starting {num_threads} RabbitMQ consumer threads...')

        for i in range(num_threads):
            thread = threading.Thread(target=start_consumer, daemon=True)
            thread.start()
            self.stdout.write(self.style.SUCCESS(f'Successfully started RabbitMQ consumer thread {i + 1}'))

        self.stdout.write(self.style.SUCCESS('All consumer threads started.'))

        # Keep the main thread alive to prevent the management command from exiting
        try:
            while True:
                # Prevent the script from exiting, while threads run in the background
                threading.Event().wait(1)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Stopping all consumers...'))
