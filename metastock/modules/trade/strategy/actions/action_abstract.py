from abc import ABC, abstractmethod

from jsonschema.validators import validate

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.actions.input_schema import ACTION_INPUT_SCHEMA_V1, ACTION_INPUT_SCHEMA_V1_NAME


class ActionAbstract(ABC):
    name = None

    def load_input(self, input_config: dict):
        api = input_config['api']

        if api == ACTION_INPUT_SCHEMA_V1_NAME:
            return self._load_input_v1(input_config)

        raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, ACTION_INPUT_SCHEMA_V1)
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {ACTION_INPUT_SCHEMA_V1_NAME}")

    def get_name(self):
        return self.name

    @abstractmethod
    def support_signal_output_versions(self) -> list[str]:
        pass
