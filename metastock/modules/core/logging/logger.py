import logging
import os

from rich.logging import RichHandler
from splunk_handler import SplunkHandler

from metastock.modules.core.logging.formatter import CustomJsonFormatter, RichFormatter
from metastock.modules.core.util.environment import env, is_development

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
        _logger.setLevel(level=logging.DEBUG)

        # Old
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        #
        # ch.setFormatter(CustomFormatter())
        # _logger.addHandler(ch)

        rich_handler = get_rich_logger_handler()
        _logger.addHandler(rich_handler)

        # File logger tạm thời cho error
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler('logs/error_logs.log')
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s")
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)

        # Splunk
        if env().get('PS_SPLUNK_ENABLE') == 'true':
            splunk = SplunkHandler(
                    host='54.151.152.110',
                    protocol="http",
                    port=8088,
                    token=env().get('PS_SPLUNK_TOKEN'),
                    index='metastock',
                    # allow_overrides=True # whether to look for _<param in log data (ex: _index)
                    debug=False,  # whether to print module activity to stdout, defaults to False
                    flush_interval=3.0,
                    # send batch of logs every n sec, defaults to 15.0, set '0' to block thread & send immediately
                    # force_keep_ahead=True # sleep instead of dropping logs when queue fills
                    # hostname='hostname', # manually set a hostname parameter, defaults to socket.gethostname()
                    # protocol='http', # set the protocol which will be used to connect to the splunk host
                    # proxies={
                    #           'http': 'http://10.10.1.10:3128',
                    #           'https': 'http://10.10.1.10:1080',
                    #         }, set the proxies for the session request to splunk host
                    #
                    queue_size=0,
                    # a throttle to prevent resource overconsumption, defaults to 5000, set to 0 for no max
                    # record_format=True, whether the log format will be json
                    # retry_backoff=1, the requests lib backoff factor, default options will retry for 1 min, defaults to 2.0
                    # retry_count=2, number of retry attempts on a failed/erroring connection, defaults to 5
                    source='metastock_' + env().get('PS_ENVIRONMENT'),
                    # manually set a source, defaults to the log record.pathname
                    sourcetype='_json',  # manually set a sourcetype, defaults to 'text'
                    verify=False,  # turn SSL verification on or off, defaults to True
                    timeout=5,  # timeout for waiting on a 200 OK from Splunk server, defaults to 60s
            )

            splunk.setFormatter(CustomJsonFormatter('%(level)s %(file)s %(message)s'))
            _logger.addHandler(splunk)

        _log_instances[name] = _logger
        return _log_instances[name]


def get_rich_logger_handler():
    # Tạo một RichHandler để định dạng thông báo log
    handler = RichHandler(
            rich_tracebacks=True if is_development() else False,
            markup=True,
            # console = console.Console(highlight = True)
    )

    handler.setFormatter(RichFormatter())

    return handler
