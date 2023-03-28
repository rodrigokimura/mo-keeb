import subprocess


def play(file: str):
    # subprocess.Popen(f"nvlc {file}".split())
    subprocess.Popen(f"mpg123 {file}".split())
