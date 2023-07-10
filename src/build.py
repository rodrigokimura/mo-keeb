import os

import PyInstaller.__main__

import main
from constants import APP_NAME
from utils import get_asset_path, get_commit_sha, is_windows


def build():
    check_build_deps()
    version_id = get_commit_sha()
    executable_name = get_executable_file_name(APP_NAME, version_id)
    script = main.__file__
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


def check_build_deps():
    if is_windows():
        import subprocess

        subprocess.run("pip install pywin32-ctypes")


def get_executable_file_name(app_name: str, version_id: str, extension=False):
    name = f"{app_name}_{version_id}"
    if extension:
        if is_windows():
            name += ".exe"
    return name


if __name__ == "__main__":
    build()
