from metastock.modules.trade.strategy.signals.signal_manager import signal_manager
from metastock.modules.trade.strategy.signals.technical.simple_sqz_mom_signal import SimpleSqzMomSignal

TRADING_STRATEGY_SIGNALS = {
        SimpleSqzMomSignal.name: {
                "class": SimpleSqzMomSignal
        }
}

for key, value in TRADING_STRATEGY_SIGNALS.items():
    signal_manager().define(key, value)
