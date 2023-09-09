from typing import Callable

import pandas as pd

from metastock.modules.com.schema.price_history_schema import priceHistorySchema


class PriceHistoryDfHelper:
    def __init__(self, data, skip_validate = False):

        if not skip_validate and isinstance(data, list) and len(data) > 0:
            priceHistorySchema.load(data[0])
        self._data = data
        self._df = None

    def get_df(self) -> pd.DataFrame:
        """

        :return:
        """
        if self._df is None:
            df = pd.DataFrame(self._data)
            self._df = df.sort_values(by = 'date', ascending = False)
            self._df.reset_index(drop = True, inplace = True)

        return self._df.copy(deep = True)

    def create_source_series(
            self,
            index_col: str = 'date',
            value_func: Callable = lambda row: row['close']
            ) -> pd.Series:
        """
        Tạo một pandas Series từ một DataFrame với index và giá trị được tính toán
        thông qua các tham số.

        Parameters:
        - data: List[Dict[str, any]] - Dữ liệu đầu vào dưới dạng JSON list
        - index_col: str - Tên cột sẽ được sử dụng làm index
        - value_func: Callable - Hàm tính toán giá trị cho mỗi row, được truyền vào dưới dạng lambda

        Returns:
        - pd.Series: Kết quả là một pandas Series
        """
        # Khởi tạo DataFrame từ dữ liệu JSON
        df = self.get_df()

        # Chuyển đổi cột index_col thành kiểu datetime và đặt nó làm index
        if index_col == 'date':
            df[index_col] = pd.to_datetime(df[index_col])

        df.set_index(index_col, inplace = True)

        # Áp dụng function để tính toán giá trị
        result_series = df.apply(value_func, axis = 1)

        return result_series
