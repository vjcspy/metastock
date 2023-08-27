import pandas as pd
from abc import ABC, abstractmethod

from metastock.modules.com.technical_indicator.error import DateNotSetError, ConfigNotSetError
from metastock.modules.com.util.price_history_helper import PriceHistoryHelper


class TechnicalIndicatorAbstract(ABC):
    _price_history_helper: PriceHistoryHelper
    _config = None

    def __init__(self, history: list):
        self._date = None
        self._history = history
        self._price_history_helper = PriceHistoryHelper(history)

    @abstractmethod
    def set_config(self, config):
        pass

    @abstractmethod
    def validate_input(self) -> bool:
        pass

    def get_config(self):
        return self._config

    def get_date(self):
        return self._date

    def set_date(self, date: str):
        self._date = date

        return self

    def get_price_history_helper(self):
        return self._price_history_helper

    def get_data(self):
        if self._date is None:
            raise DateNotSetError()

        if self.get_config() is None:
            raise ConfigNotSetError()

    def get_data_for_date(self, date: str):
        self._date = date

        return self.get_data()
