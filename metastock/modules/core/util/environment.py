import os


class Environment:
    instance = None

    def get(self, key: str):
        return os.environ.get(key)


def env() -> Environment:
    if Environment.instance is None:
        Environment.instance = Environment()

    return Environment.instance


def is_development() -> bool:
    return env().get('PS_ENVIRONMENT') == 'development' or env().get('ENVIRONMENT') == 'development'
