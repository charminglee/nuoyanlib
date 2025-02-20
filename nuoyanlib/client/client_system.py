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


import mod.client.extraClientApi as _client_api
from .._core._client._lib_client import (
    get_lib_system as _get_lib_system,
)
from .._core._client._comp import (
    ScreenNode as _ScreenNode,
    ClientSystem as _ClientSystem,
)
from .._core._logging import log as _log
from .._core._listener import quick_listen as _quick_listen


__all__ = [
    "NuoyanClientSystem",
]


@_quick_listen
class NuoyanClientSystem(_ClientSystem):
    """
    | ClientSystem扩展类，将客户端继承本类即可使用其全部功能。
    | ``NuoyanClientSystem`` 已启用快捷监听功能，继承 ``NuoyanClientSystem`` 后无需再使用 ``quick_listen`` 装饰器。

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
        super(NuoyanClientSystem, self).__init__(namespace, system_name)
        self.__lib_sys = _get_lib_system()
        self._set_print_log()
        _log("Inited: %s" % self.__class__.__module__, NuoyanClientSystem)

    def Destroy(self):
        """
        *[event]*

        | 客户端系统销毁时触发。
        | 若重写该方法，请调用一次父类的同名方法。如：
        ::

            class MyClientSystem(NuoyanClientSystem):
                def Destroy(self):
                    super(MyClientSystem, self).Destroy()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanClientSystem, self).Destroy()
        self.UnListenAllEvents()

    # New Interfaces ===================================================================================================

    # noinspection PyUnresolvedReferences
    def BroadcastToAllClient(self, event_name, event_data):
        """
        | 广播事件到所有玩家的客户端，效果与服务端的BroadcastToAllClient类似。
        | 监听时使用当前客户端的命名空间和名称即可。
        | 若传递的数据为字典，则客户端接收到的字典会内置一个名为 ``__id__`` 的key，其value为发送广播的玩家实体ID。

        -----

        :param str event_name: 事件名称
        :param Any event_data: 数据

        :return: 是否成功
        :rtype: bool
        """
        if not self.__lib_sys:
            return False
        self.__lib_sys.broadcast_to_all_client(event_name, event_data, self.namespace, self.systemName)
        return True

    # noinspection PyUnresolvedReferences
    def NotifyToMultiClients(self, player_ids, event_name, event_data):
        """
        | 广播事件到多个玩家的客户端，效果与服务端的NotifyToMultiClients类似。
        | 监听时使用当前客户端的命名空间和名称即可。
        | 若传递的数据为字典，则客户端接收到的字典会内置一个名为 ``__id__`` 的key，其value为发送广播的玩家实体ID。

        -----

        :param list[str] player_ids: 玩家实体ID列表
        :param str event_name: 事件名称
        :param Any event_data: 数据

        :return: 是否成功
        :rtype: bool
        """
        if not self.__lib_sys:
            return False
        self.__lib_sys.notify_to_multi_clients(player_ids, event_name, event_data, self.namespace, self.systemName)
        return True

    def RegisterAndCreateUI(self, namespace, ui_key, cls_path, ui_screen_def, stack=False, param=None):
        """
        | 注册并创建UI。
        | 如果UI已创建，则返回其实例。
        | 使用该接口创建的UI，其UI类 ``__init__`` 方法的 ``param`` 参数会自带一个名为 ``__cs__`` 的key，对应的值为创建UI的客户端的实例，可以方便地调用客户端的属性、方法和接口。

        -----

        :param str namespace: 命名空间，建议为mod名字
        :param str ui_key: UI唯一标识
        :param str cls_path: UI类路径
        :param str ui_screen_def: UI画布路径，格式为"namespace.scree_name"，namespace对应UI json文件中"namespace"的值，scree_name为想打开的画布的名称（一般为main）
        :param bool stack: 是否使用堆栈管理的方式创建UI，默认为False
        :param dict|None param: 创建UI的参数字典，会传到UI类__init__方法的param参数中，默认为空字典

        :return: UI类实例，注册或创建失败时返回None
        :rtype: _ScreenNode|None
        """
        node = _client_api.GetUI(namespace, ui_key)
        if node:
            return node
        if not _client_api.RegisterUI(namespace, ui_key, cls_path, ui_screen_def):
            return
        if param is None:
            param = {}
        if isinstance(param, dict):
            param['__cs__'] = self
        if stack:
            return _client_api.PushScreen(namespace, ui_key, param)
        else:
            return _client_api.CreateUI(namespace, ui_key, param)

    # Internal =========================================================================================================

    def _set_print_log(self):
        _client_api.SetMcpModLogCanPostDump(True)

















