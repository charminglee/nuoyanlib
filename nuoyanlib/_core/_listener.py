# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-16
|
| ==============================================
"""


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


__all__ = [
    "EventArgsProxy",
    "ClientEventProxy",
    "ServerEventProxy",
    "event",
    "listen_event",
    "unlisten_event",
    "listen_all_events",
    "unlisten_all_events",
]


def _get_event_source(client, event_name, ns="", sys_name=""):
    if client:
        if event_name in ALL_CLIENT_ENGINE_EVENTS:
            return client_api.GetEngineNamespace(), client_api.GetEngineSystemName()
        elif event_name in ALL_CLIENT_LIB_EVENTS:
            return _const.LIB_NAME, _const.LIB_CLIENT_NAME
    else:
        if event_name in ALL_SERVER_ENGINE_EVENTS:
            return server_api.GetEngineNamespace(), server_api.GetEngineSystemName()
        elif event_name in ALL_SERVER_LIB_EVENTS:
            return _const.LIB_NAME, _const.LIB_SERVER_NAME
    return (ns, sys_name) if ns and sys_name else None


def _listen_for(ns, sys_name, event_name, func, priority):
    get_lib_system().listen_for(ns, sys_name, event_name, func, priority)


def _unlisten_for(ns, sys_name, event_name, func, priority):
    get_lib_system().unlisten_for(ns, sys_name, event_name, func, priority)


class EventArgsProxy(object):
    def __init__(self, arg_dict, event_name):
        self.arg_dict = arg_dict
        self.event_name = event_name

    def __getattr__(self, key):
        if key in self.arg_dict:
            return self.arg_dict[key]
        # 代理dict方法
        if hasattr(self.arg_dict, key):
            return getattr(self.arg_dict, key)
        raise _error.EventParameterError(self.event_name, key)

    def __setattr__(self, key, value):
        # 兼容可修改的事件参数
        object.__setattr__(self, key, value)
        if key in self.arg_dict:
            self.arg_dict[key] = value

    def __repr__(self):
        s = "<EventArgsProxy of '%s':" % self.event_name
        for k, v in self.arg_dict.items():
            s += "\n  .%s = %s" % (k, repr(v))
        s += "\n>"
        return s

    __len__      = lambda self:    self.arg_dict.__len__()
    __contains__ = lambda self, a: self.arg_dict.__contains__(a)
    __getitem__  = lambda self, a: self.arg_dict.__getitem__(a)
    __setitem__  = lambda self, a: self.arg_dict.__setitem__(a)
    __cmp__      = lambda self, a: self.arg_dict.__cmp__(a)
    __delitem__  = lambda self, a: self.arg_dict.__delitem__(a)
    __eq__       = lambda self, a: self.arg_dict.__eq__(a)
    __ge__       = lambda self, a: self.arg_dict.__ge__(a)
    __gt__       = lambda self, a: self.arg_dict.__gt__(a)
    __iter__     = lambda self:    self.arg_dict.__iter__()
    __le__       = lambda self, a: self.arg_dict.__le__(a)
    __lt__       = lambda self, a: self.arg_dict.__lt__(a)
    __ne__       = lambda self, a: self.arg_dict.__ne__(a)


class _BaseEventProxy(object):
    def __init__(self, *args, **kwargs):
        super(_BaseEventProxy, self).__init__(*args, **kwargs)
        self._listen_events()

    def _listen_events(self):
        client = is_client()
        for attr in dir(self):
            try:
                method = getattr(self, attr)
            except:
                continue
            if not isinstance(method, MethodType):
                continue
            name = method.__name__
            source = _get_event_source(client, name)
            if source:
                self._proxy_listen(*source, event_name=name, method=method)

    def _proxy_listen(self, ns, sys_name, event_name, method, priority=0):
        def proxy(_, args=None):
            method(EventArgsProxy(args, event_name) if args else None)
        proxy_name = "_proxy_" + event_name
        proxy.__name__ = proxy_name
        proxy = MethodType(proxy, self)
        setattr(self, proxy_name, proxy)
        _listen_for(ns, sys_name, event_name, proxy, priority)


class ClientEventProxy(_BaseEventProxy):
    """
    | 客户端事件代理类，继承该类的客户端将获得以下功能：
    | 所有客户端事件无需监听，编写一个与事件同名的方法即可使用该事件，且事件参数采用对象形式，支持补全。
    """


class ServerEventProxy(_BaseEventProxy):
    """
    | 服务端事件代理类，继承该类的服务端将获得以下功能：
    | 所有服务端事件无需监听，编写一个与事件同名的方法即可使用该事件，且事件参数采用对象形式，支持补全。
    """


_LISTEN_ARGS_KEY = "_nyl_listen_args"


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
    :param int priority: 优先级，默认为0
    :param bool is_method: 回调函数是否是实例方法，默认为True

    :return: 返回原函数
    :rtype: function
    """
    def add_listener(func):
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
        if not hasattr(func, _LISTEN_ARGS_KEY):
            func._nyl_listen_args = []
        func._nyl_listen_args.append(args)
        if not is_method:
            _unlisten_for(_ns, _sys_name, _event_name, func, priority) # 防止重复监听相同参数的事件
            _listen_for(_ns, _sys_name, _event_name, func, priority)
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
    args = getattr(func, _LISTEN_ARGS_KEY, None)
    return args if args else []


