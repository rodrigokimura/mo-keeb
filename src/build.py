import os

import PyInstaller.__main__

from constants import APP_NAME
from utils import get_asset_path, get_commit_sha


def build():
    version_id = get_commit_sha()
    executable_name = get_executable_file_name(APP_NAME, version_id)
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
    ]

    command = f"{script} {' '.join(f'--{opt}' for opt in options)}"
    PyInstaller.__main__.run(command.split())


def get_executable_file_name(app_name: str, version_id: str):
    return app_name
    # name = f"{app_name}_{version_id}"
    # return name


if __name__ == "__main__":
    build()
