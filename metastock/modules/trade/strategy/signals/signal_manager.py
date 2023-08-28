from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class ASignalManager(AbstractManager):
    INSTANCE = None


def signal_manager() -> ASignalManager:
    if ASignalManager.INSTANCE is None:
        ASignalManager.INSTANCE = ASignalManager()

    return ASignalManager.INSTANCE
