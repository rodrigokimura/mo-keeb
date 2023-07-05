import os

import main
from settings import APP_NAME
from utils import get_asset_path


def build():
    executable_name = APP_NAME
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
    ]
    command = (
        f"pipenv run pyinstaller {script} {' '.join(f'--{opt}' for opt in options)}"
    )
    os.popen(command).read()


if __name__ == "__main__":
    build()
