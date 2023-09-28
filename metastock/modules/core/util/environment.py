import os

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


class Environment:
    instance = None

    def get(self, key: str):
        return os.environ.get(key)


def env() -> Environment:
    if Environment.instance is None:
        Environment.instance = Environment()

    return Environment.instance


def is_development() -> bool:
    return env().get('PS_ENVIRONMENT') in ['development', 'local'] or env().get('ENVIRONMENT') == 'development'


current_env = os.environ.get('ENVIRONMENT')
if current_env == 'development':
    load_dotenv('.env.local')
    load_dotenv('.env.development')
elif current_env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.local')
    load_dotenv('.env.development')


def dump_env():
    table = Table(title="Environment")

    table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    for key, value in os.environ.items():
        # Kiểm tra nếu tên biến môi trường bắt đầu bằng PS_
        if key.startswith("PS_"):
            table.add_row(key, value)

    console = Console()
    console.print(table, justify="center")
