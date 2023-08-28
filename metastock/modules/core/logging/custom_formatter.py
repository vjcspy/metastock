import logging
from rich import console


# class CustomFormatter(logging.Formatter):
#     grey = "\x1b[38;20m"
#     yellow = "\x1b[33;20m"
#     red = "\x1b[31;20m"
#     bold_red = "\x1b[31;1m"
#     reset = "\x1b[0m"
#     # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
#     format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s"
#
#     FORMATS = {
#             logging.DEBUG: grey + format + reset,
#             logging.INFO: grey + format + reset,
#             logging.WARNING: yellow + format + reset,
#             logging.ERROR: red + format + reset,
#             logging.CRITICAL: bold_red + format + reset
#     }
#
#     def format(self, record):
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)

class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.console = console.Console()

    def format(self, record):
        log_message = super().format(record)

        if record.levelno == logging.DEBUG:
            log_message = f"{log_message}"
        elif record.levelno == logging.INFO:
            log_message = f"{log_message}"
        elif record.levelno == logging.WARNING:
            log_message = f"{log_message}"
        elif record.levelno == logging.ERROR:
            log_message = f"{log_message}"
        elif record.levelno == logging.CRITICAL:
            log_message = f"{log_message}"

        return log_message
