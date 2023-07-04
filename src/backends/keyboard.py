import keyboard

from backends.abstract import Backend
from constants import Modifier
from core.abstract import AbstractApp


class Keyboard(Backend):
    def __init__(self, app: AbstractApp) -> None:
        self.app = app

    def setup(self):
        keyboard.hook(self.on_event)

    def on_event(self, ev: keyboard.KeyboardEvent):
        if ev.event_type == keyboard.KEY_UP:
            self.on_release(ev)
        elif ev.event_type == keyboard.KEY_DOWN:
            self.on_press(ev)

    def on_press(self, ev: keyboard.KeyboardEvent):
        key_name = self._translate_key(ev.name or "")
        self.app.on_press(key_name)

    def on_release(self, ev: keyboard.KeyboardEvent):
        key_name = self._translate_key(ev.name or "")
        self.app.on_release(key_name)

    def _translate_key(self, key: str):
        if "windows" in key:
            return Modifier.META.value.str_id
        return key
