import os


def is_windows():
    return os.name == "nt"


def get_path(relative_path: str):
    return f"src/{relative_path}"
