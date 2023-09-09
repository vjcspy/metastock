from metastock.modules.rabbitmq.consumer_manager import consumer_manager
from metastock.modules.rabbitmq.job_consumer import JobConsumer
from metastock.modules.test.consumer.test_consumer import TestConsumer
from metastock.modules.test.consumer.test_job_worker1 import TestJobWorker1
from metastock.modules.test.consumer.test_job_worker2 import TestJobWorker2
from metastock.modules.trade.consumer.strategy_consumer import StrategyConsumer

# ________________ Config consumer ________________
consumer_manager().add_consumer(
        [
                TestConsumer(),
                StrategyConsumer(),
                JobConsumer(
                        name = 'test_job_consumer',
                        exchange = 'testbed.exchange',
                        queue = 'testbed.python.job.consumer.queue',
                        routing_key = 'testbed.python.job.consumer.key',
                        workers = [
                                TestJobWorker1(),
                                TestJobWorker2()
                        ]
                )
        ]
)
