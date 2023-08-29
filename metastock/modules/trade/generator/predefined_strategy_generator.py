from typing import Any

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.find_common_elements import find_common_elements
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.error import (
    ActionAndSignalNotMatch, StrategyActionNotFound,
    StrategyFilterNotFound, StrategySignalNotFound,
    TradeFileNotFoundError,
    StrategyNotFound,
)
from metastock.modules.trade.generator.input_schema import PRE_DEFINED_INPUT_SCHEMA_V1
from metastock.modules.trade.generator.strategy_generator_abstract import StrategyGeneratorAbstract
import simplejson as json
import os
import jsonschema

from metastock.modules.trade.strategy import strategy_manager
from metastock.modules.trade.strategy.actions import action_manager
from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.filters import filter_manager
from metastock.modules.trade.strategy.filters.filter_abstract import FilterAbstract
from metastock.modules.trade.strategy.signals import signal_manager
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract
from metastock.modules.trade.util.get_strategy_hash import get_strategy_hash
from metastock.modules.trade.value.url import TradeUrlValue


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
        if strategy_manager().get_class_map().get(self.strategy_name) is not None:
            try:
                self.strategy: StrategyAbstract = \
                    strategy_manager().get_class_map().get(strategy_config['name'])['class']()
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
        self.logger.debug("Will simulate load strategy and it's signal and action for validate input")
        for _input_config in _input_configs:
            self.strategy.load_input(input_config = _input_config["data"])
            self.logger.debug(f"OK validate input for strategy [blue]{_input_config['data']['name']}[/blue]")

            # Simulate load filter to verify input
            filter_input = _input_config["data"]["input"]["filter"]
            filters = filter_input['filters']
            self.logger.debug("Will simulate load filters")
            for filter_class_name in filters:
                filter_class = filter_manager().get_class(filter_class_name)

                if filter_class is None:
                    raise StrategyFilterNotFound()

                filter_instance: FilterAbstract = filter_class()
                filter_instance.load_input(filter_input['input'])
                self.logger.debug(f"OK validate input for filter [blue]{filter_class_name}[/blue]")

            # Simulate load signal to verify input
            signal_input = _input_config["data"]["input"]["signal"]
            signals = signal_input['signals']
            self.logger.debug("Will simulate load signals")
            signal_instances = []
            for signal_class_name in signals:
                signal_class = signal_manager().get_class(signal_class_name)

                if signal_class is None:
                    raise StrategySignalNotFound()

                signal: SignalAbstract = signal_class()
                signal.load_input(signal_input['input'])
                self.logger.debug(f"OK validate input for signal [blue]{signal_class_name}[/blue]")
                signal_instances.append(signal)

            # Simulate load action to verify input
            action_input = _input_config["data"]["input"]["action"]
            actions = action_input['actions']
            self.logger.debug("Will simulate load actions")
            for action_class_name in actions:
                action_class = action_manager().get_class(action_class_name)

                if action_class is None:
                    raise StrategyActionNotFound()

                action: ActionAbstract = action_class()
                action.load_input(action_input['input'])
                self.logger.debug(f"OK validate input for action [blue]{action_class_name}[/blue]")

                # verify each action can understand output schema
                for signal in signal_instances:
                    signal_outputs = signal.support_output_versions()
                    action_supports = action.support_signal_output_versions()

                    if len(find_common_elements(signal_outputs, action_supports)) == 0:
                        raise ActionAndSignalNotMatch(
                                f"Action '{action.get_name()}' not match with any output of signal '{signal.get_name()}'"
                        )

        return _input_configs

    def generate(self):
        self.logger.debug(
                f"Process generate with strategy '{self.strategy_name}' and input type '{self.strategy_inputs_type}' with data {self.strategy_inputs}"
        )
        client = http_client()
        url = TradeUrlValue.TRADING_STRATEGY_PROCESS_URL
        # call api service to generate jobs for strategy and it's inputs
        for config in self.strategy_inputs:
            self.logger.info(
                    f"Process strategy '{self.strategy_name}' with input name '{config.get('data').get('name')}'"
            )
            strategy_input = config['data']['input']
            from_date, to_date = self._get_range_data(strategy_input["range"])
            hash_key = get_strategy_hash(
                    strategy_name = self.strategy_name,
                    strategy_input = config['data'],
                    from_date = from_date,
                    to_date = to_date
            )
            data = {
                    "strategy_name": self.strategy_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "strategy_input": config['data'],
                    "hash_key": hash_key
            }

            try:
                self.logger.info(f"Will send to API server to process strategy with data {data}")

                res = client.post(url, data)

                if res is None:
                    return

                if res.status_code == 409:
                    self.logger.warning(
                            f"[yellow]DUPLICATED[/yellow] Already generated for strategy '{self.strategy_name}' and input name '{config['data']['name']}'"
                    )
                elif res.status_code == 201:
                    self.logger.info(
                            f"OK generated for strategy '{self.strategy_name}' and input name '{config['data']['name']}'"
                    )
                else:
                    self.logger.warning(
                            f"Could not generate in api server with response {res.text}"
                    )
            except Exception as e:
                self.logger.error("An error occurred when send to downstream: %s", e, exc_info = True)
