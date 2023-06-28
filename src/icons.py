from typing import NamedTuple

import pygame
import pygame.freetype

from settings import FONT_FILE, ICON_COLOR, ICON_FONT_SIZE, ICON_PADDING


def recolor(
    surf: pygame.surface.Surface, foreground_color: pygame.color.Color | str
) -> pygame.surface.Surface:
    mask = pygame.mask.from_surface(surf)
    transparent = pygame.color.Color(0, 0, 0, 0)

    return mask.to_surface(setcolor=foreground_color, unsetcolor=transparent)


def draw_text_in_a_box(
    text: str,
    font: pygame.freetype.Font,
    color: pygame.color.Color | str,
    padding: tuple[int, int, int, int],
):
    pad_top, pad_right, pad_bottom, pad_left = padding
    transparent = pygame.color.Color(0, 0, 0, 0)
    text_img, rect = font.render(text, color, transparent)
    rect.width += pad_left + pad_right
    rect.height += pad_top + pad_bottom

    img = pygame.surface.Surface(rect.size).convert_alpha()
    img.fill(transparent)
    img.blit(text_img, (pad_left, pad_top))

    pygame.draw.rect(img, color, img.get_rect(), 1)
    return img


class IconImage(NamedTuple):
    idle: pygame.surface.Surface
    pressed: pygame.surface.Surface

    @classmethod
    def from_text(cls, text: str):
        padding = ICON_PADDING
        font = pygame.freetype.Font(FONT_FILE, ICON_FONT_SIZE)
        font.antialiased = False
        font.pad = True
        pressed = draw_text_in_a_box(text, font, ICON_COLOR, padding)
        idle = pressed.copy()
        idle.set_alpha(100)
        return cls(idle=idle, pressed=pressed)

    @classmethod
    def from_file(cls, file: str):
        img = pygame.image.load(file)
        pressed = recolor(img, ICON_COLOR)
        idle = pressed.copy()
        idle.set_alpha(100)
        return cls(idle=idle, pressed=pressed)

    def get_image(self, pressed: bool):
        if pressed:
            return self.pressed
        return self.idle
