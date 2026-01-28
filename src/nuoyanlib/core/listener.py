# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-20
#  ⠀
# =================================================


if 0:
    from typing import Any


import bisect
from types import MethodType
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from . import _const, error, _sys
from ._utils import iter_obj_attrs, try_exec
from ..utils.enum import ClientEvent, ServerEvent


__all__ = [
    "ALL_CLIENT_LIB_EVENTS",
    "ALL_SERVER_LIB_EVENTS",
    "event",
    "listen_event",
    "unlisten_event",
    "listen_all_events",
    "unlisten_all_events",
    "is_listened",
    "EventArgsWrap",
    "BaseEventProxy",
    "ClientEventProxy",
    "ServerEventProxy",
]


ALL_CLIENT_LIB_EVENTS = {}
ALL_SERVER_LIB_EVENTS = {
    # 'ItemGridChangedServerEvent': _const.LIB_CLIENT_NAME,
    'UiInitFinished': _const.LIB_CLIENT_NAME,
}


class _EventPool(object):
    __slots__ = ('__name__', 'pool', 'priorities', 'lock', 'remove_lst', 'add_lst')

    def __init__(self, event_id):
        self.pool = {}
        self.priorities = []
        self.lock = False
        self.remove_lst = []
        self.add_lst = []
        self.__name__ = event_id

    def __bool__(self):
        return any(v for v in self.pool.values())

    __nonzero__ = __bool__

    def __call__(self, args=None):
        # 事件触发（modsdk调用入口）
        if args is None:
            args = {}

        # 加锁，防止在回调执行过程中再次监听/反监听了同一个事件，导致for循环抛出异常
        self.lock = True

        # 按优先级调用
        for p in self.priorities:
            for f in self.pool[p]:
                try_exec(f, args)
        self.lock = False

        while self.remove_lst:
            self._remove(*self.remove_lst.pop())
        while self.add_lst:
            self._add(*self.add_lst.pop())

    def _add(self, func, priority=0):
        p = -priority
        if p not in self.pool:
            self.pool[p] = set()
            # 插入优先级并排序
            bisect.insort(self.priorities, p)

        func_set = self.pool[p]
        if func in func_set:
            return
        if not self.lock:
            func_set.add(func)
        else:
            self.add_lst.append((func, priority))

    def _remove(self, func, priority=0):
        p = -priority
        if p not in self.pool:
            return
        func_set = self.pool[p]
        if func not in func_set:
            return
        if not self.lock:
            func_set.remove(func)
        else:
            self.remove_lst.append((func, priority))

    @staticmethod
    def _get(event_name, ns, sys_name, new=True):
        event_id = "%s_%s_%s" % (ns, sys_name, event_name)
        lib_sys = _sys.get_lib_system()
        if not lib_sys:
            return
        ep = getattr(lib_sys, event_id, None)
        if new and ep is None:
            ep = _EventPool(event_id)
            setattr(lib_sys, event_id, ep)
            # modsdk触发回调函数逻辑：getattr(lib_sys, ep.__name__)(args)
            lib_sys.ListenForEvent(ns, sys_name, event_name, lib_sys, ep)
        return ep

    @staticmethod
    def listen_event(func, event_name, ns, sys_name, priority=0):
        ep = _EventPool._get(event_name, ns, sys_name)
        ep._add(func, priority)

    @staticmethod
    def unlisten_event(func, event_name, ns, sys_name, priority=0):
        ep = _EventPool._get(event_name, ns, sys_name, False)
        if ep is None:
            return
        ep._remove(func, priority)

    @staticmethod
    def is_listened(func, event_name, ns, sys_name, priority=0):
        p = -priority
        ep = _EventPool._get(event_name, ns, sys_name, False)
        if ep is None or p not in ep.pool:
            return False
        return func in ep.pool[p]


