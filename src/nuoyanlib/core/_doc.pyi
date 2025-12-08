# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-05
|
| ====================================================
"""


from typing import Any
from ._types._typing import FuncDecorator


def signature(s: str) -> FuncDecorator: ...
def process_global_docs(dct: dict) -> None: ...
def process_doc(obj: Any) -> None: ...
