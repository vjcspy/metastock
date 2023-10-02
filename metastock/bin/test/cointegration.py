from metastock.modules.com.helper.cointegration_test_helper import CointegrationTestHelper
from metastock.modules.stockinfo.value.constain import VNINDEX_SYMBOL

helper = CointegrationTestHelper(
        symbol1='VIN',
        symbol2=VNINDEX_SYMBOL,
)

helper.is_cointegration()

print(f"beta: {helper.beta()}")

vecm = helper.vecm()
print(helper.vecm())
