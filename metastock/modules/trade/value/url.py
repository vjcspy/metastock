from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.environment import env


class TradeUrlValue:
    LIVE_BASE_URL = "https://stock.ngocdiep.top"

    TRADING_STRATEGY_PROCESS_URL = (
        env().get("PS_API_END_POINT") + "/strategy/process"
        if env().get("PS_API_END_POINT") is not None
        else None
    )

    STOCK_TRADING_ANALYSIS_HULLMA_URL = (
        env().get("PS_API_END_POINT") + "/stock-trading/analysis/hullma"
        if env().get("PS_API_END_POINT") is not None
        else None
    )

    def get_stock_trading_analysis_url(self):
        return f"{TradeUrlValue.LIVE_BASE_URL}/stock-trading/analysis"

    def get_stock_trading_save_analysis_url(self):
        base_url = self._get_base_url()

        return f"{base_url}/stock-trading/analysis"

    def get_stock_trading_bulk_submit(self):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/bulk-submit-action"

    def get_stock_trading_patch_process(self):
        base_url = self._get_base_url()

        return f"{base_url}/strategy/process"

    def _get_base_url(self):
        if env().get("PS_API_END_POINT") is None:
            raise AppError("Missing PS_API_END_POINT env config")

        return env().get("PS_API_END_POINT")
