from metastock.modules.trade.strategy.actions.action_manager import action_manager
from metastock.modules.trade.strategy.actions.simple_action_v1 import SimpleActionV1

TRADING_STRATEGY_ACTIONS = {
        SimpleActionV1.name: {
                "class": SimpleActionV1
        }
}

for key, value in TRADING_STRATEGY_ACTIONS.items():
    action_manager().define(key, value)
