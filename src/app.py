import os
from datetime import datetime

import pygame
import pygame.freetype
from pynput import keyboard
from settings import *


class App:
    def __init__(self) -> None:
        self.setup()
        self.keys_buffer = []
        path = os.getcwd()
        file = f"{path}/src/key1.wav"
        self.sound = pygame.mixer.Sound(file)
        self.font = pygame.freetype.Font("src/assets/pixeldroidMenuRegular.ttf", 48)
        self.font.antialiased = False
        self.font.pad = True

    def setup(self):
        pygame.init()
        pygame.font.init()

    def run(self):
        pygame.display.set_caption("mo-keeb")
        w = self.get_max_width()
        size = [w, 50]

        display = pygame.display.set_mode(size)
        display.fill(BACKGROUND_COLOR)

        clock = pygame.time.Clock()
        listener = keyboard.Listener(
            on_press=lambda *args, **kwargs: self.on_press(*args, **kwargs),
        )
        listener.start()

        running = True
        while running:
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            display = pygame.display.get_surface()
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
            key = key_data["key"]
            typed_at: datetime = key_data["typed_at"]
            delta = (datetime.now() - typed_at)
            delta = delta.total_seconds()
            key_img, key_rect = self.font.render(key, FONT_COLOR)
            key_img.set_alpha((1 - delta / MAX_AGE_IN_SECONDS) * 255)
            key_rect.topright = ((screen_width - w) - 5, 0)
            w += key_rect.w
            image_data.append((key_img, key_rect))
            display.blit(key_img, key_rect)

    def get_max_width(self):
        _, font_rect = self.font.render("w", FONT_COLOR)
        return font_rect.w * MAX_CHARS_TO_DISPLAY

    def on_press(
        self, key: keyboard.KeyCode | keyboard.Key
    ):
        if isinstance(key, keyboard.KeyCode):
            key_name = key.char
        elif isinstance(key, keyboard.Key):
            key_name = key.name
        else:
            key_name = ""

        key_name = change_name_to_symbol(key_name)

        key_data = {"key": key_name, "typed_at": datetime.now()}
        self.keys_buffer.append(key_data)

        self.sound.play()


def change_name_to_symbol(key_name: str) -> str:
    mapping = {
        "space": "[_]",
        "ctrl": "[C]",
        "cmd": "[WIN]",
        "enter": "[ENTER]",
    }
    return mapping.get(key_name, key_name)


if __name__ == "__main__":
    app = App()
    app.run()
