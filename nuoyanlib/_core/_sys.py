# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


def check_env(target):
    if target == "client" and not is_client():
        raise ImportError("cannot import nuoyanlib.client in server environment")
    if target == "server" and is_client():
        raise ImportError("cannot import nuoyanlib.server in client environment")


def get_lib_system():
    if is_client():
        from ._client._lib_client import instance
    else:
        from ._server._lib_server import instance
    return instance()


def is_apollo():
    return False


def is_client():
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

    def add_event_callback(self, event, callback):
        api = get_api()
        self.ListenForEvent(api.GetEngineNamespace(), api.GetEngineSystemName(), event, callback.__self__, callback) # NOQA

    def remove_event_callback(self, event, callback):
        api = get_api()
        self.UnListenForEvent(api.GetEngineNamespace(), api.GetEngineSystemName(), event, callback.__self__, callback) # NOQA

    def add_condition_to_func(self, cond, func, freq):
        cond_id = max(self.cond_func.iterkeys()) + 1 if self.cond_func else 0
        self.cond_func[cond_id] = (cond, func, freq)
        self.cond_state[cond_id] = False
        return cond_id

    def remove_condition_to_func(self, cond_id):
        if cond_id in self.cond_func:
            del self.cond_func[cond_id]
            del self.cond_state[cond_id]
            return True
        return False



















