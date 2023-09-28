import pytest
from metastock.modules.com.technical_indicator.sqz_mom import SqzMomConfig, SqzMom
import json
import os


@pytest.fixture
def setup_data():
    cur_path = os.path.dirname(__file__)
    string_to_remove = 'modules/com/technical_indicator'
    index = cur_path.find(string_to_remove)
    new_cur_path = cur_path[:index] + cur_path[index + len(string_to_remove):]
    f = open(new_cur_path + 'mock_data/bfc_history_small.json')
    data = json.load(f)
    return data


# def test_get_value(setup_data):
#     sqz_config = SqzMomConfig()
#     sqz = SqzMom(setup_data)
#     sqz.set_config(sqz_config)
#
#     sqzs = []
#     for i in range(3):
#         date = setup_data[i]['date']
#         value, sqzOn, sqzOff, noSqz = sqz.set_date(date).get_data()
#         sqzs.append(value)
#
#     expected = [-422, -207, -150]
#     assert sqzs == expected
