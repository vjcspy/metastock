import numpy as np
import pandas as pd

from metastock import Logger
from metastock.bin.test.get_history_data import get_history_data
from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.hullma import Hullma

history_data = get_history_data(symbol = 'VCB')

priceHelper = PriceHistoryDfHelper(history_data)

hullma = Hullma(history = history_data)
hulma_data = hullma.get_data()
Logger().info(hulma_data.head(20))


def predict_trend_change(wma_series: pd.Series, n: int) -> pd.DataFrame:
    results = []

    for i in range(n, len(wma_series)):
        y = wma_series.iloc[i - n:i][::-1].diff().values[1:]  # Bỏ qua giá trị đầu tiên NaN từ .diff()
        x = np.arange(len(y))

        # Áp dụng bình phương nhỏ nhất để tìm hệ số góc
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond = None)[0]

        # Dự đoán số ngày để đổi chiều
        if m != 0:
            days_to_zero = -c / m
        else:
            days_to_zero = np.inf  # Nếu m = 0, không thể dự đoán khi nào đổi chiều
            trend = "Stable"

        results.append(
                {
                        "Date": wma_series.index[i],
                        "Slope": m,
                        "Days to Zero Change": days_to_zero if 0 < days_to_zero < 3 else None
                }
        )

    return pd.DataFrame(results).set_index("Date")


predic = predict_trend_change(hulma_data.head(80), 5)

Logger().info(predic)
