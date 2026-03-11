import aio_pika
from domain.ports import LogPublisher

class RabbitMQPublisher(LogPublisher):
    def __init__(self, url='amqp://guest:guest@localhost/', queue_name='seguridad_logs'):
        self.url = url
        self.queue_name = queue_name

    async def publish_log(self, message: str):
        connection = await aio_pika.connect_robust(self.url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue.name,
            )