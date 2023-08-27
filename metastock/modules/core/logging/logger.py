import logging

from metastock.modules.core.logging.custom_formatter import CustomFormatter

_log_instances = {}


def Logger(name: str = "root") -> logging.Logger:
    cached = _log_instances.get(name)
    if cached:
        return cached
    else:
        _logger = logging.getLogger(name)
        _logger.setLevel(level = logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(CustomFormatter())
        _logger.addHandler(ch)
        _log_instances[name] = _logger
        return _log_instances[name]