def _get_event_source(is_client, event_name):
    if is_client:
        if event_name in ALL_CLIENT_LIB_EVENTS:
            return _const.LIB_NAME, ALL_CLIENT_LIB_EVENTS[event_name]
        elif event_name in ClientEvent:
            return c_api.GetEngineNamespace(), c_api.GetEngineSystemName()
    else:
        if event_name in ALL_SERVER_LIB_EVENTS:
            return _const.LIB_NAME, ALL_SERVER_LIB_EVENTS[event_name]
        elif event_name in ServerEvent:
            return s_api.GetEngineNamespace(), s_api.GetEngineSystemName()


def _parse_listen_args(func, event_name, ns, sys_name):
    if event_name and isinstance(event_name, str):
        event_name = event_name
    else:
        event_name = func.__name__
    if ns and sys_name:
        return event_name, ns, sys_name
    else:
        source = _get_event_source(_sys.is_client(), event_name)
        if source:
            return event_name, source[0], source[1]
        raise error.EventSourceError(event_name, ns, sys_name)


def event(event_name="", ns="", sys_name="", priority=0, is_method=True):
    """
    [装饰器]

    基于事件池机制的事件监听器，在高频监听/反监听场景下性能更好。

    说明
    ----

    适用于普通函数与实例方法，若用于普通函数，需将 ``is_method`` 参数设为 ``False`` 。
    事件名与函数名相同时，可省略 ``event_name`` 参数。监听 ModSDK 事件时，可省略 ``ns`` 和 ``sys_name`` 参数。

    在类中使用时，需在 ``__init__()`` 方法中调用一次 ``listen_all_events()`` 方可生效，详见示例。

    示例
    ----

    >>> import mod.client.extraClientApi as client_api
    >>> class MyClientSystem(client_api.GetClientSystemCls()):
    ...     def __init__(self, namespace, system_name):
    ...         super(MyClientSystem, self).__init__(namespace, system_name)
    ...         # 对当前类中所有被@event装饰的方法执行事件监听
    ...         nyl.listen_all_events(self)
    ...         # 调用以下函数可监听特定事件
    ...         # nyl.listen_event(self.MyCustomEvent)
    ...
    ...     # 监听MyCustomEvent事件，事件来源为MyMod:MyServerSystem
    ...     @nyl.event("MyCustomEvent", "MyMod", "MyServerSystem")
    ...     def EventCallback(self, args):
    ...         pass
    ...
    ...    # 事件名与函数名相同时，可省略event_name参数
    ...    @nyl.event(ns="MyMod", sys_name="MyServerSystem")
    ...    def MyCustomEvent(self, args):
    ...        pass
    ...
    ...     # 监听ModSDK事件且事件名与函数名相同时，可省略所有参数
    ...     @nyl.event
    ...     def UiInitFinished(self, args):
    ...         pass
    ...
    ...     def Destroy(self):
    ...         # 必要时，调用以下函数可取消当前类中所有被@event装饰的方法的事件监听
    ...         nyl.unlisten_all_events(self)
    ...         # 调用以下函数可取消监听特定事件
    ...         # nyl.unlisten_event(self.MyCustomEvent)
    ...

    对静态函数使用时，事件将被立即监听，无需手动调用 ``listen_all_events()`` 或 ``listen_event()``。

    >>> @nyl.event(ns="MyMod", sys_name="MyServerSystem", is_method=False)
    ... def MyCustomEvent(args):
    ...     pass
    ...

    -----

    :param str|function event_name: 事件名称；默认为被装饰函数名
    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool is_method: 被装饰函数是否是实例方法；默认为 True
    """
    def add_listener(func):
        # 解析事件参数
        args = _parse_listen_args(func, event_name, ns, sys_name)
        # 插入标记
        if not hasattr(func, '_nyl__listen_args'):
            func._nyl__listen_args = []
        func._nyl__listen_args.append((args[0], args[1], args[2], priority))
        # 非实例方法，立即执行监听
        if not is_method:
            _EventPool.listen_event(func, *args, priority=priority)
        return func
    # @event(...)
    if isinstance(event_name, str):
        return add_listener
    # @event
    else:
        return add_listener(event_name) # noqa


