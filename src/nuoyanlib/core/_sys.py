# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from collections import defaultdict
import threading
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from . import _const
from ._logging import warning, info


def load_extensions():
    from ._utils import try_exec
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


_THREAD_LOCAL = threading.local()


def get_lib_system():
    if not hasattr(_THREAD_LOCAL, 'lib_sys'):
        if is_client():
            from .client._lib_client import instance
        else:
            from .server._lib_server import instance
        _THREAD_LOCAL.lib_sys = instance()
    return _THREAD_LOCAL.lib_sys


def is_client():
    """
    判断当前环境是否是客户端。

    -----

    :return: 是则返回True，否则返回False
    :rtype: bool
    """
    return threading.current_thread().name == "MainThread"


def get_api():
    if not hasattr(_THREAD_LOCAL, 'api'):
        _THREAD_LOCAL.api = c_api if is_client() else s_api
    return _THREAD_LOCAL.api


def get_lv_comp():
    if not hasattr(_THREAD_LOCAL, 'LvComp'):
        if is_client():
            from .client.comp import LvComp
        else:
            from .server.comp import LvComp
        _THREAD_LOCAL.LvComp = LvComp
    return _THREAD_LOCAL.LvComp


def get_cf(entity_id):
    if not hasattr(_THREAD_LOCAL, 'CF'):
        if is_client():
            from .client.comp import CF
        else:
            from .server.comp import CF
        _THREAD_LOCAL.CF = CF
    return _THREAD_LOCAL.CF(entity_id)


LEVEL_ID = get_api().GetLevelId()


class NuoyanLibBaseSystem(object):
    def __init__(self, namespace, system_name):
        super(NuoyanLibBaseSystem, self).__init__(namespace, system_name)
        self.all_sd = defaultdict(list)
        self.unregister_sd_data = {}
        self.is_client = is_client()
        if self.is_client:
            lib_sys_name = _const.LIB_SERVER_NAME
        else:
            lib_sys_name = _const.LIB_CLIENT_NAME
        self.native_listen(_const.LIB_NAME, lib_sys_name, "_NuoyanLibSyncData", self._NuoyanLibSyncData)

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

    def Destroy(self):
        self.UnListenAllEvents() # noqa

    def native_listen(self, ns, sys_name, event_name, method, priority=0):
        self.ListenForEvent(ns, sys_name, event_name, method.__self__, method, priority) # noqa

    def native_unlisten(self, ns, sys_name, event_name, method, priority=0):
        self.UnListenForEvent(ns, sys_name, event_name, method.__self__, method, priority) # noqa

    # region SyncData ==================================================================================================

    def _NuoyanLibSyncData(self, all_data):
        for k, v in all_data.items():
            if k in self.all_sd:
                for sd in self.all_sd[k]:
                    if sd._flag != sd.F_SOURCE:
                        sd._on_engine_sync(v)
            else:
                self.unregister_sd_data[k] = v

    def register_sd(self, sd):
        k = sd.key
        if k in self.all_sd and self.all_sd[k][0]._flag == sd.F_SOURCE:
            # 已存在同名数据源
            raise KeyError("SyncData key '%s' already exists" % k)
        if sd._flag != sd.F_SOURCE:
            if k in self.all_sd:
                sd.value = self.all_sd[k][0].value
            elif k in self.unregister_sd_data:
                sd.value = self.unregister_sd_data.pop(k)
        self.all_sd[k].append(sd)

    def sync(self, key):
        data = {key: self.all_sd[key][0].value}
        if self.is_client:
            self.NotifyToServer("_NuoyanLibSyncData", data) # noqa
        else:
            self.BroadcastToAllClient("_NuoyanLibSyncData", data) # noqa

    def sync_all(self, player_id=None):
        if not self.all_sd:
            return
        all_data = {
            key: sd_list[0].value
            for key, sd_list in self.all_sd.items()
            if len(sd_list) == 1
        }
        if self.is_client:
            self.NotifyToServer("_NuoyanLibSyncData", all_data) # noqa
        else:
            if player_id:
                self.NotifyToClient(player_id, "_NuoyanLibSyncData", all_data) # noqa
            else:
                self.BroadcastToAllClient("_NuoyanLibSyncData", all_data) # noqa

    # endregion




















