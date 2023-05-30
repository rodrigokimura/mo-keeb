import os

import pygame


def play():
    path = os.getcwd()
    file = f"{path}/src/key1.wav"
    sound = pygame.mixer.Sound(file)
    sound.play()
