import typer

from metastock.main import queue_consumer_start

typer.run(queue_consumer_start)
