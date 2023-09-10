from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class AlertActionV1(ActionAbstract):
    name = 'alert_action_v1'

    def support_signal_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def run(self, strategy: StrategyAbstract, signals: list[SignalAbstract]):
        for signal in signals:
            version_compatible = self._get_compatible_versions(signal).pop(0)

            signal_output = signal.get_output(version_compatible)

            a = 1
