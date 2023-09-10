from metastock.bin.test.get_history_data import get_history_data
from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.hullma import Hullma
from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.util.predict_trend_change import predict_trend_change

history_data = get_history_data(symbol = 'VCB')

priceHelper = PriceHistoryDfHelper(history_data)

hullma = Hullma(history = history_data)
hulma_data = hullma.get_data()
Logger().info(hulma_data.head(20))

predic = predict_trend_change(hulma_data.head(80), 5)

Logger().info(predic)
