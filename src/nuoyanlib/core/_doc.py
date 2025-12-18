# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


import re


def get_signature(func, start=0):
    s = ""
    code = func.__code__
    defs = func.__defaults__ or ()
    arg_names = code.co_varnames[:code.co_argcount]
    no_def_argcount = code.co_argcount - len(defs)

    for i, name in enumerate(arg_names):
        if i < start:
            continue
        if i < no_def_argcount:
            # 无默认值参数
            s += "%s, " % name
        else:
            # 带默认值参数
            s += "%s=%s, " % (name, defs[i - no_def_argcount])
    s = s[:-2]

    # 如果有*args
    if code.co_flags & 0x04:
        s += ", *args"
    # 如果有**kwargs
    if code.co_flags & 0x08:
        s += ", **kwargs"
    return s


def signature(s="", start=0):
    def decorator(func):
        _s = s if s else get_signature(func, start)
        _s = "%s(%s)" % (func.__name__, _s)

        doc = getattr(func, '__doc__', None)
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


if __name__ == "__main__":
    @signature(start=1)
    def f(_, a, b=3, c=4, *args, **kwargs):
        """
        114514。
        """
    print(f.__doc__)
