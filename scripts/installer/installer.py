# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


from functools import partial
import os
from pathlib import Path
import shutil
import sys
from typing import Iterable


PACKAGE_DIRECTORY_NAME = "nuoyanlib"
EXTENSIONS_DIRECTORY_NAME = "extensions"
IGNORED_DIRECTORY_NAMES = [
    "__pycache__"
]
IGNORED_FILE_SUFFIXES = [
    ".pyc"
]
SHOW_PROGRESS = False
COPY_BUFFER_SIZE = 1024 * 1024
PROGRESS_BAR_WIDTH = 30


def get_source_directory() -> Path:
    bundle_directory = getattr(sys, "_MEIPASS", None)
    if bundle_directory is not None:
        return Path(bundle_directory) / PACKAGE_DIRECTORY_NAME
    return Path(__file__).resolve().parents[2] / "src" / PACKAGE_DIRECTORY_NAME


SOURCE_DIRECTORY = get_source_directory()


def is_ignored_name(
    name: str,
    copy_pyi: bool = True,
    copy_extensions: bool = False,
) -> bool:
    suffix = Path(name).suffix.lower()
    return (
        name in IGNORED_DIRECTORY_NAMES
        or suffix in IGNORED_FILE_SUFFIXES
        or (not copy_pyi and suffix == ".pyi")
        or (not copy_extensions and name == EXTENSIONS_DIRECTORY_NAME)
    )


def ignore_files(
    path: str,
    names: Iterable[str],
    copy_pyi: bool = True,
    copy_extensions: bool = False,
) -> list[str]:
    return [
        name
        for name in names
        if is_ignored_name(name, copy_pyi, copy_extensions)
    ]


def calculate_total_size(
    source: Path,
    copy_pyi: bool = True,
    copy_extensions: bool = False,
) -> int:
    total_size = 0
    for root, directories, files in os.walk(source):
        root = Path(root)
        directories[:] = [
            name
            for name in directories
            if not is_ignored_name(name, copy_pyi, copy_extensions)
        ]
        for name in files:
            if not is_ignored_name(name, copy_pyi, copy_extensions):
                total_size += (root / name).stat().st_size
    return total_size


class CopyProgress:
    def __init__(self, total_size: int) -> None:
        self.total_size = total_size
        self.copied_size = 0

    def update(self, copied_size: int) -> None:
        self.copied_size += copied_size
        self.render()

    def render(self) -> None:
        if self.total_size:
            percentage = min(
                self.copied_size * 100.0 / self.total_size,
                100.0,
            )
        else:
            percentage = 100.0

        filled_width = int(PROGRESS_BAR_WIDTH * percentage / 100.0)
        if filled_width == PROGRESS_BAR_WIDTH:
            bar = "=" * PROGRESS_BAR_WIDTH
        else:
            bar = (
                "=" * filled_width
                + ">"
                + " " * (PROGRESS_BAR_WIDTH - filled_width - 1)
            )
        progress = "安装中: [{}] {:>3.0f}%".format(bar, percentage)
        sys.stdout.write("\r" + progress)
        sys.stdout.flush()

    def finish(self) -> None:
        self.copied_size = self.total_size
        self.render()
        sys.stdout.write("\n")
        sys.stdout.flush()

    def copy_file(self, source: str, target: str) -> Path:
        source_path = Path(source)
        target_path = Path(target)
        with source_path.open("rb") as source_file, target_path.open("wb") as target_file:
            while True:
                chunk = source_file.read(COPY_BUFFER_SIZE)
                if not chunk:
                    break
                target_file.write(chunk)
                self.update(len(chunk))
        shutil.copystat(source_path, target_path)
        return target_path


def install(
    destination: str,
    copy_pyi: bool = True,
    copy_extensions: bool = False,
) -> Path:
    destination = Path(destination)
    source = SOURCE_DIRECTORY.resolve()
    destination = destination.expanduser().resolve()
    target = destination / PACKAGE_DIRECTORY_NAME

    if not source.is_dir():
        raise FileNotFoundError("source directory does not exist: {}".format(source))
    if destination.exists() and not destination.is_dir():
        raise ValueError("destination is not a directory: {}".format(destination))
    if target == source or source in target.parents:
        raise ValueError("destination must not be inside the source directory")

    if SHOW_PROGRESS:
        total_size = calculate_total_size(source, copy_pyi, copy_extensions)
        progress = CopyProgress(total_size)
        copy_function = progress.copy_file
    else:
        progress = None
        copy_function = shutil.copy2
    try:
        if target.exists():
            if not target.is_dir():
                raise ValueError("target is not a directory: {}".format(target))
            shutil.rmtree(target)
        shutil.copytree(
            source,
            target,
            ignore=partial(
                ignore_files,
                copy_pyi=copy_pyi,
                copy_extensions=copy_extensions,
            ),
            copy_function=copy_function,
        )
    finally:
        if progress:
            progress.finish()
    return target
