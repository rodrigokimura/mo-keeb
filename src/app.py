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


def recolor(
    surf: pygame.surface.Surface, foreground_color: pygame.color.Color | str
) -> pygame.surface.Surface:
    mask = pygame.mask.from_surface(surf)
    transparent = pygame.color.Color(0, 0, 0, 0)

    return mask.to_surface(setcolor=foreground_color, unsetcolor=transparent)


class IconImage(NamedTuple):
    idle: pygame.surface.Surface
    pressed: pygame.surface.Surface

    @classmethod
    def from_file(cls, file: str):
        img = pygame.image.load(file)
        idle = recolor(img, ICON_IDLE_COLOR)
        pressed = recolor(img, ICON_PRESSED_COLOR)
        return cls(idle=idle, pressed=pressed)

    def get_image(self, pressed: bool):
        if pressed:
            return self.pressed
        return self.idle


class App:
    def __init__(self) -> None:
        self.setup()
        self.keys_buffer: List[CommandData] = []
        path = os.getcwd()
        file = f"{path}/src/key1.wav"
        self.volume = VOLUME
        self.channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        self.channel.set_volume(self.volume / 100)
        self.sound = pygame.mixer.Sound(file)
        self.font = pygame.freetype.Font(FONT_FILE, FONT_SIZE)
        self.font.antialiased = False
        self.font.pad = True
        self.padding = WINDOW_PADDING

        self.modifiers = {
            Modifier.SHIFT: False,
            Modifier.CTRL: False,
            Modifier.ALT: False,
            Modifier.META: False,
        }

        self.icons = {
            Modifier.SHIFT: IconImage.from_file(SHIFT_ICON_FILE),
            Modifier.CTRL: IconImage.from_file(CTRL_ICON_FILE),
            Modifier.ALT: IconImage.from_file(ALT_ICON_FILE),
            Modifier.META: IconImage.from_file(SUPER_ICON_FILE),
        }

    def setup(self):
        pygame.init()
        pygame.font.init()

    def run(self):
        pygame.display.set_caption("mo-keeb")
        size = [WINDOW_WIDTH + 2 * self.padding, WINDOW_HEIGTH + 2 * self.padding]

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
            key_rect.topright = ((screen_width - w) - self.padding, self.padding)
            w += key_rect.w
            image_data.append((key_img, key_rect))

            display.blit(key_img, key_rect)

        icon_width = 90
        display.blit(
            self.icons[Modifier.SHIFT].get_image(self.modifiers[Modifier.SHIFT]),
            (self.padding, 50),
        )
        display.blit(
            self.icons[Modifier.CTRL].get_image(self.modifiers[Modifier.CTRL]),
            (self.padding + icon_width, 50),
        )
        display.blit(
            self.icons[Modifier.META].get_image(self.modifiers[Modifier.META]),
            (self.padding + 2 * icon_width, 50),
        )
        display.blit(
            self.icons[Modifier.ALT].get_image(self.modifiers[Modifier.ALT]),
            (self.padding + 3 * icon_width, 50),
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

        self.channel.play(self.sound)

    def on_release(self, key: keyboard.KeyCode | keyboard.Key):
        key_name = self._translate_key_name(key)

        # special case
        for mod_name in self.modifiers.keys():
            if mod_name in key_name:
                self.modifiers[mod_name] = False


def change_name_to_symbol(key_name: str) -> str:
    print(key_name)

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
