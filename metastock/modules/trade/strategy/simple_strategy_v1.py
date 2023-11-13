from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class SimpleStrategyV1(StrategyAbstract):
    name = "simple_strategy_v1"

    def load_input(
        self, input_config: dict, from_date: str = None, to_date: str = None
    ):
        super().load_input(input_config, from_date, to_date)

    def get_input_description(self):
        return {}

    def execute(self):
        super().execute()

        # Process filter in runtime, global filter already run in generator

        # Process action
        for action in self.actions:
            action.run(self, self.signals)
