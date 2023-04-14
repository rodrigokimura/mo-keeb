import os

import pygame


def main():
    pygame.init()
    pygame.display.set_caption("mo-keeb")
    size = [100, 100]
    pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    path = os.getcwd()
    file = f"{path}/src/key1.wav"
    sound = pygame.mixer.Sound(file)

    while running:
        dt = clock.tick(100) / 1000

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                sound.play()

            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
