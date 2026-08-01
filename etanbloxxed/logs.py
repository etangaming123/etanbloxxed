"""Finding and tailing Roblox's log files."""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Iterator

from .constants import MAC_LOG_DIR, WINDOWS_LOG_DIR, WINDOWS_ROBLOX_VERSIONS_DIR


def default_log_directory(is_windows: bool) -> Path:
    if is_windows:
        return Path(os.path.expandvars(WINDOWS_LOG_DIR))
    return Path(os.path.expanduser(MAC_LOG_DIR))


def default_roblox_versions_directory() -> Path:
    return Path(os.path.expandvars(WINDOWS_ROBLOX_VERSIONS_DIR))


def find_latest_log_file(directory: Path) -> Path:
    directory = Path(directory)
    candidates = [f for f in directory.iterdir() if f.is_file() and "Player" in f.name]
    if not candidates:
        raise FileNotFoundError(f"No Roblox player log files found in {directory}")
    return max(candidates, key=lambda f: f.stat().st_mtime)


def find_latest_modified_directory(folder_path: Path) -> Path:
    folder_path = Path(folder_path)
    subdirectories = [d for d in folder_path.iterdir() if d.is_dir()]
    if not subdirectories:
        raise FileNotFoundError(f"No subdirectories found in {folder_path}")
    return max(subdirectories, key=lambda d: d.stat().st_mtime)


def follow(file) -> Iterator[str]:
    """Yield new lines appended to `file` as they're written, like `tail -f`."""
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
