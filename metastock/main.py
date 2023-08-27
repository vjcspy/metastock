import typer
from rich.progress import track
import time
from termcolor import colored

from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager

app = typer.Typer()

logger = Logger()


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
    Awesome Portal Gun
    """


@app.command()
def load():
    """
    Load the portal gun
    """
    _test_progress()


@app.command()
def main():
    rabbitmq_manager().initialize()
