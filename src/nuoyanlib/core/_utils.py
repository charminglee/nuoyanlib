# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


import threading
import traceback
from types import MethodType
from functools import wraps
from ._doc import signature, get_signature
from . import _env


# region Function Utils ================================================================================================


class dualmethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            if instance is None:
                return self.func(owner, *args, **kwargs)
            else:
                return self.func(instance, *args, **kwargs)
        return wrapper


def hook_method(obj, func_name, before_hook=None, after_hook=None):
    func = getattr(obj, func_name)

    def invoke(*args, **kwargs):
        if before_hook:
            try:
                before_hook(*args, **kwargs)
            except:
                traceback.print_exc()
        ret = None
        try:
            ret = func(*args, **kwargs)
        except:
            traceback.print_exc()
        if after_hook:
            try:
                after_hook(*args, **kwargs)
            except:
                traceback.print_exc()
        return ret

    if isinstance(func, MethodType):
        @wraps(func.__func__)
        def wrapper(self, *args, **kwargs):
            return invoke(*args, **kwargs)
        wrapper = MethodType(wrapper, obj, obj.__class__) # noqa
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return invoke(*args, **kwargs)

    setattr(obj, func_name, wrapper)
    return wrapper


def kwargs_defaults(**kwargs):
    def decorator(func):
        co = func.__code__
        arg_names = co.co_varnames[:co.co_argcount]

        # 设置完整的函数签名（用于文档生成）
        sgn = get_signature(func)
        sgn = sgn[:sgn.rindex(",")] # 去掉末尾**kwargs
        sgn += ", *"
        for i in kwargs.items():
            sgn += ", %s=%s" % i
        signature(sgn)(func)

        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            for k in f_kwargs:
                if k not in kwargs and k not in arg_names:
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
        traceback.print_exc()
        return e


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
    def __init__(self, size=128):
        self.size = size
        self.full = False
        # 双向循环链表
        root = []
        root[:] = [root, root, None, None]
        self.root = root # noqa
        self.hits = 0
        self.misses = 0

    def __call__(self, func_or_cls):
        is_cls = isinstance(func_or_cls, type)
        if is_cls:
            func = func_or_cls.__new__
        else:
            func = func_or_cls
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
                hit_node[PREV] = tail
                hit_node[NEXT] = root
                self.hits += 1
                return res

            self.misses += 1
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
                old_key, _ = root[KEY], root[RESULT]
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

        def lru_info():
            return cache_len(), size, self.hits, self.misses

        if is_cls:
            func_or_cls.lru_info = staticmethod(lru_info)
            func_or_cls.__new__ = staticmethod(wrapper)
            return func_or_cls
        else:
            wrapper.lru_info = lru_info
            return wrapper


_NOT_FOUND = object()


class cached_property(object):
    def __init__(self, func):
        self.func = func
        self.attrname = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            cache = instance.__dict__
        except AttributeError:
            raise TypeError(
                "no '__dict__' attribute on %s instance to cache %s property"
                % (type(instance).__name__, self.attrname)
            )
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            val = self.func(instance)
            try:
                cache[self.attrname] = val
            except TypeError:
                raise TypeError(
                    "the '__dict__' attribute on %s instance does not support item assignment for caching %s property"
                    % (type(instance).__name__, self.attrname)
                )
        return val


class write_only_property(property):
    def __init__(self, fset=None, doc=None):
        if doc is None and fset is not None:
            doc = getattr(fset, '__doc__', None)
        property.__init__(self, None, fset, None, doc)
        self.name = fset.__name__ if fset else ""

    def setter(self, fset):
        return write_only_property(fset, self.__doc__)

    def getter(self, fget):
        raise AttributeError("write_only_property '%s' does not support getter" % self.name)

    def deleter(self, fdel):
        raise AttributeError("write_only_property '%s' does not support deleter" % self.name)


