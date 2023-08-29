from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME


class SimpleActionV1(ActionAbstract):
    name = 'simple_action_v1'

    def support_signal_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]
