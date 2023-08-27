from metastock.modules.core.logging.logger import Logger


class RabbitMQProducer:
    def __init__(self, queue_manager):
        self.queue_manager = queue_manager

    def publish_message(self, exchange, routing_key, message):
        self.queue_manager.channel.basic_publish(
                exchange = exchange,
                routing_key = routing_key,
                body = message
        )
        Logger().info(f"Message '{message}' published to exchange '{exchange}' with routing_key '{routing_key}'.")
