import pygame

from config.models import Config
from core.app import App

if __name__ == "__main__":
    config = Config.load()
    pygame.init()
    app = App(config)
    app.run()
