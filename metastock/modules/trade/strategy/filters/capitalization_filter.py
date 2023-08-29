from metastock.modules.trade.strategy.filters.filter_abstract import FilterAbstract


class CapitalizationFilter(FilterAbstract):
    name = 'capitalization_filter'

    def filter(self, symbol: str) -> bool:
        return True
