import arrow
from rich.table import Table

from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.assessor.abstract_accessor import AbstractAccessor


class SimpleBuyAccessorDefaultConfig:
    def __init__(self):
        self.min_t = 2
        self.max_t = 4


class SimpleBuyAssessor(AbstractAccessor):
    name = "simple_buy_accessor_v1"

    def __init__(self):
        super().__init__()
        self.config = None
        self.result = {}

    def before_run(self):
        input_config = self.get_input_config()["input"]

        self.config = SimpleBuyAccessorDefaultConfig()

        if "t" in input_config:
            min_t = input_config["t"].get("min")
            max_t = input_config["t"].get("max")

            if isinstance(min_t, int) and min_t > 2:
                self.config.min_t = min_t
            if isinstance(max_t, int):
                self.config.max_t = max_t

        Logger().info(f"Use config {self.config} for access")

    def access(self, strategy_process, process_actions, history_price):
        symbol = strategy_process["symbol"]
        Logger().will(f"access for symbol {symbol} by SimpleBuyAssessor")

        if symbol in self.result:
            Logger().warning(f"Duplicate access for symbol {symbol}")
        else:
            self.result[symbol] = {"pass": [], "fail": [], "percent": 0}

        for action in process_actions:
            date = action["date"]
            a_date = arrow.get(date)
            min_date = a_date.shift(days=self.config.min_t)
            max_date = a_date.shift(days=self.config.max_t)

            def is_valid_min_max_day(price_day):
                a_price_day = arrow.get(price_day["date"])

                return min_date <= a_price_day <= max_date

            look_up_days = [
                price_day
                for price_day in history_price
                if is_valid_min_max_day(price_day)
            ]

            result = next(
                (
                    obj
                    for obj in look_up_days
                    if max(obj["rHigh"], obj["rClose"]) >= action["meta"]["price"]
                ),
                None,
            )

            if result is not None:
                self.result[symbol]["pass"].append(action)
            else:
                self.result[symbol]["fail"].append(action)

        self.result[symbol]["percent"] = round(
            len(self.result[symbol]["pass"])
            / (len(self.result[symbol]["pass"]) + len(self.result[symbol]["fail"])),
            2,
        )

    def run(self):
        super().run()
        self._summary()

    def _summary(self):
        table = Table(title="Summary")
        table.add_column("Key", justify="left", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        # Sắp xếp lại dictionary theo giá trị percent
        sorted_result = dict(
            sorted(self.result.items(), key=lambda x: x[1]["percent"], reverse=True)
        )

        # Duyệt qua từng phần tử trong dictionary đã sắp xếp
        for symbol, data in sorted_result.items():
            table.add_row(
                f"{symbol}",
                f"percent: {data['percent']}, pass: {len(data['pass'])}, fail: {len(data['fail'])}",
            )

        total_percent = 0
        num_symbols = len(self.result)

        for symbol_data in self.result.values():
            total_percent += symbol_data["percent"]

        # Tính trung bình
        average_percent = round(total_percent / num_symbols, 2)
        table.add_row(
            "AVG percent",
            f"{average_percent}",
        )
        Logger().console().print(table, justify="center")
