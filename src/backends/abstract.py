from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def setup(self):
        ...
