from datetime import datetime
from typing import List

import pygame
import pygame.freetype

from backends.abstract import Backend
from backends.keyboard import Keyboard
from backends.pynput import Pynput
from constants import CommandData, Modifier
from core.abstract import AbstractApp
from icons import IconImage
from settings import FONT_FILE, MAX_BUFFER_SIZE, SOUND_FILE, Config
from utils import is_windows


class App(AbstractApp):
    def __init__(self, config: Config) -> None:
        self.config = config
        (
            self.top_pad,
            self.right_pad,
            self.bottom_pad,
            self.left_pad,
        ) = self.config.paddings.window
        self.modifiers = {modifier: False for modifier in Modifier}
        self.setup()
        self.keys_buffer: List[CommandData] = []
        self.icons = {
            modifier: IconImage.from_text(modifier.value.desc, self.config)
            for modifier in Modifier
        }
        self.clipping_rect = pygame.rect.Rect(
            self.left_pad,
            self.top_pad,
            (self.display.get_width() - self.right_pad - self.left_pad),
            (self.display.get_height() - self.top_pad - self.bottom_pad),
        )
        if self.config.behavior.backend == "auto":
            backend = Keyboard if is_windows() else Pynput
        else:
            backend = Keyboard if self.config.behavior.backend == "keyboard" else Pynput
        self.backend: Backend = backend(self)

    def setup(self):
        pygame.init()
        pygame.mixer.init()
        self._setup_fonts()
        self._setup_sound()
        pygame.display.set_caption("mo-keeb")
        self.display = pygame.display.set_mode((self.get_width(), self.get_height()))

    def _setup_fonts(self):
        pygame.font.init()
        self.font = pygame.freetype.Font(FONT_FILE, self.config.font_sizes.chars)
        self.font.antialiased = False
        self.font.pad = True

        self.icon_font = pygame.freetype.Font(FONT_FILE, self.config.font_sizes.icons)
        self.icon_font.antialiased = False
        self.icon_font.pad = True

    def _setup_sound(self):
        self.volume = self.config.behavior.volume
        self.channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        self.channel.set_volume(self.volume / 100)
        self.sound = pygame.mixer.Sound(SOUND_FILE)

    def get_width(self):
        _, pad_right, _, pad_left = self.config.paddings.icon
        icon_width = sum(
            self.icon_font.get_rect(m.value.desc).width + pad_left + pad_right
            for m in self.modifiers
        )
        return (
            icon_width
            + (len(self.modifiers) - 1) * self.config.gaps.between_icons
            + self.left_pad
            + self.right_pad
        )

    def get_height(self):
        i_t, _, i_b, _ = self.config.paddings.icon
        font = pygame.freetype.Font(FONT_FILE, self.config.font_sizes.icons)
        font.antialiased = False
        font.pad = True

        text_height = self.font.get_rect("W").height
        icon_height = font.get_rect(Modifier.SHIFT.value.desc).height + i_t + i_b

        return (
            text_height
            + self.config.gaps.below_chars
            + icon_height
            + self.top_pad
            + self.bottom_pad
        )

    def run(self):
        clock = pygame.time.Clock()

        self.backend.setup()

        running = True
        while running:
            clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()

            pygame.display.update()

        pygame.quit()

    def update(self):
        self.display.fill(self.config.colors.background)
        self.update_chars()
        self.update_icons()
        self.display.set_clip(self.clipping_rect)

    def update_chars(self):
        image_data = []
        acc_width = 0
        width = self.display.get_width()
        for key_data in self.keys_buffer:
            key = key_data.key
            typed_at = key_data.typed_at

            delta = datetime.now() - typed_at
            delta = delta.total_seconds()

            key_img, key_rect = self.font.render(key, self.config.colors.chars)
            key_img.set_alpha(int((1 - delta / self.config.behavior.max_age) * 255), 0)
            key_rect.topright = (width - acc_width - self.right_pad, self.top_pad)
            acc_width += key_rect.w
            image_data.append((key_img, key_rect))

            self.display.blit(key_img, key_rect)

    def update_icons(self):
        acc_width = self.left_pad
        height = self.display.get_height()
        for modifier, icon in self.icons.items():
            img = icon.get_image(self.modifiers[modifier])
            self.display.blit(
                img, (acc_width, height - img.get_height() - self.bottom_pad)
            )
            acc_width += img.get_size()[0] + self.config.gaps.between_icons

    def on_press(self, key_name: str):
        mod_pressed = False
        for mod in self.modifiers:
            if mod.value.str_id in key_name:
                self.modifiers[mod] = True
                mod_pressed = True

        if not mod_pressed:
            key_name = change_name_to_symbol(key_name)

            key_data = CommandData(key_name, datetime.now())

            if len(self.keys_buffer) >= MAX_BUFFER_SIZE:
                self.keys_buffer.pop()

            self.keys_buffer.insert(0, key_data)

        self.channel.play(self.sound)

    def on_release(self, key_name: str):
        # special case
        for mod in self.modifiers:
            if mod.value.str_id in key_name:
                self.modifiers[mod] = False


def change_name_to_symbol(key_name: str) -> str:
    mapping = {
        "space": " ",
        "enter": "[E]",
        "backspace": "[BS]",
    }
    return mapping.get(key_name, key_name)
