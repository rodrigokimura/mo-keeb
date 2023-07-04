from pynput import keyboard as keyboard

from backends.abstract import Backend
from core.abstract import AbstractApp


class Pynput(Backend):
    def __init__(self, app: AbstractApp) -> None:
        self.app = app

    def setup(self):
        listener = keyboard.Listener(
            on_press=lambda *args, **kwargs: self.on_press(*args, **kwargs),
            on_release=lambda *args, **kwargs: self.on_release(*args, **kwargs),
        )
        listener.start()

    def _translate_key_name(self, key: keyboard.KeyCode | keyboard.Key):
        if isinstance(key, keyboard.KeyCode):
            key_name = key.char or ""
            # HACK: force this to alt_gr
            if key.vk == 65027:
                key_name = "alt_gr"
        elif isinstance(key, keyboard.Key):
            key_name = key.name
        else:
            key_name = ""
        return key_name

    def on_press(self, key: keyboard.KeyCode | keyboard.Key):
        key_name = self._translate_key_name(key)
        self.app.on_press(key_name)

    def on_release(self, key: keyboard.KeyCode | keyboard.Key):
        key_name = self._translate_key_name(key)
        self.app.on_release(key_name)
