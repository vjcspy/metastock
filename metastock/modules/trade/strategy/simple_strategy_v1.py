from jsonschema.validators import validate

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.input_schema import STRATEGY_INPUT_SCHEMA_V1
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class SimpleStrategyV1(StrategyAbstract):
    name = 'simple_strategy_v1'

    _input_schema_v1_name = '@predefined_input/strategy/v1'

    def load_input(self, input_config: dict, from_date: str = None, to_date: str = None):
        api = input_config['api']

        if api == self._input_schema_v1_name:
            self._load_input_v1(input_config)
        else:
            raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, STRATEGY_INPUT_SCHEMA_V1)
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {self._input_schema_v1_name}")

    def get_input_description(self):
        return {}
