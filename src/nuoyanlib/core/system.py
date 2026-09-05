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


from types import MethodType
from collections import defaultdict
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from .listener import _get_event_source, event, EventArgsWrap
from ._utils import iter_obj_attrs
from ._env import is_client
from . import _const


class NySystem(object):
    def __init__(self):
        isc = is_client()
        for attr in iter_obj_attrs(self):
            if not isinstance(attr, MethodType) or hasattr(attr, '_nyl__listen_args'):
                # 跳过属性和已被@event装饰的方法
                continue
            event_name = attr.__name__
            source = _get_event_source(isc, event_name)
            if source:
                @event(event_name, *source)
                def proxy(args):
                    attr(EventArgsWrap(args, event_name) if args else None)
                name = "_nyl__proxy_" + event_name
                proxy.__name__ = name
                setattr(self, name, proxy)


__NCS = None
__NSS = None


def _get_ncs_cls():
    global __NCS
    if not __NCS:
        import mod.client.extraClientApi as api
        CS = api.GetClientSystemCls()

        class NyClientSystem(NySystem, CS):
            def __init__(self, namespace, system_name): # noqa
                NySystem.__init__(self)
                CS.__init__(self, namespace, system_name)

        __NCS = NyClientSystem
    return __NCS


def _get_nss_cls():
    global __NSS
    if not __NSS:
        import mod.server.extraServerApi as api
        SS = api.GetServerSystemCls()

        class NyServerSystem(NySystem, SS):
            def __init__(self, namespace, system_name): # noqa
                NySystem.__init__(self)
                SS.__init__(self, namespace, system_name)

        __NSS = NyServerSystem
    return __NSS


class NuoyanLibBaseSystem(object):
    def __init__(self):
        self.all_sd = defaultdict(list)
        self.unregister_sd_data = {}
        self.is_client = is_client()
        if self.is_client:
            lib_sys_name = _const.LIB_SERVER_NAME
        else:
            lib_sys_name = _const.LIB_CLIENT_NAME
        self.native_listen(_const.LIB_NAME, lib_sys_name, "_NuoyanLibSyncData", self._NuoyanLibSyncData)

    @classmethod
    def run(cls):
        if is_client():
            sys_name = _const.LIB_CLIENT_NAME
            api = c_api
        else:
            sys_name = _const.LIB_SERVER_NAME
            api = s_api
        system = api.GetSystem(_const.LIB_NAME, sys_name)
        if system:
            res = True
        else:
            path = cls.__module__ + "." + cls.__name__
            res = bool(api.RegisterSystem(_const.LIB_NAME, sys_name, path))

        return res

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