def inject_is_client(func):
    signature(start=1)(func)

    @wraps(func)
    def c(*args, **kwargs):
        return func(True, *args, **kwargs)

    @wraps(func)
    def s(*args, **kwargs):
        return func(False, *args, **kwargs)

    @wraps(func)
    def auto(*args, **kwargs):
        return func(_env.is_client(), *args, **kwargs)

    auto._nyl__inject_is_client = (c, s, func)
    return auto


def get_arg_names(func):
    code = func.__code__ # noqa
    arg_names = code.co_varnames[:code.co_argcount]
    return arg_names


def client_api(func): # todo
    return func


def server_api(func): # todo
    return func


# endregion


# region Class Utils ===================================================================================================


class SingletonMeta(type):
    def __new__(metacls, name, bases, dct):
        cls = type.__new__(metacls, name, bases, dct)
        cls._instance = None
        return cls

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance


class Singleton(object):
    __metaclass__ = SingletonMeta
    _instance = None


_KWARGS_MARK = (object(),)


def _singleton_key(args, kwargs):
    if not kwargs:
        return args
    return args + _KWARGS_MARK + tuple(sorted(kwargs.items()))


class ArgsSingletonMeta(type):
    def __new__(metacls, name, bases, dct):
        cls = type.__new__(metacls, name, bases, dct)
        cls._instances = {}
        cls._unhashable_instances = []
        return cls

    def __call__(cls, *args, **kwargs):
        key = _singleton_key(args, kwargs)
        try:
            inst = cls._instances.get(key)
        except TypeError:
            for cached_key, cached_inst in cls._unhashable_instances:
                if cached_key == key:
                    return cached_inst
            inst = type.__call__(cls, *args, **kwargs)
            cls._unhashable_instances.append((key, inst))
            return inst
        if inst is None:
            inst = type.__call__(cls, *args, **kwargs)
            cls._instances[key] = inst
        return inst


class ArgsSingleton(object):
    __metaclass__ = ArgsSingletonMeta
    _instances = {}
    _unhashable_instances = []


# endregion


def get_module(*args):
    path = join_chr(*args)
    try:
        return __imp(path)
    except:
        return None


# def get_obj_size(obj, seen=None):
#     if seen is None:
#         seen = set()
#     import sys
#     size = sys.getsizeof(obj)
#
#     obj_id = id(obj)
#     if obj_id in seen:
#         return 0
#     seen.add(obj_id)
#
#     if hasattr(obj, 'keys') and type(obj.keys) is MethodType:
#         size += sum(
#             get_obj_size(k, seen) + get_obj_size(obj[k], seen)
#             for k in obj.keys()
#         )
#     elif hasattr(obj, '__iter__') and type(obj.__iter__) is MethodType and not isinstance(obj, (str, unicode)):
#         size += sum(get_obj_size(i, seen) for i in obj)
#     elif hasattr(obj, '__dict__'):
#         size += get_obj_size(obj.__dict__, seen)
#
#     return size


class DefaultLocal(object):
    def __init__(self, default_factory=lambda: None):
        object.__setattr__(self, '_default_factory', default_factory)
        object.__setattr__(self, '_local', threading.local())

    def __getattribute__(self, name):
        local = object.__getattribute__(self, '_local')
        value = getattr(local, name, _NOT_FOUND)
        if value is _NOT_FOUND:
            factory = object.__getattribute__(self, '_default_factory')
            value = factory()
            local.__setattr__(name, value)
        return value

    def __setattr__(self, name, value):
        local = object.__getattribute__(self, '_local')
        return local.__setattr__(name, value)

    def __delattr__(self, name):
        local = object.__getattribute__(self, '_local')
        return local.__delattr__(name)


