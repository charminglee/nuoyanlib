# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-11
|
| ====================================================
"""


import threading
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from . import _const
from ._utils import try_exec
from ._logging import warning, info


__all__ = []


def load_extensions():
    imp = get_api().ImportModule
    if _const.ROOT == "nuoyanlib":
        module_path = "nuoyanlib.extensions"
    else:
        module_path = _const.ROOT + ".nuoyanlib.extensions"
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


def get_env():
    return "client" if is_client() else "server"


def check_env(target):
    if target != get_env():
        from . import error
        raise error.AcrossImportError


_lib_client = None
_lib_server = None


def get_lib_system(_is_client=None):
    if _is_client is None:
        _is_client = is_client()
    if _is_client:
        global _lib_client
        if not _lib_client:
            from .client._lib_client import instance
            _lib_client = instance()
        return _lib_client
    else:
        global _lib_server
        if not _lib_server:
            from .server._lib_server import instance
            _lib_server = instance()
        return _lib_server


def is_apollo():
    return False


def is_client():
    """
    | 判断当前环境是否是客户端。

    -----

    :return: 是则返回True，否则返回False
    :rtype: bool
    """
    return threading.current_thread().name == "MainThread"


def get_api(_is_client=None):
    if _is_client is None:
        _is_client = is_client()
    return c_api if _is_client else s_api


def get_comp_factory(_is_client=None):
    return get_api(_is_client).GetEngineCompFactory()


_CLvComp = None
_SLvComp = None


def get_lv_comp(_is_client=None):
    if _is_client is None:
        _is_client = is_client()
    if _is_client:
        global _CLvComp
        if not _CLvComp:
            from .client.comp import LvComp
            _CLvComp = LvComp
        return _CLvComp
    else:
        global _SLvComp
        if not _SLvComp:
            from .server.comp import LvComp
            _SLvComp = LvComp
        return _SLvComp


_CCF = None
_SCF = None


def get_cf(entity_id, _is_client=None):
    if _is_client is None:
        _is_client = is_client()
    if _is_client:
        global _CCF
        if not _CCF:
            from .client.comp import CF
            _CCF = CF
        return _CCF(entity_id)
    else:
        global _SCF
        if not _SCF:
            from .server.comp import CF
            _SCF = CF
        return _SCF(entity_id)


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
        if is_client():
            sys_name = _const.LIB_CLIENT_NAME
            api = c_api
        else:
            sys_name = _const.LIB_SERVER_NAME
            api = s_api
        system = api.GetSystem(_const.LIB_NAME, sys_name)
        if system:
            return True
        else:
            path = cls.__module__ + "." + cls.__name__
            return bool(api.RegisterSystem(_const.LIB_NAME, sys_name, path))

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



















