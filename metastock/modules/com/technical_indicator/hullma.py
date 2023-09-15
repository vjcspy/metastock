import numpy as np
import pandas as pd

from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.technical_indicator_abstract import TechnicalIndicatorAbstract
from metastock.modules.com.util.price.wma import wma


class HullmaConfig:
    length: int

    def __init__(
            self, length=16,
            cal_source_func=lambda row: row['close']
    ):
        self.length = length
        self.cal_source_func = cal_source_func


class Hullma(TechnicalIndicatorAbstract):
    _cache = {}

    def __init__(self, history: list, symbol: str = None):
        super().__init__(history)

        # default config
        self._symbol = symbol
        self._config = HullmaConfig()
        self._cache = {}

    def get_data(self) -> pd.Series:
        config: HullmaConfig = self.get_config()
        length = config.length
        price_helper = self.get_price_helper()
        _cache_key = self._get_cache_key(length)

        if _cache_key is not None and self._cache.get(_cache_key) is None:
            source = price_helper.create_source_series(value_func=config.cal_source_func)
            hulma = wma(2 * wma(source, int(length / 2)) - wma(source, length), round(np.sqrt(length)))
            self._cache[_cache_key] = hulma

        return self._cache.get(self._get_cache_key(length))

    def _get_cache_key(self, length: int):
        if self._symbol is None:
            return None

        df = self.get_price_helper().get_df()
        first_index = df.index[0].strftime('%Y-%m-%d')
        last_index = df.index[-1].strftime('%Y-%m-%d')

        return self._symbol + '|' + first_index + '|' + last_index + '|' + str(length)
