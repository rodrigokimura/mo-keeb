import os

import pygame
from pynput import keyboard


class App:
    def __init__(self) -> None:
        self.setup()
        self.keys_buffer = []
        path = os.getcwd()
        file = f"{path}/src/key1.wav"
        self.sound = pygame.mixer.Sound(file)
        self.font = pygame.font.Font("src/assets/pixeldroidMenuRegular.ttf", 48)

    def setup(self):
        pygame.init()
        pygame.font.init()

    def run(self):
        pygame.display.set_caption("mo-keeb")
        size = [200, 50]
        display = pygame.display.set_mode(size)

        clock = pygame.time.Clock()
        listener = keyboard.Listener(
            on_press=lambda *args, **kwargs: self.on_press(display, *args, **kwargs),
        )
        listener.start()

        running = True
        while running:
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            display = pygame.display.get_surface()

            pygame.display.update()

        pygame.quit()

    def on_press(
        self, display: pygame.surface.Surface, key: keyboard.KeyCode | keyboard.Key
    ):
        if isinstance(key, keyboard.KeyCode):
            key_name = key.char
        elif isinstance(key, keyboard.Key):
            key_name = key.name
        else:
            key_name = ""

        key_name = change_name_to_symbol(key_name)

        self.keys_buffer.append(key_name)

        if len(self.keys_buffer) > 5:
            del self.keys_buffer[0]

        text = " ".join(self.keys_buffer)

        display.fill("black")
        # font_surf = self.font.render(text[-10:], True, pygame.color.Color())
        font_surf = self.font.render(text[-10:], True, "#ffffff")
        display.blit(font_surf, (0, 0))
        self.sound.play()


def change_name_to_symbol(key_name: str) -> str:
    mapping = {
        "space": "_",
    }
    return mapping.get(key_name, key_name)


if __name__ == "__main__":
    app = App()
    app.run()
