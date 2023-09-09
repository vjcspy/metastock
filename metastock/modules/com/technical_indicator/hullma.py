import numpy as np
import pandas as pd

from metastock.modules.com.technical_indicator.technical_indicator_abstract import TechnicalIndicatorAbstract
from metastock.modules.com.util.price.wma import wma


class HullmaConfig:
    length: int

    def __init__(
            self, length = 16,
            cal_source_func = lambda row: row['close']
    ):
        self.length = length
        self.cal_source_func = cal_source_func


class Hullma(TechnicalIndicatorAbstract):
    _cache = {}

    def __init__(self, history: list):
        super().__init__(history)
        self.set_config(HullmaConfig())

    def get_data(self) -> pd.Series:
        config: HullmaConfig = self.get_config()
        length = config.length

        if self._cache.get(length) is None:
            source = self.get_price_helper().create_source_series(value_func = config.cal_source_func)
            hulma = wma(2 * wma(source, int(length / 2)) - wma(source, length), round(np.sqrt(length)))
            self._cache[length] = hulma

        return self._cache.get(length)
