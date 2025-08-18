# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-18
|
| ==============================================
"""


def info(msg: str, show_env=True) -> None: ...
def warning(msg: str, show_env=True) -> None: ...
def error(msg: str, show_env=True) -> None: ...
def debug(msg: str, show_env=True) -> None: ...
def disable_modsdk_loggers() -> None: ...
