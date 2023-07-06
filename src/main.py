import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from config.models import Config
from core.app import App

if __name__ == "__main__":
    import pygame

    config = Config.load()
    pygame.init()
    app = App(config)
    app.run()
