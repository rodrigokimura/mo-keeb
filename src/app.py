import enum
import os
from datetime import datetime
from typing import List, NamedTuple

import pygame
import pygame.freetype
from pynput import keyboard

from settings import *


class CommandData(NamedTuple):
    key: str
    typed_at: datetime


class Modifier(enum.StrEnum):
    META = "cmd"
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"


class App:
    def __init__(self) -> None:
        self.setup()
        self.keys_buffer: List[CommandData] = []
        path = os.getcwd()
        file = f"{path}/src/key1.wav"
        self.sound = pygame.mixer.Sound(file)
        self.font = pygame.freetype.Font("src/assets/pixeldroidMenuRegular.ttf", 48)
        self.font.antialiased = False
        self.font.pad = True

        self.modifiers = {
            Modifier.SHIFT: False,
            Modifier.CTRL: False,
            Modifier.ALT: False,
            Modifier.META: False,
        }

    def setup(self):
        pygame.init()
        pygame.font.init()

    def run(self):
        pygame.display.set_caption("mo-keeb")
        w = self.get_max_width()
        size = [w, 120]

        display = pygame.display.set_mode(size)
        display.fill(BACKGROUND_COLOR)

        clock = pygame.time.Clock()
        listener = keyboard.Listener(
            on_press=lambda *args, **kwargs: self.on_press(*args, **kwargs),
            on_release=lambda *args, **kwargs: self.on_release(*args, **kwargs),
        )
        listener.start()

        running = True
        while running:
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # display = pygame.display.get_surface()
            self.update_chars(display)

            pygame.display.update()

        pygame.quit()

    def update_chars(self, display: pygame.surface.Surface):
        image_data = []

        display.fill(BACKGROUND_COLOR)

        reversed = self.keys_buffer.copy()
        reversed.reverse()
        w = 0
        screen_width = display.get_size()[0]
        for key_data in reversed:
            key = key_data.key
            typed_at = key_data.typed_at

            delta = datetime.now() - typed_at
            delta = delta.total_seconds()

            key_img, key_rect = self.font.render(key, FONT_COLOR)
            key_img.set_alpha(int((1 - delta / MAX_AGE_IN_SECONDS) * 255), 0)
            key_rect.topright = ((screen_width - w) - 5, 0)
            w += key_rect.w
            image_data.append((key_img, key_rect))

            display.blit(key_img, key_rect)

        pygame.draw.circle(
            display, "red", (50, 50), 10, 0 if self.modifiers[Modifier.SHIFT] else 1
        )
        pygame.draw.circle(
            display, "blue", (70, 50), 10, 0 if self.modifiers[Modifier.CTRL] else 1
        )
        pygame.draw.circle(
            display, "yellow", (90, 50), 10, 0 if self.modifiers[Modifier.ALT] else 1
        )
        pygame.draw.circle(
            display, "white", (110, 50), 10, 0 if self.modifiers[Modifier.META] else 1
        )

    def get_max_width(self):
        _, font_rect = self.font.render("w", FONT_COLOR)
        return font_rect.w * MAX_CHARS_TO_DISPLAY

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

        mod_pressed = False
        for mod_name in self.modifiers.keys():
            if mod_name in key_name:
                self.modifiers[mod_name] = True
                mod_pressed = True

        if not mod_pressed:
            key_name = change_name_to_symbol(key_name)

            key_data = CommandData(key_name, datetime.now())

            if len(self.keys_buffer) >= MAX_BUFFER_SIZE:
                del self.keys_buffer[0]

            self.keys_buffer.append(key_data)

        self.sound.play()

    def on_release(self, key: keyboard.KeyCode | keyboard.Key):
        key_name = self._translate_key_name(key)

        # special case
        for mod_name in self.modifiers.keys():
            if mod_name in key_name:
                self.modifiers[mod_name] = False
        # self.sound.play()


def change_name_to_symbol(key_name: str) -> str:
    mapping = {
        "space": " ",
        # "ctrl": "[C]",
        # "ctrl_r": "[C]",
        # "alt": "[A]",
        # "shift": "[S]",
        # "shift_r": "[S]",
        # "cmd": "[W]",
        "enter": "[E]",
        "backspace": "[BS]",
    }
    return mapping.get(key_name, key_name)


if __name__ == "__main__":
    app = App()
    app.run()
