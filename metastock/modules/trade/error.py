from metastock.modules.core.util.app_error import AppError


class TradeFileNotFoundError(AppError):
    def __init__(self, message='Please check your config', code='trade_general_error_000'):
        super().__init__(message, code)


class StrategyNotFound(AppError):
    def __init__(self, message='Please check your strategy config', code='trade_general_error_000'):
        super().__init__(message, code)


class NotSupportConfigType(AppError):
    def __init__(self, message='Please check your config', code='trade_general_error_000'):
        super().__init__(message, code)
