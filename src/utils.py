import os


def is_windows():
    return os.name == "nt"


def get_asset_path(file_name: str):
    return f"src/assets/{file_name}"
