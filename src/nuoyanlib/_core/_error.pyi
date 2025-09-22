# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-21
|
| ==============================================
"""


from typing import Tuple


class SystemNotFoundError(RuntimeError):
    ns: str
    sys_name: str
    def __init__(self: ..., ns: str, sys_name: str) -> None: ...
class NuoyanLibServerSystemRegisterError(RuntimeError):
    pass
class NuoyanLibClientSystemRegisterError(RuntimeError):
    pass
class PathMatchError(RuntimeError):
    pattern: str
    def __init__(self: ..., pattern: str) -> None: ...
class AcrossImportError(ImportError): ...
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
    def __init__(self: ..., name: str, is_client: bool) -> None: ...
