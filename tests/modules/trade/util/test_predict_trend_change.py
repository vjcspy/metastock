# Tạo một bộ dữ liệu mẫu cho việc kiểm tra
import pandas as pd

from metastock.modules.trade.util.predict_trend_change import predict_trend_change


def test_predict_trend_change():
    # Tạo một pd.Series giả lập
    wma_series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    n = 3

    # Gọi hàm predict_trend_change
    result_df = predict_trend_change(wma_series, n)

    # Kiểm tra xem kết quả có đúng kiểu dữ liệu là pd.DataFrame không
    assert isinstance(result_df, pd.DataFrame)

    # # Kiểm tra xem DataFrame có cột 'Date', 'Slope', 'Days to Zero Change' không
    # assert 'Date' in result_df.columns
    # assert 'Slope' in result_df.columns
    # assert 'Days to Zero Change' in result_df.columns
    #
    # # Kiểm tra xem 'Days to Zero Change' có giá trị NaN (vì không thể dự đoán) khi Slope = 0 không
    # assert pd.isna(result_df['Days to Zero Change'].iloc[2])
