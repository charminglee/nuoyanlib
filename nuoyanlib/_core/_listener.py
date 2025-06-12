# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


import weakref
from functools import update_wrapper
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
    "listen_for",
    "unlisten_for",
    "EventArgsProxy",
    "ClientEventProxy",
    "ServerEventProxy",
    "event",
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


def listen_for(*args, **kwargs):
    """
    | 通用事件监听。支持对普通函数与实例方法添加事件监听，回调函数不再需要与类绑定。
    | 若要移除监听，请使用 ``unlisten_for()`` 。

    -----

    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param str event_name: 事件名称
    :param function func: 事件回调函数
    :param int priority: 优先级，默认为0

    :return: 无
    :rtype: None
    """
    get_lib_system().listen_for(*args, **kwargs)


def unlisten_for(*args, **kwargs):
    """
    | 移除通过 ``listen_for()`` 或 ``@event`` 添加的事件监听。

    -----

    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param str event_name: 事件名称
    :param function func: 事件回调函数
    :param int priority: 优先级，默认为0

    :return: 无
    :rtype: None
    """
    get_lib_system().unlisten_for(*args, **kwargs)


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
        listen_for(ns, sys_name, event_name, proxy, priority)


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


class event(object):
    """
    [装饰器]

    | 事件监听器。监听ModSDK事件时，可省略 ``ns`` 和 ``sys_name`` 参数。
    | 适用于普通函数与实例方法，若用于普通函数，请将 ``is_method`` 参数设为 ``False`` 。

    -----

    :param str event_name: 事件名称，默认为被装饰函数名
    :param str ns: 事件来源命名空间
    :param str sys_name: 事件来源系统名称
    :param int priority: 优先级，默认为0
    :param bool is_method: 回调函数是否是实例方法，默认为True

    :return: 返回event类
    :rtype: event
    """

    def __init__(self, event_name="", ns="", sys_name="", priority=0, is_method=True):
        self._ns = ns
        self._sys_name = sys_name
        self._priority = priority
        self._is_method = is_method
        self._func = None
        self.__self__ = None
        self.listen_args = []
        if callable(event_name):
            # @event
            self._event_name = ""
            self._bind_func(event_name)
        else:
            self._event_name = event_name

    def __call__(self, *args, **kwargs):
        if not self._func:
            # @event(...)
            self._bind_func(args[0])
            return self
        else:
            # 调用原函数
            return (
                self._func(self.__self__(), *args, **kwargs)
                if self._is_method
                else self._func(*args, **kwargs)
            )

    def _bind_func(self, func):
        if isinstance(func, event):
            # 处理嵌套@event
            self.listen_args.extend(func.listen_args)
            func = func._func
        self._func = func
        update_wrapper(self, func)
        if not self._event_name:
            self._event_name = func.__name__
        if not self._ns or not self._sys_name:
            source = _get_event_source(is_client(), self._event_name, self._ns, self._sys_name)
            if not source:
                raise _error.EventSourceError(self._event_name, self._ns, self._sys_name)
            self._ns, self._sys_name = source
        args = (self._ns, self._sys_name, self._event_name, self._priority)
        self.listen_args.append(args)
        if not self._is_method:
            self._listen(args)

    def _listen(self, args):
        func = self if self._is_method else self._func
        unlisten_for(args[0], args[1], args[2], func, args[3]) # 防止重复监听相同参数的事件
        listen_for(args[0], args[1], args[2], func, args[3])

    def unlisten(self):
        """
        | 移除事件监听。

        -----

        :return: 无
        :rtype: None
        """
        func = self if self._is_method else self._func
        for args in self.listen_args:
            unlisten_for(args[0], args[1], args[2], func, args[3])

    def __get__(self, ins, cls):
        # 用于获取回调函数所在实例
        if self.__self__ is None:
            self.__self__ = weakref.ref(ins)
        return self

    @staticmethod
    def _get_all_event_ins(ins):
        for name in dir(ins):
            try:
                attr = getattr(ins, name) # 获取到event描述符时将触发event.__get__
            except AttributeError:
                continue
            if isinstance(attr, event):
                yield attr

    @staticmethod
    def listen_all(ins):
        """
        | 对当前类中所有被 ``@event`` 装饰的方法执行事件监听。

        -----

        :param Any ins: 当前类的实例

        :return: 无
        :rtype: None
        """
        for e in event._get_all_event_ins(ins):
            for args in e.listen_args:
                e._listen(args)

    @staticmethod
    def unlisten_all(ins):
        """
        | 对当前类中所有被 ``@event`` 装饰的方法执行事件反监听。

        -----

        :param Any ins: 当前类的实例

        :return: 无
        :rtype: None
        """
        for e in event._get_all_event_ins(ins):
            e.unlisten()


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

    def call(event_obj, args):
        key = (
            event_obj._ns,
            event_obj._sys_name,
            event_obj._event_name,
            id(event_obj if event_obj._is_method else event_obj._func),
            event_obj._priority,
        )
        cb = get_lib_system().listen_map[key]
        ins = cb.__self__
        if isinstance(ins, weakref.ReferenceType):
            ins = ins() # NOQA
        func = getattr(ins, cb.__name__) # 模拟引擎触发回调函数
        func(args)

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
    assert (
        LoadClientAddonScriptsAfter._ns,
        LoadClientAddonScriptsAfter._sys_name,
        LoadClientAddonScriptsAfter._event_name,
    ) == ("Minecraft", "Engine", "LoadClientAddonScriptsAfter")
    assert [i[:3] for i in LoadClientAddonScriptsAfter.listen_args] == [
        ("mihoyo", "StarRail", "event"),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter"),
        ("abc", "system", "LoadClientAddonScriptsAfter"),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter"),
    ]
    LoadClientAddonScriptsAfter.unlisten()

    a = {'a': 1}
    class T(object):
        def __init__(self):
            event.listen_all(self)
        @event("LoadClientAddonScriptsAfter")
        @event(ns="a", sys_name="b")
        def CustomEvent(self, args):
            assert self is t
            assert args is a
    t = T()
    call(t.CustomEvent, a)
    t.CustomEvent(a)
    assert [i[:3] for i in t.CustomEvent.listen_args] == [
        ("a", "b", "CustomEvent"),
        ("Minecraft", "Engine", "LoadClientAddonScriptsAfter"),
    ]
    assert t.CustomEvent.__name__ == "CustomEvent"
    event.unlisten_all(t)

    # class A(object):
    #     pass
    # a = A()
    # @event("LoadClientAddonScriptsAfter")
    # @event(ns="a", sys_name="b")
    # def _CustomEvent(self, args):
    #     assert self is a
    #     assert args == {'a': 1}
    # a.CustomEvent = _CustomEvent
    # a.CustomEvent({'a': 1})
    # for i in a.CustomEvent.listen_args:
    #     print(i)
    # assert a.CustomEvent.__name__ == "_CustomEvent"
    # a.CustomEvent.unlisten()
    # assert not a.CustomEvent.listen_args










