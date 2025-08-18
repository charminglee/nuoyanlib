# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-19
|
| ==============================================
"""


from typing import Any


def info(msg: str, *args: Any, show_env: bool = True) -> None: ...
def warning(msg: str, *args: Any, show_env: bool = True) -> None: ...
def error(msg: str, *args: Any, show_env: bool = True) -> None: ...
def debug(msg: str, *args: Any, show_env: bool = True) -> None: ...
def disable_modsdk_loggers() -> None: ...
