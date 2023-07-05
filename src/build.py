import os

import main
from utils import get_asset_path, is_windows


def build():
    script = main.__file__
    assets = get_asset_path("*")
    sep = ";" if is_windows() else ":"
    bundled_assets = "./assets"
    command = f"pipenv run pyinstaller {script} --onefile --noupx --add-data {assets}{sep}{bundled_assets}"
    os.popen(command).read()


if __name__ == "__main__":
    build()
