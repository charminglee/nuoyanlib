# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-10
|
| ==============================================
"""


from weakref import WeakValueDictionary
from types import FunctionType, MethodType
from . import _error


__all__ = []


def check_env(target):
    if target == "client" and not is_client():
        raise _error.NotInClientError
    if target == "server" and is_client():
        raise _error.NotInServerError


def get_lib_system():
    if is_client():
        from ._client._lib_client import instance
    else:
        from ._server._lib_server import instance
    return instance()


def is_apollo():
    return False


def is_client():
    """
    | 判断当前环境是否是客户端。

    -----

    :return: 是则返回True，否则返回False
    :rtype: bool
    """
    from threading import current_thread
    return current_thread().name == "MainThread"


def get_api():
    if is_client():
        import mod.client.extraClientApi as api
    else:
        import mod.server.extraServerApi as api
    return api


def get_comp_factory():
    return get_api().GetEngineCompFactory()


LEVEL_ID = get_api().GetLevelId()


class NuoyanLibBaseSystem(object):
    def __init__(self, *args, **kwargs):
        super(NuoyanLibBaseSystem, self).__init__(*args, **kwargs)
        self.cond_func = {}
        self.cond_state = {}
        self.__tick = 0
        self.listen_map = WeakValueDictionary()

    def Update(self):
        self.__tick += 1
        for cond_id, (cond, func, freq) in self.cond_func.items():
            if self.__tick % freq:
                continue
            curr_state = cond()
            old_state = self.cond_state[cond_id]
            if curr_state != old_state:
                func(curr_state)
                self.cond_state[cond_id] = curr_state

    def Destroy(self):
        self.UnListenAllEvents() # NOQA
        self.listen_map.clear()

    def _get_self(self, method):
        from ._listener import event
        return method.__self__() if isinstance(method, event) else method.__self__

    def native_listen(self, ns, sys_name, event_name, method, priority=0):
        ins = self._get_self(method)
        self.ListenForEvent(ns, sys_name, event_name, ins, method, priority) # NOQA

    def native_unlisten(self, ns, sys_name, event_name, method, priority=0):
        ins = self._get_self(method)
        self.UnListenForEvent(ns, sys_name, event_name, ins, method, priority) # NOQA

    def listen_for(self, ns, sys_name, event_name, func, priority=0):
        key = (ns, sys_name, event_name, id(func), priority)
        if key in self.listen_map:
            return False
        if isinstance(func, FunctionType):
            def method(_, a=None):
                func(a if a else {})
            from ..utils.mc_random import random_string
            rand = random_string(16, num=False)
            method.__name__ = rand
            method = MethodType(method, self)
            setattr(self, rand, method)
        else:
            method = func
        self.listen_map[key] = method
        self.native_listen(ns, sys_name, event_name, method, priority)
        return True

    def unlisten_for(self, ns, sys_name, event_name, func, priority=0):
        key = (ns, sys_name, event_name, id(func), priority)
        method = self.listen_map.pop(key, None)
        if method:
            self.native_unlisten(ns, sys_name, event_name, method, priority)
            return True
        return False

    def add_condition_to_func(self, cond, func, freq):
        cond_id = max(self.cond_func.iterkeys()) + 1 if self.cond_func else 0
        self.cond_func[cond_id] = (cond, func, freq)
        self.cond_state[cond_id] = False
        return cond_id

    def rm_condition_to_func(self, cond_id):
        if cond_id in self.cond_func:
            del self.cond_func[cond_id]
            del self.cond_state[cond_id]
            return True
        return False



















