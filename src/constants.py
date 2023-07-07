import enum
from datetime import datetime
from typing import NamedTuple

from utils import get_asset_path

APP_NAME = "mo-keeb"
CONFIG_FILE_NAME = "config"

MAX_CHARS_TO_DISPLAY = 15
MAX_BUFFER_SIZE = 30

SOUND_FILE = get_asset_path("sound.wav")


class CommandData(NamedTuple):
    key: str
    typed_at: datetime


class ModifierData(NamedTuple):
    str_id: str
    desc: str


class Modifier(enum.Enum):
    SHIFT = ModifierData("shift", "SHIFT")
    CTRL = ModifierData("ctrl", "CTRL")
    META = ModifierData("cmd", "SUPER")
    ALT = ModifierData("alt", "ALT")


class BackendOption(enum.StrEnum):
    AUTO = "auto"
    PYNPUT = "pynput"
    KEYBOARD = "keyboard"


class FontOption(enum.StrEnum):
    SCIENTIFICA = "scientifica"
    PIXELDROID_MENU = "pixeldroid_menu"
    MONOCRAFT = "monocraft"


class ProfileOption(enum.StrEnum):
    RED = "red"
    BLUE = "blue"
    BROWN = "brown"
