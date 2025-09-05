# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-06
|
| ==============================================
"""


from threading import current_thread


__all__ = [
    "get_env",
    "is_client",
    "get_api",
    "get_comp_factory",
    "get_lv_comp",
]


DEV_MOVE = True


def get_env():
    return "client" if is_client() else "server"


def load_extensions():
    from ._const import ROOT
    from ._utils import try_exec
    from ._logging import warning, info
    imp = get_api().ImportModule

    if ROOT == "nuoyanlib":
        module_path = "nuoyanlib.extensions"
    else:
        module_path = ROOT + ".nuoyanlib.extensions"
    try:
        ext_module = imp(module_path)
        ext_list = ext_module.EXTENSION_LOADING_LIST
    except (ImportError, AttributeError):
        return []

    env = get_env()
    loaded_ext = []
    for name in ext_list:
        full_name = name + "." + env
        try:
            module = imp("%s.%s" % (ext_module, full_name))
            res = try_exec(module.init)
        except (ImportError, AttributeError):
            continue
        if isinstance(res, Exception):
            warning("Extension '%s' loading failed", full_name)
        else:
            loaded_ext.append(name)

    info("Loaded extensions: %s", loaded_ext)
    return loaded_ext


def check_env(target):
    if DEV_MOVE:
        return
    if target != get_env():
        from . import _error
        raise _error.AcrossImportError


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
    return current_thread().name == "MainThread"


def get_api():
    if is_client():
        import mod.client.extraClientApi as api
    else:
        import mod.server.extraServerApi as api
    return api


def get_comp_factory():
    return get_api().GetEngineCompFactory()


def get_lv_comp():
    if is_client():
        from ._client.comp import LvComp
    else:
        from ._server.comp import LvComp
    return LvComp


LEVEL_ID = get_api().GetLevelId()


class NuoyanLibBaseSystem(object):
    def __init__(self, *args, **kwargs):
        super(NuoyanLibBaseSystem, self).__init__(*args, **kwargs)
        self.__tick = 0
        self.cond_func = {}
        self.cond_state = {}
        self.event_pool = {}

    @classmethod
    def register(cls):
        raise NotImplementedError

    def get_lib_dict(self):
        raise NotImplementedError

    def Update(self):
        self.__tick += 1
        for cond_id, (cond, func, freq) in self.cond_func.items():
            if self.__tick % freq or cond_id not in self.cond_state:
                continue
            curr_state = cond()
            old_state = self.cond_state[cond_id]
            if curr_state != old_state:
                func(curr_state)
                self.cond_state[cond_id] = curr_state

    def Destroy(self):
        self.UnListenAllEvents() # NOQA
        self.cond_func.clear()
        self.cond_state.clear()
        self.event_pool.clear()

    def native_listen(self, ns, sys_name, event_name, method, priority=0):
        self.ListenForEvent(ns, sys_name, event_name, method.__self__, method, priority) # NOQA

    def native_unlisten(self, ns, sys_name, event_name, method, priority=0):
        self.UnListenForEvent(ns, sys_name, event_name, method.__self__, method, priority) # NOQA

    def add_condition_to_func(self, cond, func, freq):
        cond_id = max(self.cond_func.iterkeys()) + 1 if self.cond_func else 0
        self.cond_func[cond_id] = (cond, func, freq)
        self.cond_state[cond_id] = False
        func(cond())
        return cond_id

    def rm_condition_to_func(self, cond_id):
        if cond_id in self.cond_func:
            del self.cond_func[cond_id]
            del self.cond_state[cond_id]
            return True
        return False



















