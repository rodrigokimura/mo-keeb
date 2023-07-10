import os

import PyInstaller.__main__

from constants import APP_NAME
from utils import get_asset_path, is_linux, is_macos, is_windows


def build():
    executable_name = get_executable_file_name(APP_NAME)
    script = os.path.join(os.path.abspath(os.path.dirname(__file__)), "main.py")
    assets = get_asset_path("*")
    sep = os.pathsep
    bundled_assets = "./assets"
    options = [
        "noconfirm",
        "clean",
        "onefile",
        "noconsole",
        f"name {executable_name}",
        f"add-data {assets}{sep}{bundled_assets}",
        f"add-data {get_asset_path('sounds')/'blue'/'*'}{sep}{bundled_assets}/sounds/blue",
        f"add-data {get_asset_path('sounds')/'brown'/'*'}{sep}{bundled_assets}/sounds/brown",
        f"add-data {get_asset_path('sounds')/'red'/'*'}{sep}{bundled_assets}/sounds/red",
        "hidden-import pynput.keyboard._xorg",
        "hidden-import pynput.mouse._xorg",
    ]

    command = f"{script} {' '.join(f'--{opt}' for opt in options)}"
    PyInstaller.__main__.run(command.split())


def get_executable_file_name(app_name: str):
    os_name = os.getenv("OS_NAME")
    if os_name is None:
        if is_linux():
            os_name = "linux"
        elif is_windows():
            os_name = "windows"
        elif is_macos():
            os_name = "macos"
        else:
            raise NotImplementedError
    return f"{app_name}-{os_name}"


if __name__ == "__main__":
    build()
