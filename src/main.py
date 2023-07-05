import pygame

from core.app import App
from settings import load_config

if __name__ == "__main__":
    config = load_config()
    pygame.init()
    app = App(config)
    app.run()
