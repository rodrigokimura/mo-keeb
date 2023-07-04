import os
import sys


def is_windows():
    return os.name == "nt"


def get_asset_path(file_name: str):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "assets", file_name)


def is_in_bunble():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
