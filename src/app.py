import os
from datetime import datetime
from typing import List

import pygame
import pygame.freetype
from pynput import keyboard

from constants import CommandData, Modifier
from icons import IconImage
from settings import *


class App:
    def __init__(self) -> None:
        self.top_pad, self.right_pad, self.bottom_pad, self.left_pad = WINDOW_PADDING
        self.modifiers = {modifier: False for modifier in Modifier}
        self.icon_gap = ICON_GAP
        self.setup()
        self.keys_buffer: List[CommandData] = []
        self.icons = {
            modifier: IconImage.from_text(modifier.value.desc) for modifier in Modifier
        }
        self.clipping_rect = pygame.rect.Rect(
            self.left_pad,
            self.top_pad,
            (self.display.get_width() - self.right_pad - self.left_pad),
            (self.display.get_height() - self.top_pad - self.bottom_pad),
        )

    def setup(self):
        pygame.init()
        self._setup_fonts()
        self._setup_sound()
        pygame.display.set_caption("mo-keeb")
        self.display = pygame.display.set_mode((self.get_width(), self.get_height()))

    def _setup_fonts(self):
        pygame.font.init()
        self.font = pygame.freetype.Font(FONT_FILE, CHARS_FONT_SIZE)
        self.font.antialiased = False
        self.font.pad = True

        self.icon_font = pygame.freetype.Font(FONT_FILE, ICON_FONT_SIZE)
        self.icon_font.antialiased = False
        self.icon_font.pad = True

    def _setup_sound(self):
        path = os.getcwd()
        file = f"{path}/src/key1.wav"
        self.volume = VOLUME
        self.channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        self.channel.set_volume(self.volume / 100)
        self.sound = pygame.mixer.Sound(file)

    def get_width(self):
        _, pad_right, _, pad_left = ICON_PADDING
        icon_width = sum(
            self.icon_font.get_rect(m.value.desc).width + pad_left + pad_right
            for m in self.modifiers
        )
        return (
            icon_width
            + (len(self.modifiers) - 1) * self.icon_gap
            + self.left_pad
            + self.right_pad
        )

    def get_height(self):
        i_t, _, i_b, _ = ICON_PADDING
        font = pygame.freetype.Font(FONT_FILE, ICON_FONT_SIZE)
        font.antialiased = False
        font.pad = True

        text_height = self.font.get_rect("W").height
        icon_height = font.get_rect(Modifier.SHIFT.value.desc).height + i_t + i_b

        return (
            text_height + TEXT_ICON_GAP + icon_height + self.top_pad + self.bottom_pad
        )

    def run(self):
        self.display.fill(BACKGROUND_COLOR)

        clock = pygame.time.Clock()
        listener = keyboard.Listener(
            on_press=lambda *args, **kwargs: self.on_press(*args, **kwargs),
            on_release=lambda *args, **kwargs: self.on_release(*args, **kwargs),
        )
        listener.start()

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
        self.display.fill(BACKGROUND_COLOR)
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

            key_img, key_rect = self.font.render(key, CHARS_COLOR)
            key_img.set_alpha(int((1 - delta / MAX_AGE_IN_SECONDS) * 255), 0)
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
            acc_width += img.get_size()[0] + self.icon_gap

    def _translate_key_name(self, key: keyboard.KeyCode | keyboard.Key):
        print(key)
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
        # if len(key_name) == 1:
        #     print(chr(ord("C")-64) == key_name)
        #     print(chr(ord("c")-64) == key_name)

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

    def on_release(self, key: keyboard.KeyCode | keyboard.Key):
        key_name = self._translate_key_name(key)

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


if __name__ == "__main__":
    app = App()
    app.run()
