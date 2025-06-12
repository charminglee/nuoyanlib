# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from typing import Tuple


class NotInClientError(ImportError): ...
class NotInServerError(ImportError): ...
class GetPropertyError(AttributeError):
    name: str
    def __init__(self: ..., name: str) -> None: ...
class ScreenNodeNotFoundError(RuntimeError): ...
class EventParameterError(AttributeError):
    event_name: str
    param: str
    def __init__(self: ..., event_name: str, param: str) -> None: ...
class VectorError(Exception): ...
class EventSourceError(TypeError):
    args = Tuple[str, str, str]
    def __init__(self: ..., name: str, ns: str, sys_name: str) -> None: ...
class EventNotFoundError(AttributeError):
    name: str
    is_client: bool
    def __init__(self, name: str, is_client: bool) -> None: ...
