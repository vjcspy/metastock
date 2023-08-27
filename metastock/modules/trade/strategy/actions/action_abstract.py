from abc import ABC, abstractmethod


class ActionAbstract(ABC):
    @abstractmethod
    def support_signal_output_versions(self) -> list[str]:
        pass
