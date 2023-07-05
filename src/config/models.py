import pathlib
import sys

import tomlkit as tk
from pydantic import BaseModel, Field

from constants import CONFIG_FILE_NAME, BackendOption
from utils import get_src, is_in_bunble


class Colors(BaseModel):
    background: str = Field(default="#1d3557")
    chars: str = Field(default="#f1faee")
    icons: str = Field(default="#caf0f8")


class FontSizes(BaseModel):
    chars: int = Field(default=48)
    icons: int = Field(default=24)


class Paddings(BaseModel):
    window: tuple[int, int, int, int] = Field(default=(10, 10, 10, 10))
    icon: tuple[int, int, int, int] = Field(default=(5, 10, 5, 10))


class Gaps(BaseModel):
    below_chars: int = Field(default=10)
    between_icons: int = Field(default=5)


class Behavior(BaseModel):
    max_age: int = Field(default=5, description="in seconds")
    volume: int = Field(default=50, description="from 0 to 100")
    backend: BackendOption = Field(
        default=BackendOption.AUTO.value,
        description=f"choices are: {list(opt.value for opt in BackendOption)}",
    )


class Config(BaseModel):
    colors: Colors = Field(default=Colors(), description="in hex")
    font_sizes: FontSizes = Field(default=FontSizes())
    paddings: Paddings = Field(
        default=Paddings(), description="top, right, left, bottom"
    )
    gaps: Gaps = Field(default=Gaps())
    behavior: Behavior = Field(default=Behavior())

    @classmethod
    def _get_config_file(cls):
        extensions = ["toml", "json"]
        dir_to_check = cls._get_config_dir()
        options = (
            dir_to_check / f"{CONFIG_FILE_NAME}.{ext}"
            for _ext in extensions
            for ext in [_ext.lower(), _ext.upper()]
        )
        for option in options:
            if option.exists():
                return option
        return None

    @staticmethod
    def _get_config_dir():
        if is_in_bunble():
            return pathlib.Path(sys.executable).parent
        return get_src().parent

    @classmethod
    def _get_table(cls, model: BaseModel):
        table = tk.table()
        for name, info in model.model_fields.items():
            attr = getattr(model, name)
            if isinstance(attr, BaseModel):
                cls._get_table(attr)
            else:
                table[name] = attr
                if desc := info.description:
                    table[name].comment(desc)
        return table

    @classmethod
    def _write_default_config(cls):
        config = tk.document()
        config.add(tk.comment("mo-keeb's config file"))
        config.add(tk.nl())
        default_config = cls()

        for name, info in default_config.model_fields.items():
            field = getattr(default_config, name)
            if not isinstance(field, BaseModel):
                continue

            table = cls._get_table(field)
            if desc := info.description:
                table.comment(desc)
            config.add(name, table)

        with open(cls._get_config_dir() / f"{CONFIG_FILE_NAME}.toml", "w") as file:
            return tk.dump(config, file)

    @classmethod
    def load(cls):
        file = cls._get_config_file()
        if file is None:
            cls._write_default_config()
            file = cls._get_config_file()
            if file is None:
                raise ValueError("Failed to create config file")
        with open(file, "r") as file:
            config = tk.load(file)
        return Config(**config)  # type: ignore
