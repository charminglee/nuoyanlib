# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-29
|
| ==============================================
"""


from collections import defaultdict
from types import MethodType
import mod.client.extraClientApi as client_api
import mod.server.extraServerApi as server_api
from . import _const, _error
from ._sys import get_lib_system, is_client
from ._types._events import (
    ALL_CLIENT_ENGINE_EVENTS,
    ALL_CLIENT_LIB_EVENTS,
    ALL_SERVER_ENGINE_EVENTS,
    ALL_SERVER_LIB_EVENTS,
)
from ._utils import iter_obj_attrs


__all__ = [
    "event",
    "listen_event",
    "unlisten_event",
    "listen_all_events",
    "unlisten_all_events",
    "EventArgsProxy",
    "ClientEventProxy",
    "ServerEventProxy",
]


class _EventPool(object):
    __slots__ = ("pool", "priorities", "__name__")

    def __init__(self):
        self.pool = defaultdict(list)
        self.priorities = []

    def __nonzero__(self): # __bool__
        return any(l for l in self.pool.values())

    def __call__(self, args=None):
        # 事件触发（modsdk调用入口）
        if args is None:
            args = {}
        for p in self.priorities:
            for f in self.pool[p]:
                f(args)

    def add(self, func, priority=0):
        func_lst = self.pool[priority]
        if func in func_lst:
            return
        func_lst.append(func)
        if priority not in self.priorities:
            self.priorities.append(priority)
            self.priorities.sort(reverse=True)

    def remove(self, func, priority=0):
        if priority not in self.pool:
            return
        if func in self.pool[priority]:
            self.pool[priority].remove(func)

    @classmethod
    def get(cls, ns, sys_name, event_name):
        event_id = ":".join([ns, sys_name, event_name])
        lib_sys = get_lib_system()
        ep = getattr(lib_sys, event_id, None)
        if ep is None:
            ep = cls()
            ep.__name__ = event_id
            setattr(lib_sys, event_id, ep)
            # modsdk触发回调函数逻辑：getattr(lib_sys, ep.__name__)(args)
            lib_sys.ListenForEvent(ns, sys_name, event_name, lib_sys, ep)
        return ep

    @classmethod
    def listen_for(cls, ns, sys_name, event_name, func, priority=0):
        ep = cls.get(ns, sys_name, event_name)
        ep.add(func, priority)

    @classmethod
    def unlisten_for(cls, ns, sys_name, event_name, func, priority=0):
        ep = cls.get(ns, sys_name, event_name)
        ep.remove(func, priority)


def _get_event_source(client, event_name, ns="", sys_name=""):
    if ns and sys_name:
        return ns, sys_name
    if client:
        if event_name in ALL_CLIENT_ENGINE_EVENTS:
            return client_api.GetEngineNamespace(), client_api.GetEngineSystemName()
        elif event_name in ALL_CLIENT_LIB_EVENTS:
            return _const.LIB_NAME, ALL_CLIENT_LIB_EVENTS[event_name]
    else:
        if event_name in ALL_SERVER_ENGINE_EVENTS:
            return server_api.GetEngineNamespace(), server_api.GetEngineSystemName()
        elif event_name in ALL_SERVER_LIB_EVENTS:
            return _const.LIB_NAME, ALL_SERVER_LIB_EVENTS[event_name]


def event(event_name="", ns="", sys_name="", priority=0, is_method=True):
    """
    [装饰器]

    | 事件监听器，适用于静态函数与方法，若用于静态函数，请将 ``is_method`` 参数设为 ``False`` 。
    | 事件名与函数名相同时，可省略 ``event_name`` 参数。监听ModSDK事件时，可省略 ``ns`` 和 ``sys_name`` 参数。
    | 注意：在类中使用时，需要在 ``.__init__()`` 方法中调用一下 ``listen_all_events()`` ，详见示例。
    | 支持嵌套使用 ``@event`` ，但相同参数的事件只会被监听一次。

    -----

    【示例】

    ::

        import mod.client.extraClientApi as client_api
        import <scripts_root>.nuoyanlib.client as nyl

        class MyClientSystem(client_api.GetClientSystemCls()):
            def __init__(self, namespace, system_name):
                # 对当前类中所有被@event装饰的方法执行事件监听
                nyl.listen_all_events(self)

            def Destroy(self):
                # 必要时，对当前类中所有被@event装饰的方法执行事件反监听
                nyl.unlisten_all_events(self)

            # 监听MyCustomEvent事件，事件来源为MyMod:MyServerSystem
            @nyl.event("MyCustomEvent", "MyMod", "MyServerSystem")
            def EventCallback(self, args):
                ...

            # 事件名与函数名相同时，可省略event_name参数
            @nyl.event(ns="MyMod", sys_name="MyServerSystem")
            def MyCustomEvent(self, args):
                ...

            # 监听ModSDK事件且事件名与函数名相同时，可省略所有参数
            @nyl.event
            def UiInitFinished(self, args):
                ...

            def unlisten_MyCustomEvent(self):
                # 反监听特定事件
                nyl.unlisten_event(self.MyCustomEvent)

    | 对静态函数使用时，事件将被立即监听，无需手动调用 ``listen_all_events()`` 。

    ::

        @nyl.event(ns="MyMod", sys_name="MyServerSystem", is_method=False)
        def MyCustomEvent(args):
            ...

    -----

    :param str event_name: 事件名称，默认为被装饰函数名
    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param int priority: 优先级，默认为0，值越大优先级越高
    :param bool is_method: 回调函数是否是实例方法，默认为True

    :return: 返回原函数
    :rtype: function
    """
    def add_listener(func):
        # 解析事件参数
        if event_name and isinstance(event_name, str):
            _event_name = event_name
        else:
            _event_name = func.__name__
        if not ns or not sys_name:
            source = _get_event_source(is_client(), _event_name, ns, sys_name)
            if not source:
                raise _error.EventSourceError(_event_name, ns, sys_name)
            _ns, _sys_name = source
        else:
            _ns, _sys_name = ns, sys_name
        args = (_ns, _sys_name, _event_name, priority)
        # 插入标记
        if not hasattr(func, '_nyl_listen_args'):
            func._nyl_listen_args = []
        func._nyl_listen_args.append(args)
        # 非实例方法，立即执行监听
        if not is_method:
            _EventPool.listen_for(_ns, _sys_name, _event_name, func, priority)
        return func
    # @event(...)
    if isinstance(event_name, str):
        return add_listener
    # @event
    else:
        return add_listener(event_name)


def _get_event_args(func):
    if isinstance(func, MethodType):
        func = func.__func__
    args = getattr(func, '_nyl_listen_args', [])
    return args


def listen_event(func, ns="", sys_name="", event_name="", priority=0):
    """
    | 基于事件池机制的事件监听，在高频监听/反监听场景下性能较好。
    | 若函数已被 ``@event`` 装饰，可省略 ``ns``、``sys_name``、``event_name`` 和 ``priority`` 参数。

    -----

    :param function func: 事件回调函数
    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param str event_name: 事件名称
    :param int priority: 优先级，值越大优先级越高

    :return: 无
    :rtype: None
    """
    if ns:
        _EventPool.listen_for(ns, sys_name, event_name, func, priority)
    else:
        for a in _get_event_args(func):
            _EventPool.listen_for(a[0], a[1], a[2], func, a[3])


def unlisten_event(func, ns="", sys_name="", event_name="", priority=0):
    """
    | 取消事件监听。
    | 基于事件池机制，在高频监听/反监听场景下性能较好。
    | 若函数已被 ``@event`` 装饰，可省略 ``ns``、``sys_name``、``event_name`` 和 ``priority`` 参数。

    -----

    :param function func: 事件回调函数
    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param str event_name: 事件名称
    :param int priority: 优先级，值越大优先级越高

    :return: 无
    :rtype: None
    """
    if ns:
        _EventPool.listen_for(ns, sys_name, event_name, func, priority)
    else:
        for a in _get_event_args(func):
            _EventPool.unlisten_for(a[0], a[1], a[2], func, a[3])


def _get_all_event_args(ins):
    for attr in iter_obj_attrs(ins):
        args = _get_event_args(attr)
        if args:
            yield attr, args


def listen_all_events(ins):
    """
    | 对实例中所有被 ``@event`` 装饰的方法设置事件监听。
    | 基于事件池机制，在高频监听/反监听场景下性能较好。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, args in _get_all_event_args(ins):
        for a in args:
            _EventPool.listen_for(a[0], a[1], a[2], method, a[3])


