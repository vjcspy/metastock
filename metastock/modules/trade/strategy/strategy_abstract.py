from abc import abstractmethod, ABC
from typing import Self

import arrow

SCHEMA_INPUT_V1 = {
        "type": "object",
        "properties": {
                "api": {
                        "type": "string",
                        "pattern": "^@predefined_input/strategy/v.*$",
                        "description": "API endpoint"
                },
                "name": {
                        "type": "string",
                        "description": "Strategy Input name"
                },
                "input": {
                        "type": "object",
                        "properties": {
                                "range": {
                                        "type": "object",
                                        "properties": {
                                                "type": {
                                                        "type": "string",
                                                        "enum": ["relative", "absolute"]
                                                },
                                                "from": {
                                                        "type": "object",
                                                        "properties": {
                                                                "modify": {
                                                                        "type": "string",
                                                                        "enum": ["shift"]
                                                                },
                                                                "amount": {
                                                                        "type": "number"
                                                                },
                                                                "amount_type": {
                                                                        "type": "string",
                                                                        "enum": ["years"]
                                                                }
                                                        },
                                                        "required": ["modify", "amount", "amount_type"]
                                                },
                                                "to": {
                                                        "type": "object"
                                                }
                                        },
                                        "required": ["type", "from"]
                                },
                                "filter": {
                                        "type": "object"
                                },
                                "signal": {
                                        "type": "object"
                                },
                                "action": {
                                        "type": "object",
                                        "properties": {
                                                "buy": {
                                                        "type": "object"
                                                },
                                                "sell": {
                                                        "type": "object"
                                                }
                                        }
                                }
                        },
                        "required": ["range", "filter", "signal", "action"]
                }
        },
        "required": ["api", "name", "input"]
}


class StrategyAbstract(ABC):
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

    def set_symbol(self, symbol: str) -> Self:
        pass

    @abstractmethod
    def load_input(self, input_config: dict):
        pass
