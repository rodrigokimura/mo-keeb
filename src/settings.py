from typing import Literal

from utils import get_path, is_windows

BACKGROUND_COLOR = "#1d3557"
CHARS_COLOR = "#f1faee"
ICON_COLOR = "#caf0f8"

CHARS_FONT_SIZE = 48
ICON_FONT_SIZE = 24
WINDOW_PADDING = (10, 10, 10, 10)  # top, right, bottom, left
ICON_PADDING = (5, 10, 5, 10)
TEXT_ICON_GAP = 10
ICON_GAP = 5

MAX_CHARS_TO_DISPLAY = 15
MAX_AGE_IN_SECONDS = 5
MAX_BUFFER_SIZE = 30
VOLUME = 50

BACKEND: Literal["keyboard"] | Literal["pynput"] = (
    "keyboard" if is_windows() else "pynput"
)

FONT_FILE = get_path("assets/pixeldroidMenuRegular.ttf")
SOUND_FILE = get_path("key1.wav")
