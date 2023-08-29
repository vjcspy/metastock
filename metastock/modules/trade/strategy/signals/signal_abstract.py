from abc import abstractmethod, ABC

from jsonschema.validators import validate

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.signals.input_schema import SIGNAL_INPUT_SCHEMA_V1, SIGNAL_INPUT_SCHEMA_V1_NAME


class SignalOutputV1:
    pass


class SignalOutputV2:
    pass


class SignalAbstract(ABC):
    name = None

    def load_input(self, input_config: dict):
        api = input_config['api']

        if api == SIGNAL_INPUT_SCHEMA_V1_NAME:
            self._load_input_v1(input_config)
        else:
            raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, SIGNAL_INPUT_SCHEMA_V1)
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {SIGNAL_INPUT_SCHEMA_V1_NAME}")

    def __init__(self):
        pass

    def get_name(self):
        return self.name

    @abstractmethod
    def support_output_versions(self) -> list[str]:
        pass

    @abstractmethod
    def get_output(self, version = 'v1') -> SignalOutputV1 | SignalOutputV2:
        pass
