import logging

from rich.logging import RichHandler

from metastock.modules.core.logging.formatter import RichFormatter
from metastock.modules.core.util.environment import is_development

_log_instances = {}


class AppLogger(logging.Logger):
    def ok(self, msg, *args, **kwargs):
        self.info(f"[green]OK[/green] {msg}", *args, **kwargs)


def Logger(name: str = "root") -> AppLogger:
    cached = _log_instances.get(name)
    if cached:
        return cached
    else:
        _logger = AppLogger(name)
        _logger.setLevel(level = logging.DEBUG)

        # Old
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        #
        # ch.setFormatter(CustomFormatter())
        # _logger.addHandler(ch)

        # Tạo một RichHandler để định dạng thông báo log
        handler = RichHandler(
                rich_tracebacks = True if is_development() else False,
                markup = True,
                # console = console.Console(highlight = True)
        )
        handler.setFormatter(RichFormatter())
        _logger.addHandler(handler)

        _log_instances[name] = _logger
        return _log_instances[name]
