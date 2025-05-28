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
#   Last Modified : 2025-05-28
#
# ====================================================


import mod.client.extraClientApi as _client_api
from . import _comp
from .. import _const, _listener, _sys, _logging
from ...utils import communicate as _communicate


def instance():
    return NuoyanLibClientSystem.instance


class NuoyanLibClientSystem(_listener.ClientEventProxy, _sys.NuoyanLibBaseSystem, _comp.ClientSystem):
    @staticmethod
    def init():
        if not _client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME):
            _client_api.RegisterSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME, _const.LIB_CLIENT_PATH)

    def __init__(self, namespace, system_name):
        super(NuoyanLibClientSystem, self).__init__(namespace, system_name)
        _logging.log("Inited, ver: %s" % _const.__version__, NuoyanLibClientSystem)

    # General ==========================================================================================================

    def UiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    def broadcast_to_all_client(self, event_name, event_data, namespace="", sys_name=""):
        if not namespace:
            namespace = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_BroadcastToAllClient", {
            'event_name': event_name,
            'event_data': event_data,
            'namespace': namespace,
            'sys_name': sys_name,
        })

    def notify_to_multi_clients(self, player_ids, event_name, event_data, namespace="", sys_name=""):
        if not namespace:
            namespace = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_NotifyToMultiClients", {
            'player_ids': player_ids,
            'event_name': event_name,
            'event_data': event_data,
            'namespace': namespace,
            'sys_name': sys_name,
        })

    def register_and_create_ui(self, namespace, ui_key, cls_path, ui_screen_def, stack=False, param=None):
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

    # set_query_mod_var ================================================================================================

    @_listener.lib_sys_event
    def _SetQueryCache(self, args):
        for entity_id, queries in args.items():
            for name, value in queries.items():
                comp = _comp.CompFactory.CreateQueryVariable(entity_id)
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    @_listener.lib_sys_event
    def _SetQueryVar(self, args):
        if args.get('__id__') == _comp.PLAYER_ID:
            return
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        comp = _comp.CompFactory.CreateQueryVariable(entity_id)
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

    # call =============================================================================================================

    @_listener.event(namespace=_const.LIB_NAME, system_name=_const.LIB_CLIENT_NAME)
    @_listener.event(namespace=_const.LIB_NAME, system_name=_const.LIB_SERVER_NAME)
    def _NuoyanLibCall(self, args):
        namespace = args['namespace']
        system_name = args['system_name']
        method = args['method']
        uuid = args['uuid']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        player_id = args.get('__id__')
        target_sys = _client_api.GetSystem(namespace, system_name)
        def callback(cb_args):
            if player_id:
                self.notify_to_multi_clients(
                    [player_id],
                    "_NuoyanLibCallReturn",
                    {'uuid': uuid, 'cb_args': cb_args},
                )
            else:
                self.NotifyToServer("_NuoyanLibCallReturn", {'uuid': uuid, 'cb_args': cb_args})
        _communicate.call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    @_listener.event(namespace=_const.LIB_NAME, system_name=_const.LIB_CLIENT_NAME)
    @_listener.event(namespace=_const.LIB_NAME, system_name=_const.LIB_SERVER_NAME)
    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        _communicate.call_callback(uuid, **cb_args)


















