# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-03
|
| ====================================================
"""


from traceback import print_exc
from types import MethodType
from functools import wraps
from ._doc import signature
from ._types._checker import args_type_check


__all__ = []


_KWARGS_MARK = (object(),)


def _lru_key(args, kwargs):
    key = args
    if kwargs:
        # 位置参数与关键字参数之间需添加一个分隔符，否则下面这种情况会匹配到同一个key：
        # func(1, a=2)
        # func(1, (a, 2))
        key += _KWARGS_MARK
        for item in kwargs.items():
            key += item
    return key[0] if len(key) == 1 else key


class lru_cache(object):
    @args_type_check(int, is_method=True)
    def __init__(self, size=128):
        self.size = size
        self.full = False
        # 双向循环链表
        root = []
        root[:] = [root, root, None, None]
        self.root = root

    def __call__(self, func):
        size = self.size
        cache = {}
        cache_get = cache.get
        cache_len = cache.__len__
        # 链表节点的四个字段
        # root[PREV]即为最新节点（表尾），root[NEXT]即为最旧节点（表头）
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3

        def wrapper(*args, **kwargs):
            key = _lru_key(args, kwargs)
            hit_node = cache_get(key)
            root = self.root

            # 缓存命中
            if hit_node is not None:
                # 将命中节点移动到表尾
                hit_prev, hit_next, _, res = hit_node
                hit_prev[NEXT] = hit_next
                hit_next[PREV] = hit_prev
                tail = root[PREV]
                tail[NEXT] = root[PREV] = hit_node
                hit_prev[PREV] = tail
                hit_prev[NEXT] = root
                return res

            res = func(*args, **kwargs)
            # 某些情况下接口会异常返回None，因此不对None值进行缓存
            if res is None:
                return

            if self.full:
                # 将新数据填入根节点
                old_root = root
                old_root[KEY] = key
                old_root[RESULT] = res
                # 让最旧节点成为新的根节点
                root = self.root = old_root[NEXT]
                old_key, old_result = root[KEY], root[RESULT]
                # 清空最旧节点上的数据
                root[KEY] = root[RESULT] = None
                # 刷新缓存
                del cache[old_key]
                cache[key] = old_root
            else:
                # 创建新节点并插入到表尾
                tail = root[PREV]
                node = [tail, root, key, res]
                tail[NEXT] = root[PREV] = cache[key] = node
                self.full = (cache_len() >= size)

            return res

        return wrapper


def client_api(func):
    return func


def server_api(func):
    return func


def singleton(init_once=True):
    def decorator(cls):
        cls.__instance__ = None
        cls.__inited__ = False
        org_new = cls.__new__
        org_init = cls.__init__

        def new_new(*args, **kwargs):
            return cls.__instance__ or org_new(*args, **kwargs)

        def new_init(self, *args, **kwargs):
            if cls.__instance__ is None:
                cls.__instance__ = self
            # 如果init_once为True，则__init__方法只会被执行一次
            if not cls.__inited__ or not _init_once:
                org_init(self, *args, **kwargs)
                cls.__inited__ = True

        cls.__new__ = staticmethod(new_new)
        cls.__init__ = new_init
        return cls

    if isinstance(init_once, bool):
        _init_once = init_once
        return decorator
    else:
        _init_once = True
        return decorator(init_once)


class cached_property(object):
    def __init__(self, getter):
        self.getter = getter
        self.__doc__ = getattr(getter, '__doc__', "")

    def __get__(self, ins, cls):
        value = self.getter(ins)
        if value is not None:
            setattr(ins, self.getter.__name__, value)
        return value


def kwargs_setter(**kwargs):
    def decorator(func):
        co = func.__code__
        sgn = co.co_varnames[:co.co_argcount]

        # 设置完整的函数签名，用于文档生成
        sgn_str = ", ".join(sgn)
        sgn_str += ", *, "
        sgn_str += ", ".join("%s=%s" % i for i in kwargs.items())
        func = signature(sgn_str)(func)

        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            for k in f_kwargs:
                if k not in kwargs and k not in sgn:
                    raise TypeError(
                        "%s() got an unexpected keyword argument '%s'"
                        % (func.__name__, k)
                    )
            for k in kwargs:
                if k not in f_kwargs:
                    f_kwargs[k] = kwargs[k]
            return func(*f_args, **f_kwargs)
        return wrapper
    return decorator


def try_exec(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print_exc()
        return e


def iter_obj_attrs(obj):
    for name in dir(obj):
        try:
            attr = getattr(obj, name)
        except AttributeError:
            # 如果获取的属性是property且getter执行时出错，会抛出AttributeError
            continue
        yield attr


def get_func(cls, module, func):
    g = cls.__init__.__func__.__globals__ # NOQA
    m = join_chr(*module)
    f = join_chr(*func)
    try:
        return getattr(g[m], f)
    except (AttributeError, KeyError):
        return


def assert_error(func, args=(), kwargs=None, exc=()):
    if isinstance(exc, tuple):
        exc_names = "(%s)" % ", ".join(e.__name__ for e in exc)
    else:
        exc_names = exc.__name__
    try:
        if kwargs is None:
            kwargs = {}
        func(*args, **kwargs)
    except exc:
        assert True
    except Exception as e:
        assert False, "%s was raised, expected %s" % (e.__class__.__name__, exc_names)
    else:
        assert False, "no exception was raised, expected %s" % exc_names


def join_chr(*seq):
    return "".join(chr(i) for i in seq)


def hook_method(org_method, my_method):
    ins = org_method.__self__
    org_name = org_method.__name__
    @wraps(org_method.__func__)
    def wrapper(self, *args, **kwargs):
        # 如果my_method或try_exec对象被异常回收，直接执行会报错，导致原方法无法执行，因此增加判断
        if my_method and try_exec:
            try_exec(my_method, *args, **kwargs)
        org_method(*args, **kwargs)
    wrapper = MethodType(wrapper, ins)
    setattr(ins, org_name, wrapper)


# def is_inv36_key(k):
#     return k.endswith(_const.INV36)
#
#
# def is_inv27_key(k):
#     return k.endswith(_const.INV27)
#
#
# def is_shortcut_key(k):
#     return k.endswith(_const.SHORTCUT)
#
#
# def is_inv_key(k):
#     return is_inv36_key(k) or is_inv27_key(k) or is_shortcut_key(k)
#
#
# def is_not_inv_key(k):
#     return not is_inv_key(k)


def __test__():
    n = [0]
    @singleton(False)
    class A(object):
        def __init__(self):
            n[0] += 1
    a1 = A()
    a2 = A()
    assert a1 == a2
    assert n[0] == 2
    @singleton
    class A(object):
        def __init__(self):
            n[0] += 1
    A()
    A()
    assert n[0] == 3

    a = [0]
    class T(object):
        @cached_property
        def prop1(self):
            a[0] += 1
            return "a" + "b"
        @cached_property
        def prop2(self):
            a[0] += 1
            return "c" + "d"
    t = T()
    assert t.prop1 == "ab"
    assert t.prop1 == "ab"
    assert t.prop2 == "cd"
    assert t.prop2 == "cd"
    assert a[0] == 2

    @kwargs_setter(c=3, d=4)
    def func(a, b=2, **kwargs):
        return a, b, kwargs['c'], kwargs['d']
    assert func(1, 2) == (1, 2, 3, 4)
    assert func(1, 2, c=6) == (1, 2, 6, 4)
    assert func(1, b=5, c=6) == (1, 5, 6, 4)
    assert func(1, c=6) == (1, 2, 6, 4)
    assert func.__doc__ == "func(a, b, *, c=3, d=4)"
    assert_error(func, (1,), {'e': 1}, TypeError)









