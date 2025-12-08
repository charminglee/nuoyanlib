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


__all__ = [
    "SystemNotFoundError",
    "NuoyanLibServerSystemRegisterError",
    "NuoyanLibClientSystemRegisterError",
    "PathMatchError",
    "AcrossImportError",
    "GetPropertyError",
    "ScreenNodeNotFoundError",
    "EventParameterError",
    "VectorError",
    "ZeroVectorError",
    "VectorDimError",
    "EventSourceError",
    "EventNotFoundError",
]


class SystemNotFoundError(RuntimeError):
    def __init__(self, ns, sys_name):
        self.ns = ns
        self.sys_name = sys_name

    def __str__(self):
        return "namespace=%r, system_name=%r" % (self.ns, self.sys_name)


class NuoyanLibServerSystemRegisterError(RuntimeError):
    pass


class NuoyanLibClientSystemRegisterError(RuntimeError):
    pass


class PathMatchError(RuntimeError):
    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        return "control path %r not matched" % self.pattern


class AcrossImportError(ImportError):
    def __str__(self):
        from ._sys import is_client
        if is_client():
            return "cannot import 'nuoyanlib.server' in client environment"
        else:
            return "cannot import 'nuoyanlib.client' in server environment"


class GetPropertyError(AttributeError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "can't get property %r, it is write-only" % self.name


class ScreenNodeNotFoundError(RuntimeError):
    def __str__(self):
        return "can't find ScreenNode instance, check if your UI class inherits 'ScreenNode' or 'CustomUIScreenProxy'"


class EventParameterError(AttributeError):
    def __init__(self, event_name, param):
        self.event_name = event_name
        self.param = param

    def __str__(self):
        return "%s has no parameter %r" % (self.event_name, self.param)


class VectorError(Exception):
    pass


class ZeroVectorError(Exception):
    pass


class VectorDimError(Exception):
    pass


class EventSourceError(TypeError):
    def __init__(self, name, ns, sys_name):
        self.args = (name, ns, sys_name)

    def __str__(self):
        return "unknown event source (event_name=%r, ns=%r, sys_name=%r)" % self.args


class EventNotFoundError(AttributeError):
    def __init__(self, name, is_client):
        self.name = name
        self.is_client = is_client

    def __str__(self):
        if self.is_client:
            return "client event %r doesn't exist" % self.name
        else:
            return "server event %r doesn't exist" % self.name


if __name__ == "__main__":
    raise EventSourceError("TestEvent", "Test", "TestSystem")