def _get_listen_args(func):
    if isinstance(func, MethodType):
        func = func.__func__
    return getattr(func, '_nyl__listen_args', None)


def listen_event(func, event_name="", ns="", sys_name="", priority=0, use_decorator=False):
    """
    基于事件池机制的事件监听，在高频监听/反监听场景下性能更好。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool use_decorator: 是否使用从 @event 装饰器传入的参数，设为 True 时，忽略 event_name、ns、sys_name 和 priority 参数；默认为 False

    :return: 无
    :rtype: None
    """
    if use_decorator:
        all_args = _get_listen_args(func)
        for args in all_args:
            _EventPool.listen_event(func, *args)
    else:
        args = _parse_listen_args(func, event_name, ns, sys_name)
        _EventPool.listen_event(func, *args, priority=priority)


def unlisten_event(func, event_name="", ns="", sys_name="", priority=0, use_decorator=False):
    """
    反监听通过 ``listen_event()`` 监听的事件。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool use_decorator: 是否使用从 @event 装饰器传入的参数，设为 True 时，忽略 event_name、ns、sys_name 和 priority 参数；默认为 False

    :return: 无
    :rtype: None
    """
    if use_decorator:
        all_args = _get_listen_args(func)
        for args in all_args:
            _EventPool.unlisten_event(func, *args)
    else:
        args = _parse_listen_args(func, event_name, ns, sys_name)
        _EventPool.unlisten_event(func, *args, priority=priority)


def _iter_all_events(ins):
    for attr in iter_obj_attrs(ins):
        args = _get_listen_args(attr)
        if args:
            yield attr, args


def listen_all_events(ins):
    """
    对实例中所有被 ``@event`` 装饰的方法进行事件监听。

    说明
    ----

    基于事件池机制，在高频监听/反监听场景下性能更好。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, all_args in _iter_all_events(ins):
        for args in all_args:
            _EventPool.listen_event(method, *args)


def unlisten_all_events(ins):
    """
    反监听实例中所有被 ``@event`` 装饰的方法的事件监听。

    说明
    ----

    基于事件池机制，在高频监听/反监听场景下性能较好。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, all_args in _iter_all_events(ins):
        for args in all_args:
            _EventPool.unlisten_event(method, *args)


def is_listened(func, event_name="", ns="", sys_name="", priority=0):
    """
    判断函数是否已监听某事件。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0

    :return: 已监听返回 True，否则返回 False
    :rtype: bool
    """
    args = _parse_listen_args(func, event_name, ns, sys_name)
    return _EventPool.is_listened(func, *args, priority=priority)


class EventArgsWrap(object):
    __slots__ = ('_arg_dict', '_event_name')

    def __init__(self, arg_dict, event_name):
        self._arg_dict = arg_dict
        self._event_name = event_name

    def __getattr__(self, key):
        # 事件参数获取
        if key in self._arg_dict:
            return self._arg_dict[key]
        raise error.EventParameterError(self._event_name, key)

    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key in EventArgsWrap.__slots__:
            object.__setattr__(self, key, value)
            return
        # 事件参数修改
        if key in self._arg_dict:
            self._arg_dict[key] = value
        else:
            raise error.EventParameterError(self._event_name, key)

    __setitem__ = __setattr__

    def __repr__(self):
        s = "<EventArgsWrap of '%s':" % self._event_name
        for k, v in self._arg_dict.items():
            s += "\n    .%s = %s" % (k, repr(v))
        s += "\n>"
        return s

    __iter__        = lambda self, *args: self._arg_dict.__iter__()
    __eq__          = lambda self, *args: self._arg_dict.__eq__(*args)
    __ne__          = lambda self, *args: self._arg_dict.__ne__(*args)
    __len__         = lambda self, *args: self._arg_dict.__len__()
    __contains__    = lambda self, *args: self._arg_dict.__contains__(*args)
    keys            = lambda self, *args: self._arg_dict.keys()
    values          = lambda self, *args: self._arg_dict.values()
    items           = lambda self, *args: self._arg_dict.items()
    iterkeys        = lambda self, *args: self._arg_dict.iterkeys()
    itervalues      = lambda self, *args: self._arg_dict.itervalues()
    iteritems       = lambda self, *args: self._arg_dict.iteritems()
    get             = lambda self, *args: self._arg_dict.get(*args)
    copy            = lambda self, *args: self._arg_dict.copy()


