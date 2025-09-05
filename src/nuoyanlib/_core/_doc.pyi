# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-06
|
| ==============================================
"""


from typing import Any, Callable, TypeVar


_T = TypeVar("_T")


def signature(s: str) -> Callable[[_T], _T]: ...
def process_global_docs(dct: dict) -> None: ...
def process_doc(obj: Any) -> None: ...
