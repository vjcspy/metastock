from metastock.modules.trade.strategy.simple_strategy_v1 import SimpleStrategyV1
from metastock.modules.trade.strategy.strategy_manager import StrategyManager

STRATEGIES = {
    SimpleStrategyV1.name: {
        "class": SimpleStrategyV1
    }
}

for key, value in STRATEGIES.items():
    StrategyManager.define_strategy(key, value)
