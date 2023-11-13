import arrow

from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.environment import env

STOCK_PRICE_HISTORY_URL = (
    env().get("PS_API_END_POINT") + "/stock-price/history"
    if env().get("PS_API_END_POINT") is not None
    else None
)

SYMBOL_INFO_URL = (
    env().get("PS_API_END_POINT") + "/cor/info"
    if env().get("PS_API_END_POINT") is not None
    else None
)

TICKER_HISTORY = (
    env().get("PS_API_END_POINT") + "/tick/histories"
    if env().get("PS_API_END_POINT") is not None
    else None
)


class StockInfoUrl:
    TICK_BASE_URL = "https://stock.ngocdiep.top"

    def get_ticker_history_url(
        self,
        symbol: str,
        from_date: str,
        to_date: str = arrow.utcnow().format("YYYY-MM-DD"),
    ):
        base_url = StockInfoUrl.TICK_BASE_URL

        return (
            f"{base_url}/tick/histories?symbol={symbol}&from={from_date}&to={to_date}"
        )

    def get_tick_url(self, symbol: str, date=arrow.utcnow().format("YYYY-MM-DD")):
        base_url = StockInfoUrl.TICK_BASE_URL

        return f"{base_url}/tick/history?symbol={symbol}&date={date}"

    def _get_base_url(self):
        if env().get("PS_API_END_POINT") is None:
            raise AppError("Missing PS_API_END_POINT env config")

        return env().get("PS_API_END_POINT")
