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


import re


__all__ = []


def signature(s):
    def decorator(func):
        _s = "%s(%s)" % (func.__name__, s)
        doc = getattr(func, '__doc__', "")
        if not doc:
            doc = _s
        else:
            doc = _s + "\n" + doc
        func.__doc__ = doc
        return func
    return decorator


def process_global_docs(dct):
    for v in dct.values():
        process_doc(v)


def process_doc(obj):
    if not hasattr(obj, '__doc__'):
        return
    doc = obj.__doc__
    if not doc:
        return
    replaces = {
        r"\[.+\]\n\n( )+": "",
        r"\| ": "",
    }
    for k, v in replaces.items():
        doc = re.sub(k, v, doc)
    try:
        obj.__doc__ = doc
    except AttributeError:
        pass