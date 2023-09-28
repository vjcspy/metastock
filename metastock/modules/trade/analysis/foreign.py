from metastock.modules.stockinfo.ulti.get_price_history import get_price_history


class StockTradingAnalysisForeign:

    def __init__(self, symbol: str, price_history: list = None):
        self._price_history = price_history
        self._symbol = symbol

    def get_data(self):
        price_history = self.get_price_history()

    def get_symbol(self):
        return self._symbol

    def get_price_history(self):
        if self._price_history is None:
            self._price_history = get_price_history(symbol=self.get_symbol())

        return self._price_history
