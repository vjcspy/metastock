from typing import Annotated

import typer
from rich.progress import track
import time
from termcolor import colored
from rich.console import Console

from metastock.config.app_config import APP_VERSION
from metastock.config.queue_config import init_queue_config
from metastock.config.trading_config import init_trading_strategy_config
from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import dump_env
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager
from metastock.modules.rabbitmq.consumer_manager import consumer_manager
from metastock.modules.trade.generator.predefined_strategy_generator import PredefinedStrategyGenerator

app = typer.Typer()

logger = Logger()

console = Console()

# _______________ BOOTSTRAP _______________
dump_env()
init_trading_strategy_config()
init_queue_config()


def _introduce():
    Logger().info(f"App version: {APP_VERSION}")


def _test_progress():
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.05)
        total += 1

    logger.info(f'Processed {colored(str(total), "blue")} things.')


@app.callback()
def callback():
    """
    Meta Stock App
    """


@app.command(name='queue:consumer:start')
def queue_consumer_start(name: Annotated[str, typer.Argument(help="Name of consumer.")]):
    """
    Start rabbitmq consumer
    """
    _introduce()
    rabbitmq_manager().initialize()

    consumer = consumer_manager().get_consumer(name)

    if consumer is not None:
        consumer.run()


@app.command(name='strategy:generator:predefine')
def strategy_generator_predefine(input: Annotated[str, typer.Argument(help="Input file.")]):
    """
    Use Predefined strategy for generate process
    """
    _introduce()
    try:
        if "/" not in input:
            input = f"fixture/trade/predefined_inputs/generator/{input}"

        generator = PredefinedStrategyGenerator(
            predefined_input=input
        )

        generator.generate()
    except Exception as e:
        Logger().error("An error occurred: %s", e, exc_info=True)


@app.command()
def main():
    """
        Do nothing!
    """
    rabbitmq_manager().initialize()
