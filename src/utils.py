import os
import sys


def is_windows():
    return os.name == "nt"


def get_asset_path(file_name: str):
    root = os.getcwd()
    if is_in_bunble():
        return os.path.join(root, "assets", file_name)
    return os.path.join(root, "src", "assets", file_name)


def is_in_bunble():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
