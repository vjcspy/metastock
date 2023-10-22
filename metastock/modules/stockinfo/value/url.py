from metastock.modules.core.util.environment import env

STOCK_PRICE_HISTORY_URL = env().get('PS_API_END_POINT') + "/stock-price/history" if env().get(
        'PS_API_END_POINT'
) is not None else None

SYMBOL_INFO_URL = env().get('PS_API_END_POINT') + "/cor/info" if env().get(
        'PS_API_END_POINT'
) is not None else None