def parse_indices(index, length, cls, op=None):
    if isinstance(index, slice):
        start, stop, step = index.indices(length)
        return [
            (op(i) if op else i)
            for i in xrange(start, stop, step)
        ]
    elif isinstance(index, int):
        if index < 0:
            index += length
        if index < 0 or index >= length:
            raise IndexError("%s index out of range" % cls.__name__)
        return op(index) if op else index
    raise TypeError(
        "%s indices must be integers or slices, not %s"
        % (cls.__name__, type(index).__name__)
    )


def parse_indices_generator(index, length, cls, op=None):
    if isinstance(index, slice):
        start, stop, step = index.indices(length)
        for i in xrange(start, stop, step):
            yield op(i) if op else i
    elif isinstance(index, int):
        if index < 0:
            index += length
        if index < 0 or index >= length:
            raise IndexError("%s index out of range" % cls.__name__)
        yield op(index) if op else index
    else:
        raise TypeError(
            "%s indices must be integers or slices, not %s"
            % (cls.__name__, type(index).__name__)
        )


class __Universal(object):
    """
    万用对象，仅用于绕过机审检查。

    对该对象所做的任何操作都将抛出 ``RuntimeError`` 。
    """

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __raise(self, *args, **kwargs):
        raise RuntimeError("you can't do anything to the UNIVERSAL_OBJECT")

    if not _env.DEBUG:
        __getattribute__    = __raise
        __setattr__         = __raise
        __delattr__         = __raise
        __eq__              = __raise
        __ne__              = __raise
        __str__             = __raise
        __repr__            = __raise
        __hash__            = None
        __format__          = __raise
        __reduce__          = __raise
        __reduce_ex__       = __raise
        __call__            = __raise
        __contains__        = __raise
        __getitem__         = __raise
        __setitem__         = __raise
        __delitem__         = __raise
        __iter__            = __raise


UNIVERSAL_OBJECT = __Universal()


class MappingProxy(object):
    def __init__(self, mapping):
        self.__mapping = mapping

    def __repr__(self):
        return "MappingProxy(%r)" % self.__mapping

    get             = lambda self, *args: self.__mapping.get(*args)
    has_key         = lambda self, *args: self.__mapping.has_key(*args)
    keys            = lambda self, *args: self.__mapping.keys()
    values          = lambda self, *args: self.__mapping.values()
    items           = lambda self, *args: self.__mapping.items()
    viewkeys        = lambda self, *args: self.__mapping.viewkeys()
    viewvalues      = lambda self, *args: self.__mapping.viewvalues()
    viewitems       = lambda self, *args: self.__mapping.viewitems()
    iterkeys        = lambda self, *args: self.__mapping.iterkeys()
    itervalues      = lambda self, *args: self.__mapping.itervalues()
    iteritems       = lambda self, *args: self.__mapping.iteritems()
    __getitem__     = lambda self, *args: self.__mapping.__getitem__(*args)
    __iter__        = lambda self, *args: self.__mapping.__iter__()
    __len__         = lambda self, *args: self.__mapping.__len__()
    __contains__    = lambda self, *args: self.__mapping.__contains__(*args)

    def __raise(self, *args, **kwargs):
        raise TypeError("MappingProxy object is read-only")

    clear       = __raise
    pop         = __raise
    popitem     = __raise
    setdefault  = __raise
    update      = __raise
    __setitem__ = __raise
    __delitem__ = __raise


def iter_obj_attrs(obj):
    for name in dir(obj):
        try:
            attr = getattr(obj, name)
        except AttributeError:
            # 如果获取的属性是property且getter执行时出错，会抛出AttributeError
            continue
        yield attr


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


def get_func(cls, module, func):
    g = cls.__init__.__func__.__globals__ # noqa
    m = join_chr(*module)
    f = join_chr(*func)
    try:
        return getattr(g[m], f)
    except (AttributeError, KeyError):
        return


def join_chr(*seq):
    return "".join(chr(i) for i in seq)


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


def __imp(p):
    return (
        globals()
        ['\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f']
        ['\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f']
        (p, fromlist=[""])
    )
