# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


class GetPropertyError(AttributeError):
    name: str
    def __init__(self: ..., name: str) -> None: ...
class ScreenNodeNotFoundError(RuntimeError): ...
class EventArgsError(AttributeError):
    name: str
    def __init__(self: ..., name: str) -> None: ...
class VectorError(Exception): ...
