from typing import Any

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import env
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.error import TradeFileNotFoundError, StrategyNotFound
from metastock.modules.trade.generator.strategy_generator_abstract import StrategyGeneratorAbstract
import simplejson as json
import os
import jsonschema

from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract
from metastock.modules.trade.util.get_strategy_hash import get_strategy_hash
from metastock.modules.trade.value.url import TradeUrlValue

PRE_DEFINED_INPUT_SCHEMA_V1 = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
                "api": {"type": "string"},
                "strategy": {
                        "type": "object",
                        "properties": {
                                "name": {"type": "string"},
                                "input": {
                                        "type": "object",
                                        "properties": {
                                                "type": {"type": "string"},
                                                "data": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                }
                                        },
                                        "required": ["type", "data"]
                                }
                        },
                        "required": ["name", "input"]
                }
        },
        "required": ["strategy"]
}


class PredefinedStrategyGenerator(StrategyGeneratorAbstract):
    logger = Logger()

    def __init__(self, predefined_input: str):
        super().__init__()
        self.predefined_input = predefined_input
        self._load_input()

    def _load_input(self):
        # Lấy đường dẫn của thư mục project. Giả sử thư mục project của bạn là thư mục cha của thư mục 'src'
        file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", self.predefined_input)
        )
        self.logger.info(f"Load input of generator by path: {file_path}")
        if not os.path.exists(file_path):
            raise TradeFileNotFoundError()

        with open(file_path, 'r') as file:
            data = json.load(file)

        if data is not None:
            api = data['api']
            match api:
                case '@predefined_input/generator/v1':
                    return self._load_input_v1(data)

    def _load_input_v1(self, data: Any):
        # Validate input
        jsonschema.validate(data, PRE_DEFINED_INPUT_SCHEMA_V1)

        # load strategy
        self._load_input_strategy_v1(data['strategy'])

    def _load_input_strategy_v1(self, strategy_config):
        # check if there is a strategy with that name
        self.strategy_name = strategy_config['name']
        if self.strategy_manager.get_strategy_map().get(self.strategy_name) is not None:
            try:
                self.strategy: StrategyAbstract = \
                    self.strategy_manager.get_strategy_map().get(strategy_config['name'])['class']()
            except Exception:
                pass

        if self.strategy is None:
            raise StrategyNotFound()

        # if the configuration was set by files type
        if strategy_config['input']['type'] == 'files':
            self.strategy_inputs_type = 'files'
            self.strategy_inputs = self._load_input_strategy_files_v1(strategy_config)

    def _load_input_strategy_files_v1(self, strategy_config):
        if not isinstance(strategy_config['input']['data'], list):
            return
        _input_configs = []
        for _file in strategy_config['input']['data']:
            file_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", _file)
            )
            if not os.path.exists(file_path):
                raise TradeFileNotFoundError('Not found strategy input configuration')
            with open(file_path, 'r') as file:
                data = json.load(file)
                _input_configs.append({"file": _file, "data": data})

        # Simulate load input for validation, we want all inputs is valid before send it to api server to create job
        for _input_config in _input_configs:
            self.strategy.load_input(input_config = _input_config["data"])

        return _input_configs

    def generate(self):
        self.logger.info(
                f"Process generate with strategy '{self.strategy_name}' and input type {self.strategy_inputs_type} with data {self.strategy_inputs}"
        )
        client = http_client()
        url = TradeUrlValue.TRADING_STRATEGY_PROCESS_URL
        # call api service to generate jobs for strategy and it's inputs
        for config in self.strategy_inputs:
            strategy_input = config['data']['input']
            from_date, to_date = self._get_range_data(strategy_input["range"])
            hash_key = get_strategy_hash(
                    strategy_name = self.strategy_name,
                    strategy_input = strategy_input,
                    from_date = from_date,
                    to_date = to_date
            )
            data = {
                    "strategy_name": self.strategy_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "strategy_input": strategy_input,
                    "hash_key": hash_key
            }

            print(data)

            res = client.post(url, data)

            if res is None:
                return

            if res.status_code == 409:
                self.logger.warning(
                        f"Already generated for strategy '{self.strategy_name}' and input name '{config['data']['name']}'"
                )
            elif res.status_code == 201:
                self.logger.info(
                        f"OK generated for strategy '{self.strategy_name}' and input name '{config['data']['name']}'"
                )
            else:
                self.logger.warning(
                        f"Could not generate in api server with response {res.text}"
                )
