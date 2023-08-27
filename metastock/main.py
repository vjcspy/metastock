from typing import Annotated

import typer
from rich.panel import Panel
from rich.progress import track
import time
from termcolor import colored
from rich.console import Console
from rich.text import Text

from metastock.config.consumer_config import CONSUMERS
from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager

app = typer.Typer()

logger = Logger()

console = Console()


def _introduce():
    pass


def _test_progress():
    total = 0
    for value in track(range(100), description = "Processing..."):
        # Fake processing time
        time.sleep(0.05)
        total += 1

    logger.info(f'Processed {colored(str(total), "blue")} things.')


@app.callback()
def callback():
    """
    Meta Stock App
    """


@app.command(name = 'queue:consumer:start')
def queue_consumer_start(name: Annotated[str, typer.Option(help = "Name of consumer.")]):
    """
    Start rabbitmq consumer
    """
    _introduce()
    rabbitmq_manager().initialize()

    consumer = None

    for consumer_class in CONSUMERS:
        if consumer_class.name == name:
            consumer = consumer_class()

    if consumer is not None:
        consumer.run()


@app.command()
def main():
    """
        Do nothing!
    """
    rabbitmq_manager().initialize()
