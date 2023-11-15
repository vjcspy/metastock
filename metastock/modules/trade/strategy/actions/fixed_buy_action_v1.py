from marshmallow import ValidationError

from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.signals.output_schema import (
    FixedBuySchema,
    SIGNAL_OUTPUT_SCHEMA_V1_NAME,
)
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class FixedBuyActionV1(ActionAbstract):
    name = "fixed_buy_action_v1"

    def support_signal_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def run(self, strategy: StrategyAbstract, signals: list[SignalAbstract]):
        for signal in signals:
            version_compatible = self._get_compatible_versions(signal).pop(0)

            signal_output = signal.get_output(version_compatible)

            try:
                FixedBuySchema().load(signal_output)

                Logger().info(
                    f"Detected {len(signal_output['buy'])} days has buy signal"
                )
                Logger().will("Send data to API to save buy action")
                for buy_data in signal_output["buy"]:
                    date = buy_data["date"]
                    price = buy_data["p"]

                    Logger().info(
                        f"Will send data buy with date: {date} at price: {price}"
                    )
            except ValidationError:
                Logger().warning(
                    f"fixed_buy_action_v1 can not process output of signal: {signal.name}"
                )
            except Exception as e:
                Logger().warning(
                    f"fixed_buy_action_v1 could not process output of signal: {signal.name}"
                )
