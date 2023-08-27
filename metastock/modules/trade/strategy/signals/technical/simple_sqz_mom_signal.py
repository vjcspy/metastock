from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract, SignalOutputV1


class SimpleSqzMomSignal(SignalAbstract):

    def support_output_versions(self) -> list[str]:
        return ['@signal_output/v1']

    def get_output(self, version='@signal_output/v1') -> SignalOutputV1:
        match version:
            case '@signal_output/v1':
                pass
            case default:
                return self._get_output_v1()

    def _get_output_v1(self) -> SignalOutputV1:
        return SignalOutputV1()
