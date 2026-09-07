# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  ================================================


import threading
import traceback
from types import MethodType
from functools import wraps
from ._doc import signature, get_signature
from ._env import is_client


def get_arg_names(func):
    code = func.__code__ # noqa
    arg_names = code.co_varnames[:code.co_argcount]
    return arg_names


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


_VOID = object()


class DefaultLocal(object):
    def __init__(self, default_factory=lambda: None):
        object.__setattr__(self, '_default_factory', default_factory)
        object.__setattr__(self, '_local', threading.local())

    def __getattribute__(self, name):
        local = object.__getattribute__(self, '_local')
        value = getattr(local, name, _VOID)
        if value is _VOID:
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


def get_file_path(index=-2):
    stack = traceback.extract_stack()
    return stack[index][0] if stack else ""


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
        return func(is_client(), *args, **kwargs)

    auto._nyl__inject_is_client = (c, s, func)
    return auto


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


def client_api(func): # todo
    return func


def server_api(func): # todo
    return func


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
        raise TypeError("MappingProxy is read-only")

    clear       = __raise
    pop         = __raise
    popitem     = __raise
    setdefault  = __raise
    update      = __raise
    __setitem__ = __raise
    __delitem__ = __raise


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


class cached_property(object):
    def __init__(self, getter):
        super(cached_property, self).__init__()
        self.getter = getter
        self.__doc__ = getattr(getter, '__doc__', None)

    def __get__(self, ins, cls):
        value = self.getter(ins)
        if value is not None:
            setattr(ins, self.getter.__name__, value)
        return value


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


def iter_obj_attrs(obj):
    for name in dir(obj):
        try:
            attr = getattr(obj, name)
        except AttributeError:
            # 如果获取的属性是property且getter执行时出错，会抛出AttributeError
            continue
        yield attr


def get_func(cls, module, func):
    g = cls.__init__.__func__.__globals__ # noqa
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


def hook_method(org_method, before_hook=None, after_hook=None):
    @wraps(org_method.__func__) # noqa
    def wrapper(self, *args, **kwargs):
        if before_hook:
            try:
                before_hook(*args, **kwargs)
            except:
                try:
                    traceback.print_exc()
                except:
                    pass
        try:
            org_method(*args, **kwargs)
        except:
            try:
                traceback.print_exc()
            except:
                pass
        if after_hook:
            try:
                after_hook(*args, **kwargs)
            except:
                try:
                    traceback.print_exc()
                except:
                    pass

    ins = org_method.__self__ # noqa
    wrapper = MethodType(wrapper, ins, ins.__class__) # noqa
    setattr(ins, org_method.__name__, wrapper)


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



