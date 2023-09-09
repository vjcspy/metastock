import pandas as pd
from abc import ABC, abstractmethod

from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.error import DateNotSetError, ConfigNotSetError
from metastock.modules.com.util.price_history_helper import PriceHistoryHelper


class TechnicalIndicatorAbstract(ABC):
    _price_history_helper: PriceHistoryHelper | None
    _price_history_df_helper: PriceHistoryDfHelper | None

    def __init__(self, history: list):
        self._date = None
        self._price_history_df_helper = None
        self._price_history_helper = None
        self._history = history
        self._config = None

    def set_config(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def get_date(self):
        return self._date

    def set_date(self, date: str):
        self._date = date

        return self

    def get_price_history_helper(self) -> PriceHistoryHelper:
        if self._price_history_helper is None:
            self._price_history_helper = PriceHistoryHelper(self._history)

        return self._price_history_helper

    def get_price_helper(self) -> PriceHistoryDfHelper:
        if self._price_history_df_helper is None:
            self._price_history_df_helper = PriceHistoryDfHelper(self._history)

        return self._price_history_df_helper

    def get_data(self):
        if self._date is None:
            raise DateNotSetError()

        if self.get_config() is None:
            raise ConfigNotSetError()

    def get_data_for_date(self, date: str):
        self._date = date

        return self.get_data()
