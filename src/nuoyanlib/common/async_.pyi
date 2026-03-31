# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-3-25
#  ⠀
# =================================================


from typing import Callable, Generator


def _next(gen: Generator) -> None: ...
def async_(func: Callable) -> Callable: ...


class async_sleep(object):
    t: float
    def __init__(self, t: float) -> None: ...













