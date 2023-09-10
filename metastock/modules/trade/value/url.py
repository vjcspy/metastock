from metastock.modules.core.util.environment import env


class TradeUrlValue:
    TRADING_STRATEGY_PROCESS_URL = env().get('PS_API_END_POINT') + "/strategy/process" if env().get(
            'PS_API_END_POINT'
    ) is not None else None

    STOCK_PRICE_HISTORY_URL = env().get('PS_API_END_POINT') + "/stock-price/history" if env().get(
            'PS_API_END_POINT'
    ) is not None else None
