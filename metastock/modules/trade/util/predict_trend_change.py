import numpy as np
import pandas as pd


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
                        "date": wma_series.index[i],
                        "slope": m,
                        "estimate_day_change": days_to_zero if 0 < days_to_zero < 3 else None
                }
        )

    return pd.DataFrame(results).set_index("date")