class BaseEventProxy(object):
    def __init__(self, *args, **kwargs):
        super(BaseEventProxy, self).__init__(*args, **kwargs)
        is_client = isinstance(self, ClientEventProxy)
        for attr in iter_obj_attrs(self):
            if not isinstance(attr, MethodType) or hasattr(attr, '_nyl__listen_args'):
                # 跳过属性和已被@event装饰的方法
                continue
            event_name = attr.__name__
            source = _get_event_source(is_client, event_name)
            if source:
                self._create_proxy(attr, event_name, *source)
        listen_all_events(self)

    def _create_proxy(self, method, event_name, ns, sys_name):
        @event(event_name, ns, sys_name)
        def proxy(args):
            method(EventArgsWrap(args, event_name) if args else None)
        name = "_nyl__proxy_" + event_name
        proxy.__name__ = name
        setattr(self, name, proxy)


class ClientEventProxy(BaseEventProxy):
    """
    客户端事件代理类。

    继承 ``ClientEventProxy`` 后，所有 ModSDK 客户端事件无需监听，编写一个与事件同名的方法即可使用，
    且事件参数采用对象形式，支持参数名补全。

    对于使用 ``@event`` 装饰器监听事件，无需在 ``__init__()`` 方法手动调用 ``listen_all_events()``。
    """


class ServerEventProxy(BaseEventProxy):
    """
    服务端事件代理类。

    继承 ``ServerEventProxy`` 后，所有 ModSDK 服务端事件无需监听，编写一个与事件同名的方法即可使用，
    且事件参数采用对象形式，支持参数名补全。

    对于使用 ``@event`` 装饰器监听事件，无需在 ``__init__()`` 方法手动调用 ``listen_all_events()``。
    """


def _lib_sys_event(name="", from_client=None):
    if from_client is None:
        from_client = not _sys.is_client()
    return event(
        name,
        _const.LIB_NAME,
        _const.LIB_CLIENT_NAME if from_client else _const.LIB_SERVER_NAME,
    )


