from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract


class SimpleActionV1(ActionAbstract):
    name = 'simple_action_v1'

    def support_signal_output_versions(self) -> list[str]:
        return ['@signal_output/v1']
