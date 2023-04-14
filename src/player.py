import subprocess


def play(file: str):
    subprocess.Popen(
        f"mpg123 {file}".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
