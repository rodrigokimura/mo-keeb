import pathlib
import sys
from typing import Literal

import tomlkit as tk

from utils import get_asset_path, get_src, is_in_bunble, is_windows

APP_NAME = "mo-keeb"
CONFIG_FILE_NAME = "config"

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

FONT_FILE = get_asset_path("pixeldroidMenuRegular.ttf")
SOUND_FILE = get_asset_path("sound.wav")


def get_config_file():
    extensions = ["toml", "json"]
    dir_to_check = get_config_dir()
    options = (
        dir_to_check / f"{CONFIG_FILE_NAME}.{ext}"
        for _ext in extensions
        for ext in [_ext.lower(), _ext.upper()]
    )
    for option in options:
        if option.exists():
            return option
    return None


def get_config_dir():
    if is_in_bunble():
        return pathlib.Path(sys.executable).parent
    return get_src().parent


def write_default_config():
    config = tk.document()
    config.add(tk.comment("mo-keeb's config file"))
    config.add(tk.nl())

    colors = tk.table()
    colors["background"] = "#1d3557"
    colors["chars"] = "#f1faee"
    colors["icons"] = "#caf0f8"
    config.add("colors", colors)

    font_sizes = tk.table()
    font_sizes["chars"] = 48
    font_sizes["icons"] = 24
    config.add("font_sizes", font_sizes)

    paddings = tk.table()
    paddings["window"] = [10, 10, 10, 10]
    paddings["icon"] = [5, 10, 5, 10]
    config.add("paddings", paddings)

    gaps = tk.table()
    gaps["below_chars"] = 10
    gaps["between_icons"] = 5
    config.add("gaps", gaps)

    behaviour = tk.table()
    behaviour["max_age"] = 5
    behaviour["volume"] = 50
    behaviour["backend"] = "auto"
    config.add("behaviour", behaviour)

    with open(get_config_dir() / f"{CONFIG_FILE_NAME}.toml", "w") as file:
        return tk.dump(config, file)


def load_config():
    file = get_config_file()
    if file is None:
        write_default_config()
        file = get_config_file()
        if file is None:
            raise ValueError("Failed to create config file")
    with open(file, "r") as file:
        config = tk.load(file)

    print(config)