def unlisten_all_events(ins):
    """
    | 取消实例中所有被 ``@event`` 装饰的方法的事件监听。
    | 基于事件池机制，在高频监听/反监听场景下性能较好。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, args in _get_all_event_args(ins):
        for a in args:
            _EventPool.unlisten_for(a[0], a[1], a[2], method, a[3])


class EventArgsProxy(object):
    __slots__ = ("_arg_dict", "_event_name")

    def __init__(self, arg_dict, event_name):
        self._arg_dict = arg_dict
        self._event_name = event_name

    def __getattr__(self, key):
        if key in self._arg_dict:
            return self._arg_dict[key]
        raise _error.EventParameterError(self._event_name, key)

    def __setattr__(self, key, value):
        if key in EventArgsProxy.__slots__:
            object.__setattr__(self, key, value)
            return
        # 事件参数修改
        if key in self._arg_dict:
            self._arg_dict[key] = value
        else:
            raise _error.EventParameterError(self._event_name, key)

    def __repr__(self):
        s = "<EventArgsProxy of '%s':" % self._event_name
        for k, v in self._arg_dict.items():
            s += "\n  .%s = %s" % (k, repr(v))
        s += "\n>"
        return s

    get          = lambda self, *a: self._arg_dict.get(*a)
    keys         = lambda self, *a: self._arg_dict.keys(*a)
    values       = lambda self, *a: self._arg_dict.values(*a)
    items        = lambda self, *a: self._arg_dict.items(*a)
    has_key      = lambda self, *a: self._arg_dict.has_key(a*a)
    copy         = lambda self, *a: self._arg_dict.copy(*a)
    iterkeys     = lambda self, *a: self._arg_dict.iterkeys(*a)
    itervalues   = lambda self, *a: self._arg_dict.itervalues(*a)
    iteritems    = lambda self, *a: self._arg_dict.iteritems(*a)
    viewkeys     = lambda self, *a: self._arg_dict.viewkeys(*a)
    viewvalues   = lambda self, *a: self._arg_dict.viewvalues(*a)
    viewitems    = lambda self, *a: self._arg_dict.viewitems(*a)
    __len__      = lambda self, *a: self._arg_dict.__len__(*a)
    __contains__ = lambda self, *a: self._arg_dict.__contains__(*a)
    __getitem__  = lambda self, *a: self._arg_dict.__getitem__(*a)
    __setitem__  = lambda self, *a: self._arg_dict.__setitem__(*a)
    __cmp__      = lambda self, *a: self._arg_dict.__cmp__(*a)
    __eq__       = lambda self, *a: self._arg_dict.__eq__(*a)
    __ge__       = lambda self, *a: self._arg_dict.__ge__(*a)
    __gt__       = lambda self, *a: self._arg_dict.__gt__(*a)
    __iter__     = lambda self, *a: self._arg_dict.__iter__(*a)
    __le__       = lambda self, *a: self._arg_dict.__le__(*a)
    __lt__       = lambda self, *a: self._arg_dict.__lt__(*a)
    __ne__       = lambda self, *a: self._arg_dict.__ne__(*a)


class _BaseEventProxy(object):
    def __init__(self, *args, **kwargs):
        super(_BaseEventProxy, self).__init__(*args, **kwargs)
        self._process_engine_events()
        listen_all_events(self)

    def _process_engine_events(self):
        client = is_client()
        for attr in iter_obj_attrs(self):
            if not isinstance(attr, MethodType) or hasattr(attr, '_nyl_listen_args'):
                continue
            name = attr.__name__
            source = _get_event_source(client, name)
            if source:
                self._create_proxy(source[0], source[1], name, attr)

    def _create_proxy(self, ns, sys_name, event_name, method):
        @event(event_name, ns, sys_name)
        def proxy(self, args=None):
            method(EventArgsProxy(args, event_name) if args else None)
        proxy_name = "_nyl_proxy_listen_" + event_name
        proxy.__name__ = proxy_name
        proxy = MethodType(proxy, self)
        setattr(self, proxy_name, proxy)


class ClientEventProxy(_BaseEventProxy):
    """
    | 客户端事件代理类，继承该类的客户端将获得以下功能：
    - 所有ModSDK客户端事件无需监听，编写一个与事件同名的方法即可使用，且事件参数采用对象形式，支持补全。
    - 支持使用 ``@event`` 装饰器监听事件，且无需在 ``.__init__()`` 方法手动调用 ``listen_all_events()``。
    """


class ServerEventProxy(_BaseEventProxy):
    """
    | 服务端事件代理类，继承该类的服务端将获得以下功能：
    - 所有ModSDK服务端事件无需监听，编写一个与事件同名的方法即可使用，且事件参数采用对象形式，支持补全。
    - 支持使用 ``@event`` 装饰器监听事件，且无需在 ``.__init__()`` 方法手动调用 ``listen_all_events()``。
    """


def lib_sys_event(name):
    return event(
        name,
        _const.LIB_NAME,
        _const.LIB_SERVER_NAME if is_client() else _const.LIB_CLIENT_NAME,
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
        assert event.itemDict == a['itemDict']
        assert len(event) == 3
        assert 'playerId' in event
        assert event['playerId'] == a['playerId']
        assert event.items() == a.items()
        event.playerId = "1919810"
        assert event.playerId == a['playerId'] == "1919810"
    CustomEvent(EventArgsProxy(a, "CustomEvent"))

    from ._utils import assert_error
    def f():
        @event("xxx", is_method=False)
        def cb(args):
            pass
    assert_error(f, (), _error.EventSourceError)
    def f():
        @event(is_method=False)
        def cb(args):
            pass
    assert_error(f, (), _error.EventSourceError)
    def f():
        @event(sys_name="system", is_method=False)
        def cb(args):
            pass
    assert_error(f, (), _error.EventSourceError)

    lib_sys = get_lib_system()
    def call(ns, sys_name, event_name, args):
        # 模拟引擎触发回调函数
        func = getattr(lib_sys, ":".join([ns, sys_name, event_name]))
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
    assert LoadClientAddonScriptsAfter._nyl_listen_args == [
        ("mihoyo", "StarRail", "event", 6),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
        ("abc", "system", "LoadClientAddonScriptsAfter", 0),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
    ]
    unlisten_event(LoadClientAddonScriptsAfter)
    assert not getattr(lib_sys, "Minecraft:Engine:LoadClientAddonScriptsAfter")
    assert not getattr(lib_sys, "abc:system:LoadClientAddonScriptsAfter")
    assert not getattr(lib_sys, "mihoyo:StarRail:event")

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
    a = [t, t2]
    assert t.CustomEvent._nyl_listen_args == [
        ("a", "b", "CustomEvent", 0),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
    ]
    assert t.CustomEvent.__name__ == "CustomEvent"
    call("a", "b", "CustomEvent", a)
    n = [0]
    t.CustomEvent(a)
    t2.CustomEvent(a)
    unlisten_all_events(t)
    unlisten_event(t2.CustomEvent)
    assert not getattr(lib_sys, "a:b:CustomEvent")
    assert not getattr(lib_sys, "Minecraft:Engine:LoadClientAddonScriptsAfter")








