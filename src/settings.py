import pathlib
import sys

import tomlkit as tk
from pydantic import BaseModel

from utils import get_asset_path, get_src, is_in_bunble

APP_NAME = "mo-keeb"
CONFIG_FILE_NAME = "config"

MAX_CHARS_TO_DISPLAY = 15
MAX_BUFFER_SIZE = 30

FONT_FILE = get_asset_path("pixeldroidMenuRegular.ttf")
SOUND_FILE = get_asset_path("sound.wav")

class Colors(BaseModel):
    background: str
    chars: str
    icons: str


class FontSizes(BaseModel):
    chars: int
    icons: int


class Paddings(BaseModel):
    window: tuple[int, int, int, int]
    icon: tuple[int, int, int, int]


class Gaps(BaseModel):
    below_chars: int
    between_icons: int


class Behavior(BaseModel):
    max_age: int
    volume: int
    backend: str


class Config(BaseModel):
    colors: Colors
    font_sizes: FontSizes
    paddings: Paddings
    gaps: Gaps
    behavior: Behavior


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
    config.add("behavior", behaviour)

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
    return Config(**config)  # type: ignore
