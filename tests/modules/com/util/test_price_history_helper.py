import pandas as pd

from metastock.modules.com.util.price_history_helper import PriceHistoryHelper
from metastock.modules.core.util.get_json_data import get_json_data

mock_data = [
        {
                "date": "2023-08-18",
                "high": 19400,
                "low": 18100,
                "close": 18300,
                "open": 19350,
                "volume": 681400,
                "trade": 252,
                "value": 12865663308,
                "buy": 621,
                "buyQuantity": 988639,
                "sell": 486,
                "sellQuantity": 1196777
        },
        {
                "date": "2023-08-17",
                "high": 19650,
                "low": 19400,
                "close": 19450,
                "open": 19400,
                "volume": 304800,
                "trade": 147,
                "value": 5952865920,
                "buy": 431,
                "buyQuantity": 662865,
                "sell": 348,
                "sellQuantity": 732655
        },
        {
                "date": "2023-08-16",
                "high": 19700,
                "low": 19450,
                "close": 19500,
                "open": 19700,
                "volume": 175300,
                "trade": 126,
                "value": 3429544658,
                "buy": 372,
                "buyQuantity": 392805,
                "sell": 288,
                "sellQuantity": 474578
        },
        {
                "date": "2023-08-15",
                "high": 20050,
                "low": 19700,
                "close": 19700,
                "open": 19700,
                "volume": 229700,
                "trade": 142,
                "value": 4545825019,
                "buy": 304,
                "buyQuantity": 505068,
                "sell": 391,
                "sellQuantity": 674611
        },
        {
                "date": "2023-08-14",
                "high": 20000,
                "low": 19350,
                "close": 19700,
                "open": 20000,
                "volume": 300100,
                "trade": 193,
                "value": 5896139725,
                "buy": 483,
                "buyQuantity": 757618,
                "sell": 449,
                "sellQuantity": 843083
        }
]


class TestPriceHistoryHelper:
    """
    Unit test class for PriceHistoryHelper.
    """

    def setup_method(self):
        """
        Set up the test environment by preparing data for each test case.
        """
        data = {
                "date": ["2023-08-18", "2023-08-17", "2023-08-16"],
                "close": [18300, 19450, 19500]
        }
        self.df = pd.DataFrame(data)
        self.helper = PriceHistoryHelper(self.df, skip_validate = True)

    def test_sma(self):
        """
        Test the SMA (Simple Moving Average) calculation.

        - Check the SMA value when there is enough data.
        - Check the SMA value when there is not enough data.
        """
        self.helper.set_date("2023-08-18")
        assert self.helper.sma(2) == (18300 + 19450) / 2

        self.helper.set_date("2023-08-17")
        assert self.helper.sma(3) is None

    def test_get_current_price(self):
        """
        Test the retrieval of the current price.

        - Check if the retrieved current price matches the expected row.
        """
        self.helper.set_date("2023-08-18")
        expected_row = self.df[self.df["date"] == "2023-08-18"].iloc[0]
        current_price = self.helper.get_current_price()
        pd.testing.assert_series_equal(current_price, expected_row)

    def test_set_date(self):
        """
        Test the setting of the date.

        - Check if the date is set correctly.
        """
        new_date = "2023-08-16"
        self.helper.set_date(new_date)
        assert self.helper._date == new_date


class TestPriceHistoryHelperStdev:
    """
    Unit test class for PriceHistoryHelper's stdev function.
    """

    def setup_method(self):
        """
        Set up the test environment by creating a sample DataFrame.
        """
        data = {
                'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'],
                'close': [10, 15, 20, 25],
                'high': [15, 20, 25, 30],
                'low': [5, 10, 15, 20],
        }
        self.df = pd.DataFrame(data)
        self.helper = PriceHistoryHelper(self.df, skip_validate = True)

    def test_stdev(self):
        """
        Test the standard deviation calculation.

        - Check the standard deviation value with valid length and default source function.
        - Check the standard deviation value with valid length and custom source function.
        - Check the standard deviation value with invalid length.
        """
        self.helper.set_date('2022-01-04')
        stdev = self.helper.stdev(3)
        assert stdev == 5

        def custom_source_func(row):
            return row['high'] - row['low']

        self.helper.set_date('2022-01-03')
        stdev = self.helper.stdev(2, cal_source_func = custom_source_func)
        assert stdev == 0

        self.helper.set_date('2022-01-01')
        assert self.helper.stdev(5) is None


class TestPriceHistoryHelperRealData:
    """
    Unit test class for PriceHistoryHelper using real data.
    """

    def test_init_data(self):
        """
        Test the initialization of data from a real source.

        - Check if the data is retrieved successfully.
        - Check if the standard deviation can be calculated with the retrieved data.
        """
        data = get_json_data("http://localhost:3000/stock-price/history?code=BFC&from=2023-07-01")

        if data is not None:
            helper = PriceHistoryHelper(data)
            helper.set_date("2023-08-18")
            stdev = helper.stdev(7)
            assert stdev is not None


