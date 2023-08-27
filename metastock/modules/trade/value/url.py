from metastock.modules.core.util.environment import env


class TradeUrlValue:
    TRADING_STRATEGY_PROCESS_URL = env().get('PS_API_END_POINT') + "/strategy/process"
