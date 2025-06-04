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
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "can't get property '%s', it is write-only" % self.name


class ScreenNodeNotFoundError(RuntimeError):
    def __str__(self):
        return "can't find ScreenNode instance, check if your UI class inherits 'ScreenNode' or 'CustomUIScreenProxy'"


class EventArgsError(AttributeError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "event has no parameter '%s'" % self.name


class VectorError(Exception):
    pass


if __name__ == "__main__":
    raise ScreenNodeNotFoundError













