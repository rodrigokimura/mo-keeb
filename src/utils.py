import os
import pathlib
import sys

import git


def is_windows():
    return os.name == "nt"


def get_asset_path(file_name: str):
    root = get_src()
    return root / "assets" / file_name


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
