import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.datetime.get_current_date import get_current_date_string
from metastock.modules.core.util.http_client import http_client
from metastock.modules.rabbitmq.job_worker import JobWorker
from metastock.modules.rabbitmq.schema import job_consumer_body_schema
from metastock.modules.stockinfo.ulti.get_price_history import get_price_history
from metastock.modules.trade.analysis.hullma import StockTradingAnalysisHullma
from metastock.modules.trade.analysis.total_trade_value import StockTradingAnalysisTotalTradeValue
from metastock.modules.trade.error import JobConsumerPayloadDataError
from metastock.modules.trade.value.url import TradeUrlValue


class StockTradingAnalysisWorker(JobWorker):
    job_id = 'stock_trading_analysis'

    def __init__(self):
        self._symbol = None
        self._price_helper = None


    def handle(self, ch, method, properties, body):
        Logger().info("Process stock trading analysis")
        data = job_consumer_body_schema.loads(body.decode("utf-8"))
        payload = data.get("payload")

        if not isinstance(payload, dict):
            raise JobConsumerPayloadDataError()

        self._symbol = payload.get('symbol')

        if not isinstance(self._symbol, str):
            raise JobConsumerPayloadDataError("payload symbol must be a string")

        price_history = self._get_price_history()
        total_trade_analysis = StockTradingAnalysisTotalTradeValue(
                symbol=self.get_symbol(),
                price_history=price_history
        )
        total_trade_data = total_trade_analysis.get_data()

        hullma_analysis = StockTradingAnalysisHullma(symbol=self.get_symbol(), price_history=price_history)
        hullma_analysis_data = hullma_analysis.get_data()

        # save to downstream
        self._save_data_to_api(
                {
                    "symbol": self.get_symbol(),
                    **total_trade_data,
                    **hullma_analysis_data
                }
        )

    def _save_data_to_api(self, data: dict):
        Logger().info(f"Will save analysis data to downstream for '{self.get_symbol()}'")
        Logger().debug(f"Analysis data of '{self.get_symbol()}' {data}")
        client = http_client()
        res = client.patch(TradeUrlValue.STOCK_TRADING_ANALYSIS_URL, data)

        Logger().debug(f"save analysis data response {res.text}")

        if res.status_code == 200:
            Logger().ok(f"save analysis data to downstream for '{self.get_symbol()}'")
        else:
            Logger().error(f"Could not save analysis data to downstream for '{self.get_symbol()}'")

    def get_symbol(self):
        return self._symbol

    def _get_price_history(self):
        current_date = arrow.utcnow()
        last_12_months = current_date.shift(months=-12).format('YYYY-MM-DD')
        return get_price_history(
                symbol=self.get_symbol(),
                from_date=last_12_months,
                to_date=get_current_date_string(),
                raise_empty_exception=True
        )
