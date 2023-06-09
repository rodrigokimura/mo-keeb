import os
import pathlib
import sys

import git


def is_windows():
    return sys.platform == "win21"


def is_linux():
    return sys.platform in ["linux", "linux2"]


def is_macos():
    return sys.platform == "darwin"


def get_asset_path(file_name: str):
    root = get_src()
    return root / "assets" / file_name


def get_sound_path_by_code_and_profile(code: str, profile: str):
    root = get_src()
    return root / "assets" / "sounds" / profile / f"{code}.wav"


def get_font_path_by_name(name: str):
    return get_asset_path(f"{name}.ttf")


def is_in_bunble():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_src():
    root = os.path.abspath(os.path.dirname(__file__))
    return pathlib.Path(root)


def get_commit_sha(short=True):
    repo = git.Repo(search_parent_directories=True)  # type: ignore
    sha = repo.head.commit.hexsha
    if short:
        short_sha = repo.git.rev_parse(sha, short=8)
        return str(short_sha)
    else:
        return sha


def get_version_info(app_name: str):
    root = get_src()
    for _, _, files in os.walk(root.parent / "dist"):
        for file in files:
            if app_name in file:
                sha = parse_executable_file_name(file)
                commit = get_commit_from_sha(sha)
                print(f"File: {file}")
                print(f"Version: {sha}")
                print(f"Date: {commit.authored_datetime}")
                print(f"Author: {commit.author}")


def parse_executable_file_name(file_name: str):
    short_commit_sha = file_name.split("_")[-1].split(".")[0]
    return short_commit_sha


def get_commit_from_sha(short_commit_sha: str):
    repo = git.Repo(search_parent_directories=True)  # type: ignore
    commit = repo.commit(short_commit_sha)
    return commit


def get_font(name: str):
    import pygame.freetype

    pygame.freetype.init()

    try:
        font = pygame.freetype.Font(get_font_path_by_name(name))
    except FileNotFoundError:
        font = pygame.freetype.SysFont(name, 10)
    return font


def backend_option_to_class(opt: str):
    from backends.keyboard import Keyboard
    from backends.pynput import Pynput
    from constants import BackendOption

    if opt == BackendOption.AUTO:
        backend = Keyboard if is_windows() else Pynput
    elif opt == BackendOption.KEYBOARD:
        backend = Keyboard
    elif opt == BackendOption.PYNPUT:
        backend = Pynput
    else:
        raise NotImplementedError
    return backend
