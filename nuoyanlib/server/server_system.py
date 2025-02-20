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
#   Last Modified : 2025-02-20
#
# ====================================================


import mod.server.extraServerApi as _server_api
from .._core._server._comp import (
    ServerSystem as _ServerSystem,
)
from .._core._server._lib_server import (
    get_lib_system as _get_lib_system,
)
from .._core._listener import (
    lib_sys_event as _lib_sys_event,
    event as _event,
)
from .._core._logging import log as _log
from .._core._listener import quick_listen as _quick_listen


__all__ = [
    "NuoyanServerSystem",
]


@_quick_listen
class NuoyanServerSystem(_ServerSystem):
    """
    | ServerSystem扩展类，将服务端继承本类即可使用其全部功能。
    | ``NuoyanServerSystem`` 已启用快捷监听功能，继承 ``NuoyanServerSystem`` 后无需再使用 ``quick_listen`` 装饰器。

    -----

    【基本功能】

    | 1、监听ModSDK事件，只需编写一个与事件同名的方法即可，无需调用 ``ListenForEvent`` 接口，且自带事件说明，无需翻阅官方文档。

    -----

    【注意事项】

    | 1、带有 *[event]* 标签的方法为事件，重写该方法即可使用该事件。
    | 2、带有 *[tick]* 标签的事件为帧事件，需要注意编写相关逻辑。
    | 3、事件回调参数中，参数名前面的美元符号 ``$`` 表示该参数可进行修改。
    | 4、重写 ``Destroy`` 方法后，请调用一次父类的同名方法。
    """

    def __init__(self, namespace, system_name):
        super(NuoyanServerSystem, self).__init__(namespace, system_name)
        self.__lib_sys = _get_lib_system()
        self.all_player_data = {}
        self.first_player_id = "-1"
        self._set_print_log()
        _log("Inited: %s" % self.__class__.__module__, NuoyanServerSystem)

    def Destroy(self):
        """
        *[event]*

        | 服务端系统销毁时触发。
        | 若重写该方法，请调用一次父类的同名方法。如：
        ::

            class MyServerSystem(NuoyanServerSystem):
                def Destroy(self):
                    super(MyServerSystem, self).Destroy()

        :return: 无
        :rtype: None
        """
        super(NuoyanServerSystem, self).Destroy()
        self.UnListenAllEvents()

    # Internal =========================================================================================================

    @_event("AddServerPlayerEvent")
    def _on_add_player(self, args):
        player_id = args['id']
        self.all_player_data.setdefault(player_id, {})
        if self.first_player_id == "-1":
            self.first_player_id = player_id

    @_event("PlayerIntendLeaveServerEvent")
    def _on_player_intend_leave(self, args):
        player_id = args['playerId']
        if player_id in self.all_player_data:
            del self.all_player_data[player_id]

    @_lib_sys_event("_ButtonCallbackTrigger")
    def _on_btn_callback_trigger(self, args):
        func_name = args['name']
        func_args = args['args']
        func_args['__id__'] = args['__id__']
        func = getattr(self, func_name, None)
        if func:
            func(func_args)

    def _set_print_log(self):
        _server_api.SetMcpModLogCanPostDump(True)






















