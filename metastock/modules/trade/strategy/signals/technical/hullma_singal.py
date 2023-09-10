from metastock.modules.com.technical_indicator.hullma import Hullma, HullmaConfig
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.util.predict_trend_change import predict_trend_change


class HullmaSignal(SignalAbstract):
    name = 'hullma_signal'

    def support_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def get_output(self, version = SIGNAL_OUTPUT_SCHEMA_V1_NAME):
        if version == SIGNAL_OUTPUT_SCHEMA_V1_NAME:
            return self._get_output_v1()

    def _get_output_v1(self):
        price_history = self.get_strategy().price_history
        input_data = self.get_input()

        hullma_input: dict = input_data.get('hullma')
        hullma_config = HullmaConfig()
        if hullma_input is not None:
            hullma_length = hullma_input.get('length')

            if hullma_length is not None:
                hullma_config.length = hullma_length

        hullma = Hullma(price_history)
        hullma.set_config(hullma_config)
        hullma_data = hullma.get_data()

        # just only for alerting
        predict_trend = predict_trend_change(hullma_data, 5)

        result = []

        for price in price_history:
            date = price['date']

            day_signal = {
                    "buy": {},
                    "sell": {},
                    "alert": {
                            "notify": False
                    }
            }

            predict_trend_day = predict_trend.loc[date]

            if predict_trend_day is not None:
                if 0 < predict_trend_day["estimate_day_change"] < 3:
                    day_signal["alert"] = {
                            "notify": True,
                            "message": f"Detect hullma change soon with config length {hullma_config.length}"
                    }

            result.append(day_signal)
