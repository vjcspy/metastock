import json
from time import sleep

from metastock import Logger
from metastock.modules.rabbitmq.consumer import RabbitMQConsumer
from metastock.modules.trade.error import StrategyNotFound, UnknownMessageFromQueue
from metastock.modules.trade.request.get_strategy_process import get_strategy_process
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract
from metastock.modules.trade.strategy.strategy_manager import strategy_manager


class StrategyConsumer(RabbitMQConsumer):
    name = 'strategy_process'

    def __init__(self):
        super().__init__(
                exchange = 'stock.trading.exchange',
                queue = 'stock.trading.strategy.queue',
                routing_key = 'stock.trading.strategy'
        )
        self.logger = Logger()

    def get_name(self):
        return StrategyConsumer.name

    def handle_message(self, ch, method, properties, body):
        try:
            self.logger.info(f"Received message: {body.decode()}")
            data: dict = json.loads(body.decode("utf-8"))
            if not isinstance(data, dict):
                raise UnknownMessageFromQueue()

            hash_key = data.get('hash')
            symbol = data.get('symbol')

            if hash is None or symbol is None:
                raise UnknownMessageFromQueue()

            self.logger.info("Will send request to API downstream to get strategy process")
            strategy_data: dict = get_strategy_process(hash_key = hash_key, symbol = symbol)
            self.logger.debug(f'Strategy process data from downstream {strategy_data}')
            strategy_class = strategy_manager().get_class(strategy_data.get('name'))

            if strategy_class is None:
                raise StrategyNotFound()

            strategy: StrategyAbstract = strategy_class()
            self.logger.debug(f'Will process strategy [blue]{strategy.get_name()}[/blue]')

            strategy.load_input(
                    input_config = strategy_data.get('input'),
                    from_date = strategy_data.get('from'),
                    to_date = strategy_data.get('to')
            )
            strategy.set_symbol(symbol)
            strategy.execute()

            sleep(1000)
            ch.basic_ack(delivery_tag = method.delivery_tag)
            Logger().info("Message acknowledged.")
        except Exception as e:
            Logger().error("An error occurred: %s", e, exc_info = True)

            sleep(300)
            # Negative Acknowledge the message
            ch.basic_nack(delivery_tag = method.delivery_tag, requeue = True)
            Logger().warning("Message not acknowledged, re-queued.")
