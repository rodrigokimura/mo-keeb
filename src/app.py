import os

import pygame
from pynput import keyboard


def callback(display: pygame.surface.Surface, *args, **kwargs):
    key = args[0]
    if isinstance(key, keyboard.KeyCode):
        key = key.char
    else:
        key = key.name

    display.fill("black")
    font = pygame.font.SysFont("freesansbold", 48)
    font_surf = font.render(key, True, "green")
    display.blit(
        font_surf,
        (
            display.get_rect().centerx - font_surf.get_rect().centerx,
            display.get_rect().centery - font_surf.get_rect().centery,
        ),
    )

    path = os.getcwd()
    file = f"{path}/src/key1.wav"
    sound = pygame.mixer.Sound(file)
    sound.play()


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("mo-keeb")
    size = [200, 50]
    display = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    listener = keyboard.Listener(
        on_press=lambda *args, **kwargs: callback(display, *args, **kwargs),
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


if __name__ == "__main__":
    main()
