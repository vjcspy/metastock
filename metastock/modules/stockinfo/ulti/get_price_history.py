import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.ulti.error import CouldNotGetPriceHistory
from metastock.modules.stockinfo.value.url import STOCK_PRICE_HISTORY_URL


def get_price_history(
        symbol: str, from_date: str, to_date: str = arrow.utcnow().format('YYYY-MM-DD'), raise_empty_exception=True
):
    url = f"{STOCK_PRICE_HISTORY_URL}?code={symbol}&from={from_date}&to={to_date}"

    client = http_client()

    Logger().info(f"Will send to API server to get history price {url}")

    res = client.get(url)
    if res.status_code != 200:
        raise CouldNotGetPriceHistory("Due to error get price history data")

    _json = res.json()

    if raise_empty_exception is True and (not isinstance(_json, list) or len(_json)) == 0:
        raise CouldNotGetPriceHistory(f"Due to price history is EMPTY {symbol}")

    Logger().ok(f"get price history for {symbol}")
    return sorted(_json, key=lambda x: x['date'], reverse=True)
