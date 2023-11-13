from metastock.modules.stockinfo.ulti.get_tick import get_tick
from metastock.modules.trade.analysis.tick import StockTradingAnalysisTick

tick_data = get_tick(symbol="VSC", date="2023-11-10")

tick_analysis = StockTradingAnalysisTick(tick_data=tick_data)
data = tick_analysis.get_data()

print("a")
