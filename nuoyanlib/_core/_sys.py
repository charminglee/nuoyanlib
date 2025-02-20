# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-02-21
#
# ====================================================


__all__ = [
    "get_lib_system",
    "is_apollo",
    "is_client",
    "get_api",
    "get_comp_factory",
    "LEVEL_ID",
]


def get_lib_system():
    if is_client():
        from ._client._lib_client import get_lib_system
    else:
        from ._server._lib_server import get_lib_system
    return get_lib_system()


def is_apollo():
    return False


def is_client():
    try:
        import mod.client.extraClientApi as client_api
        return client_api.GetLocalPlayerId() != "-1"
    except ImportError:
        return False


def get_api():
    if is_client():
        import mod.client.extraClientApi as client_api
        return client_api
    else:
        import mod.server.extraServerApi as server_api
        return server_api


def get_comp_factory():
    return get_api().GetEngineCompFactory()


LEVEL_ID = get_api().GetLevelId()


class NuoyanLibBaseSystem(object):
    def __init__(self, namespace, system_name):
        super(NuoyanLibBaseSystem, self).__init__(namespace, system_name)
        self._cond_func = {}
        self._cond_state = {}
        self.__tick = 0

    def Update(self):
        self.__tick += 1
        for cond_id, (cond, func, freq) in self._cond_func.items():
            if self.__tick % freq:
                continue
            curr_state = cond()
            old_state = self._cond_state[cond_id]
            if curr_state != old_state:
                func(curr_state)
                self._cond_state[cond_id] = curr_state

    def add_condition_to_func(self, cond, func, freq):
        cond_id = max(self._cond_func.iterkeys()) + 1 if self._cond_func else 0
        self._cond_func[cond_id] = (cond, func, freq)
        self._cond_state[cond_id] = False
        return cond_id

    def remove_condition_to_func(self, cond_id):
        if cond_id in self._cond_func:
            del self._cond_func[cond_id]
            del self._cond_state[cond_id]
            return True
        return False



















