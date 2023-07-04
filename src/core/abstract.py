from abc import ABC, abstractmethod

from constants import Modifier


class AbstractApp(ABC):
    modifiers: dict[Modifier, bool]

    @abstractmethod
    def on_press(self, key_name: str):
        ...

    @abstractmethod
    def on_release(self, key_name: str):
        ...
