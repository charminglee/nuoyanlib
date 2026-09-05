# -*- coding: utf-8 -*-
#  =================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  =================================================


from typing import Any


def info(msg: str, *args: Any, show_env: bool = False) -> None: ...
def warning(msg: str, *args: Any, show_env: bool = False) -> None: ...
def error(msg: str, *args: Any, show_env: bool = False) -> None: ...
def debug(msg: str, *args: Any, show_env: bool = False) -> None: ...
def disable_modsdk_loggers() -> None: ...