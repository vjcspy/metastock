from metastock.config.queue_config import init_queue_config
from metastock.config.trading_config import init_trading_strategy_config
from metastock.modules.core.util.environment import dump_env

dump_env()
init_trading_strategy_config()
init_queue_config()