def __test__():
    a = {
        'playerId': "-114514",
        'pos': (1, 1, 1),
        'itemDict': {'newItemName': "minecraft:apple", 'newAuxValue': 0, 'count': 1},
    }
    def CustomEvent(event):
        # print(event)
        assert event.playerId == a['playerId']
        assert event.pos == a['pos']
        assert event.get('itemDict') == a['itemDict']
        assert 'playerId' in event
        for k in event:
            assert event[k] == a[k]
        assert event == a
        assert len(event) == 3
        assert event.keys() == a.keys()
        assert event.values() == a.values()
        assert event.items() == a.items()
        event.playerId = "1919810"
        assert event.playerId == a['playerId'] == "1919810"
    CustomEvent(EventArgsWrap(a, "CustomEvent"))

    from ._utils import assert_error
    def f():
        @event("xxx", is_method=False)
        def cb(args):
            pass
    assert_error(f, exc=error.EventSourceError)
    def f():
        @event(is_method=False)
        def cb(args):
            pass
    assert_error(f, exc=error.EventSourceError)
    def f():
        @event(sys_name="system", is_method=False)
        def cb(args):
            pass
    assert_error(f, exc=error.EventSourceError)

    lib_sys = _sys.get_lib_system()
    def call(ns, sys_name, event_name, args):
        # 模拟引擎触发回调函数
        func = getattr(lib_sys, "_".join([ns, sys_name, event_name]))
        func(args)

    a = {'arg': 1}
    @event(is_method=False)
    @event(ns="abc", sys_name="system", is_method=False)
    @event("LoadClientAddonScriptsAfter", is_method=False)
    @event("event", "mihoyo", "StarRail", 6, is_method=False)
    def LoadClientAddonScriptsAfter(args):
        assert args is a
    call("Minecraft", "Engine", "LoadClientAddonScriptsAfter", a)
    LoadClientAddonScriptsAfter(a)
    assert LoadClientAddonScriptsAfter.__name__ == "LoadClientAddonScriptsAfter"
    assert LoadClientAddonScriptsAfter._nyl__listen_args == [
        ("event", "mihoyo", "StarRail", 6),
        ("LoadClientAddonScriptsAfter", "Minecraft", "Engine", 0),
        ("LoadClientAddonScriptsAfter", "abc", "system", 0),
        ("LoadClientAddonScriptsAfter", "Minecraft", "Engine", 0),
    ]
    unlisten_event(LoadClientAddonScriptsAfter, use_decorator=True)
    assert not getattr(lib_sys, "Minecraft_Engine_LoadClientAddonScriptsAfter")
    assert not getattr(lib_sys, "abc_system_LoadClientAddonScriptsAfter")
    assert not getattr(lib_sys, "mihoyo_StarRail_event")

    n = [0]
    class T(object):
        def __init__(self):
            listen_all_events(self)
        @event("LoadClientAddonScriptsAfter")
        @event(ns="a", sys_name="b")
        def CustomEvent(self, args):
            assert self is args[n[0]]
            n[0] += 1
    t = T()
    t2 = T()
    tl = [t, t2]
    assert t.CustomEvent._nyl__listen_args == [
        ("CustomEvent", "a", "b", 0),
        ("LoadClientAddonScriptsAfter", "Minecraft", "Engine", 0),
    ]
    assert t.CustomEvent.__name__ == "CustomEvent"
    n = [0]
    t.CustomEvent(tl)
    t2.CustomEvent(tl)
    unlisten_all_events(t)
    unlisten_event(t2.CustomEvent, use_decorator=True)
    assert not getattr(lib_sys, "a_b_CustomEvent")
    assert not getattr(lib_sys, "Minecraft_Engine_LoadClientAddonScriptsAfter")


def __benchmark__(n, timer, **kwargs):
    class C(ServerEventProxy, s_api.GetServerSystemCls()):
        def __init__(self, namespace, system_name):
            super(C, self).__init__(namespace, system_name)
            listen_event(self.OnMobHitBlockServerEvent)
            ep = _EventPool._get("OnMobHitBlockServerEvent", "Minecraft", "Engine")

            timer.start("nuoyanlib listen")
            for _ in xrange(n):
                listen_event(self.OnMobHitBlockServerEvent)
            timer.end("nuoyanlib listen")

            timer.start("nuoyanlib unlisten")
            for _ in xrange(n):
                unlisten_event(self.OnMobHitBlockServerEvent)
            timer.end("nuoyanlib unlisten")

            timer.start("modsdk listen")
            for _ in xrange(n):
                self.ListenForEvent("Minecraft", "Engine", "OnMobHitBlockServerEvent", self, self.OnMobHitBlockServerEvent) # noqa
            timer.end("modsdk listen")

            timer.start("modsdk unlisten")
            for _ in xrange(n):
                self.UnListenForEvent("Minecraft", "Engine", "OnMobHitBlockServerEvent", self, self.OnMobHitBlockServerEvent) # noqa
            timer.end("modsdk unlisten")

            timer.start("event call")
            for _ in xrange(n):
                ep({})
            timer.end("event call")

            timer.start("common call")
            for _ in xrange(n):
                self.OnMobHitBlockServerEvent({}) # noqa
            timer.end("common call")

        @event
        def OnMobHitBlockServerEvent(self, args):
            pass

    C("", "")










