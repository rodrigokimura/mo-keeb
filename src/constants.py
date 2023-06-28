import enum
from datetime import datetime
from typing import NamedTuple


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
