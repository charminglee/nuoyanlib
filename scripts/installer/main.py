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


import argparse
from pathlib import Path
import sys
from typing import Optional, Sequence

from installer import install
from ui import run_installer_ui


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="将「nuoyanlib」安装到指定目录"
    )
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        help="「nuoyanlib」的安装目录",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if args.destination is None:
        return run_installer_ui()

    target = install(args.destination)
    print("已将「nuoyanlib」安装到 {}".format(target))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
