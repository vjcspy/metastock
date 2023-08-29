from abc import abstractmethod, ABC
from typing import Self


class StrategyAbstract(ABC):
    name = None

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

    def set_symbol(self, symbol: str) -> Self:
        pass

    @abstractmethod
    def load_input(self, input_config: dict, from_date: str = None, to_date: str = None):
        """
        from_date and to_date may be passed because they are resolved before send to API server in case relative date
        """
        pass

    @abstractmethod
    def execute(self):
        pass