class TestPriceHistoryHelperTrueRangeAndPreviousClose:

    def setup_method(self):
        # Create a sample DataFrame for testing
        data = [
                {'date': '2022-01-01', 'high': 10, 'low': 5, 'close': 8},
                {'date': '2022-01-02', 'high': 15, 'low': 7, 'close': 12},
                {'date': '2022-01-03', 'high': 20, 'low': 10, 'close': 18}
        ]
        self.helper = PriceHistoryHelper(data, skip_validate = True)

    def test_true_range_by_date(self):
        # Test true range calculation for a valid date
        assert self.helper.true_range_by_date('2022-01-02') == 8

        # Test true range calculation for a date with missing previous close value
        assert self.helper.true_range_by_date('2022-01-01') is None

        # Test true range calculation for a date with missing target row
        assert self.helper.true_range_by_date('2022-01-04') is None

    def test_get_previous_close_by_date(self):
        # Test getting previous close for a valid date
        assert self.helper.get_previous_close_by_date('2022-01-02') == 8

        # Test getting previous close for a date with missing previous close value
        assert self.helper.get_previous_close_by_date('2022-01-01') is None

        # Test getting previous close for a date with missing target row
        assert self.helper.get_previous_close_by_date('2022-01-04') is None


class TestPriceHistoryHelperGetPreviousRowByDate:

    def setup_method(self):
        self.data = mock_data

    def test_get_previous_row_by_date(self):
        helper = PriceHistoryHelper(self.data)

        # Test for previous row with 1 day difference
        prev_row_1 = helper.get_previous_row_by_date("2023-08-18", days = 1)
        expected_prev_row_1 = {
                "date": "2023-08-17",
                "high": 19650,
                "low": 19400,
                "close": 19450,
                "open": 19400,
                "volume": 304800,
                "trade": 147,
                "value": 5952865920,
                "buy": 431,
                "buyQuantity": 662865,
                "sell": 348,
                "sellQuantity": 732655
        }
        assert prev_row_1.to_dict() == expected_prev_row_1

        # Test for previous row with 2 days difference
        prev_row_2 = helper.get_previous_row_by_date("2023-08-16", days = 2)
        expected_prev_row_2 = {
                "date": "2023-08-14",
                "high": 20000,
                "low": 19350,
                "close": 19700,
                "open": 20000,
                "volume": 300100,
                "trade": 193,
                "value": 5896139725,
                "buy": 483,
                "buyQuantity": 757618,
                "sell": 449,
                "sellQuantity": 843083
        }
        assert prev_row_2.to_dict() == expected_prev_row_2

        # Test for previous row with 0 days difference (same date)
        prev_row_0 = helper.get_previous_row_by_date("2023-08-16", days = 3)
        assert prev_row_0 is None


class TestPriceHistoryHelperGetSubsetRowsByDate:

    def setup_method(self):
        self.data = mock_data

    def test_get_subset_rows_by_date(self):
        helper = PriceHistoryHelper(self.data)

        # Test for subset rows with 1 day difference
        subset_rows_1 = helper.get_subset_rows_by_date("2023-08-18", days = 1)
        expected_subset_rows_1 = [
                {
                        "date": "2023-08-18",
                        "high": 19400,
                        "low": 18100,
                        "close": 18300,
                        "open": 19350,
                        "volume": 681400,
                        "trade": 252,
                        "value": 12865663308,
                        "buy": 621,
                        "buyQuantity": 988639,
                        "sell": 486,
                        "sellQuantity": 1196777
                },
        ]
        pd.testing.assert_frame_equal(subset_rows_1, pd.DataFrame(expected_subset_rows_1))

        # Test for subset rows with 1 day difference
        subset_rows_2 = helper.get_subset_rows_by_date("2023-08-15", days = 2)
        expected_subset_rows_2 = [
                {
                        "date": "2023-08-15",
                        "high": 20050,
                        "low": 19700,
                        "close": 19700,
                        "open": 19700,
                        "volume": 229700,
                        "trade": 142,
                        "value": 4545825019,
                        "buy": 304,
                        "buyQuantity": 505068,
                        "sell": 391,
                        "sellQuantity": 674611
                },
                {
                        "date": "2023-08-14",
                        "high": 20000,
                        "low": 19350,
                        "close": 19700,
                        "open": 20000,
                        "volume": 300100,
                        "trade": 193,
                        "value": 5896139725,
                        "buy": 483,
                        "buyQuantity": 757618,
                        "sell": 449,
                        "sellQuantity": 843083
                }
        ]
        pd.testing.assert_frame_equal(
            subset_rows_2.reset_index(drop = True), pd.DataFrame(expected_subset_rows_2),
            check_index_type = False
            )
