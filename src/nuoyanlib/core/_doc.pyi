# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


from typing import Any, Callable
from ._types._typing import _T


def signature(s: str) -> Callable[[_T], _T]: ...
def process_global_docs(dct: dict) -> None: ...
def process_doc(obj: Any) -> None: ...
