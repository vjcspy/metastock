from typing import Any

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class SimpleStrategyV1(StrategyAbstract):
    name = 'simple_strategy_v1'

    def load_input(self, input_config: dict):
        api = input_config['api']

        if api == '@predefined_input/strategy/v1':
            self._load_input_v1(input_config)
        else:
            raise NotSupportConfigType("")

    def _load_input_v1(self, input_config):
        pass

    def get_input_description(self):
        return {}
