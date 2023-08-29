from metastock.modules.trade.strategy.filters.capitalization_filter import CapitalizationFilter
from metastock.modules.trade.strategy.filters.filter_manager import filter_manager
from metastock.modules.trade.strategy.filters.specific_symbols_filter import SpecificSymbolsFilter

TRADING_STRATEGY_FILTERS = {
        CapitalizationFilter.name: {
                "class": CapitalizationFilter
        },
        SpecificSymbolsFilter.name: {
                "class": SpecificSymbolsFilter
        }
}

for key, value in TRADING_STRATEGY_FILTERS.items():
    filter_manager().define(key, value)