def listen_event(func):
    """
    | 执行事件监听。

    -----

    :param function func: 事件回调函数

    :return: 无
    :rtype: None
    """
    for a in _get_event_args(func):
        _unlisten_for(a[0], a[1], a[2], func, a[3])
        _listen_for(a[0], a[1], a[2], func, a[3])


def unlisten_event(func):
    """
    | 移除事件监听。

    -----

    :param function func: 事件回调函数

    :return: 无
    :rtype: None
    """
    for a in _get_event_args(func):
        _unlisten_for(a[0], a[1], a[2], func, a[3])


def _get_all_event_args(ins):
    for name in dir(ins):
        try:
            attr = getattr(ins, name)
        except AttributeError:
            continue
        args = _get_event_args(attr)
        if args:
            yield attr, args


def listen_all_events(ins):
    """
    | 对实例中所有被 ``@event`` 装饰的方法执行事件监听。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, args in _get_all_event_args(ins):
        for a in args:
            _unlisten_for(a[0], a[1], a[2], method, a[3])
            _listen_for(a[0], a[1], a[2], method, a[3])


def unlisten_all_events(ins):
    """
    | 对实例中所有被 ``@event`` 装饰的方法执行事件反监听。

    -----

    :param Any ins: 类实例（通常为self参数）

    :return: 无
    :rtype: None
    """
    for method, args in _get_all_event_args(ins):
        for a in args:
            _unlisten_for(a[0], a[1], a[2], method, a[3])


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
        assert event.playerId == a['playerId']
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

    def call(func, args):
        if isinstance(func, MethodType):
            cb = func
        else:
            listen_args = getattr(func, _LISTEN_ARGS_KEY)[0]
            key = (
                listen_args[0],
                listen_args[1],
                listen_args[2],
                id(func),
                listen_args[3],
            )
            cb = get_lib_system().listen_map[key]
        # 模拟引擎触发回调函数
        func = getattr(cb.__self__, cb.__name__)
        func(args)

    lm = get_lib_system().listen_map.copy()
    a = {'arg': 1}
    @event(is_method=False)
    @event(ns="abc", sys_name="system", is_method=False)
    @event("LoadClientAddonScriptsAfter", is_method=False)
    @event("event", "mihoyo", "StarRail", 6, is_method=False)
    def LoadClientAddonScriptsAfter(args):
        assert args is a
    call(LoadClientAddonScriptsAfter, a)
    LoadClientAddonScriptsAfter(a)
    assert LoadClientAddonScriptsAfter.__name__ == "LoadClientAddonScriptsAfter"
    assert getattr(LoadClientAddonScriptsAfter, _LISTEN_ARGS_KEY) == [
        ("mihoyo", "StarRail", "event", 6),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
        ("abc", "system", "LoadClientAddonScriptsAfter", 0),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
    ], getattr(LoadClientAddonScriptsAfter, _LISTEN_ARGS_KEY)
    unlisten_event(LoadClientAddonScriptsAfter)

    class T(object):
        def __init__(self):
            listen_all_events(self)
        @event("LoadClientAddonScriptsAfter")
        @event(ns="a", sys_name="b")
        def CustomEvent(self, args):
            assert self is args['ins']
    t = T()
    a = {'ins': t}
    t2 = T()
    a2 = {'ins': t2}
    assert getattr(t.CustomEvent, _LISTEN_ARGS_KEY) == [
        ("a", "b", "CustomEvent", 0),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter", 0),
    ]
    assert t.CustomEvent.__name__ == "CustomEvent"
    call(t.CustomEvent, a)
    t.CustomEvent(a)
    call(t2.CustomEvent, a2)
    t2.CustomEvent(a2)
    unlisten_all_events(t)
    unlisten_event(t2.CustomEvent)
    assert get_lib_system().listen_map == lm








