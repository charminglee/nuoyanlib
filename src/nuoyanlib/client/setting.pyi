# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-5
#  ⠀
#  ================================================


from typing import Any, overload
from ..core._types._typing import T


def save_setting(name: str, data: Any, is_global: bool = True) -> bool: ...
@overload
def read_setting(name: str, default: None = None, is_global: bool = True) -> Any: ...
@overload
def read_setting(name: str, default: T, is_global: bool = True) -> T: ...
