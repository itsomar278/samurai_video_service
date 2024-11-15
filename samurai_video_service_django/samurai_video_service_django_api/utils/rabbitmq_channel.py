import pika


class RabbitMQChannel:
    _channel = None
    _connection = None

    @staticmethod
    def create_channel():
        if RabbitMQChannel._connection is None or RabbitMQChannel._connection.is_closed:
            RabbitMQChannel._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    credentials=pika.PlainCredentials('guest', 'guest')
                )
            )
        if RabbitMQChannel._channel is None or RabbitMQChannel._channel.is_closed:
            RabbitMQChannel._channel = RabbitMQChannel._connection.channel()
        return RabbitMQChannel._channel

    @staticmethod
    def close_channel():
        if RabbitMQChannel._channel:
            RabbitMQChannel._channel.close()
        if RabbitMQChannel._connection:
            RabbitMQChannel._connection.close()
