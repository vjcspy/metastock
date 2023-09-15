from abc import abstractmethod, ABC

from jsonschema.validators import validate

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.find_common_elements import find_common_elements
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.error import (
    ActionAndSignalNotMatch, CouldNotExecuteStrategy,
    NotSupportConfigType,
    StrategyActionNotFound, StrategyFilterNotFound,
    StrategySignalNotFound,
)
from metastock.modules.trade.strategy.actions.action_manager import action_manager
from metastock.modules.trade.strategy.filters.filter_manager import filter_manager
from metastock.modules.trade.strategy.input_schema import STRATEGY_INPUT_SCHEMA_V1, STRATEGY_INPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_manager import signal_manager
from metastock.modules.trade.value.url import TradeUrlValue


class StrategyAbstract(ABC):
    actions: list
    filters: list
    signals: list
    name = None

    def __init__(self):
        self.to_date = None
        self.from_date = None
        self.input_config = None
        self.symbol = None
        self.price_history = None

        self.signals = []
        self.filters = []
        self.actions = []

    def get_name(self):
        return self.name

    @abstractmethod
    def get_input_description(self):
        """
        Mỗi một strategy sẽ mô tả cách mà config của nó có thể được dynamic config như thế nào.

        Mục đích của việc này là để strategy generator có thể dynamic generate input trong tất cả các trường hợp.
        Từ đó chạy strategy này trong một phạm vi nào đó để tìm ra best input config

        Returns:
            TBD
        """
        pass

    def set_symbol(self, symbol: str):
        self.symbol = symbol

        return self

    def get_symbol(self):
        return self.symbol

    def load_input(self, input_config: dict, from_date: str = None, to_date: str = None) -> bool:
        """
        from_date and to_date may be passed because they are resolved before send to API server in case relative date
        """
        self.input_config = input_config
        self.from_date = from_date
        self.to_date = to_date

        api = input_config['api']

        if api == STRATEGY_INPUT_SCHEMA_V1_NAME:
            self._load_input_v1()
        else:
            raise NotSupportConfigType(f"Not support this config input api {api}")

        return True

    def _load_input_v1(self):
        try:
            validate(self.input_config, STRATEGY_INPUT_SCHEMA_V1)

        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {STRATEGY_INPUT_SCHEMA_V1_NAME}")

        _filter_config = self.input_config['input']['filter']
        self._load_filters(_filter_config['filters'], _filter_config['input'])

        _signal_config = self.input_config['input']['signal']
        self._load_signals(_signal_config['signals'], _signal_config['input'])

        _action_config = self.input_config['input']['action']
        self._load_actions(_action_config['actions'], _action_config['input'])

    def _load_filters(self, filters: list[str], filter_input):
        for filter_class_name in filters:
            filter_class = filter_manager().get_class(filter_class_name)

            if filter_class is None:
                raise StrategyFilterNotFound()

            filter_instance = filter_class()
            filter_instance.load_input(filter_input)
            Logger().ok(f"load filter [blue]{filter_class_name}[/blue]")

            filter_instance.set_strategy(self)

            self.filters.append(filter_instance)

    def _load_signals(self, signals: list[str], signal_input):
        for signal_class_name in signals:
            signal_class = signal_manager().get_class(signal_class_name)

            if signal_class is None:
                raise StrategySignalNotFound()

            signal = signal_class()
            signal.load_input(signal_input)
            Logger().ok(f"load signal [blue]{signal_class_name}[/blue]")

            signal.set_strategy(self)

            self.signals.append(signal)

    def _load_actions(self, actions: list[str], action_input):
        for action_class_name in actions:
            action_class = action_manager().get_class(action_class_name)

            if action_class is None:
                raise StrategyActionNotFound()

            action = action_class()
            action.load_input(action_input)
            Logger().ok(f"load action [blue]{action_class_name}[/blue]")

            action.set_strategy(self)

            self.actions.append(action)

            # verify each action can understand output schema
            for signal in self.signals:
                signal_outputs = signal.support_output_versions()
                action_supports = action.support_signal_output_versions()

                if len(find_common_elements(signal_outputs, action_supports)) == 0:
                    raise ActionAndSignalNotMatch(
                        f"Action '{action.get_name()}' not match with any output of signal '{signal.get_name()}'"
                    )

    def execute(self):
        self._load_price_history()

    def _load_price_history(self):
        """
        Load price history base on date from input config
        """

        url = f"{TradeUrlValue.STOCK_PRICE_HISTORY_URL}?code={self.symbol}"
        # url = f"{TradeUrlValue.STOCK_PRICE_HISTORY_URL}?code={'VCB'}"
        url = f"{url}&from={self.from_date}&to={self.to_date}"

        client = http_client()

        try:
            Logger().info(f"Will send to API server to get history price {url}")

            res = client.get(url)
            if res.status_code != 200:
                raise CouldNotExecuteStrategy("Due to error get price history data")

            _json = res.json()
            if not isinstance(_json, list) or len(_json) == 0:
                raise CouldNotExecuteStrategy(f"Due to price history is EMPTY {self.symbol}")

            price_sorted = sorted(_json, key=lambda x: x['date'], reverse=True)
            Logger().ok(f"get price history for {self.symbol}")
            self.price_history = price_sorted

        except Exception as e:
            Logger().error(
                "An error occurred when send to downstream: %s",
                e,
            )

            raise CouldNotExecuteStrategy(f"Due to error get price history data {self.symbol}")

    def get_price_history(self):
        return self.price_history
