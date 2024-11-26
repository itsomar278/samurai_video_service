import pika

class RabbitMQChannel:
    @staticmethod
    def create_channel():
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        channel = connection.channel()
        return connection, channel

    @staticmethod
    def close_channel(connection, channel):
        if channel and not channel.is_closed:
            channel.close()
        if connection and not connection.is_closed:
            connection.close()
