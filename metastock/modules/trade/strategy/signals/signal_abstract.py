from abc import abstractmethod, ABC


class SignalOutputV1:
    pass


class SignalOutputV2:
    pass


class SignalAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def support_output_versions(self) -> list[str]:
        pass

    @abstractmethod
    def get_output(self, version='v1') -> SignalOutputV1 | SignalOutputV2:
        pass
