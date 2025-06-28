# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-24
|
| ==============================================
"""


import mod.client.extraClientApi as client_api
from .comp import ClientSystem, CF, PLAYER_ID
from .. import _const, _logging
from ..listener import ClientEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton


__all__ = []


def instance():
    if not NuoyanLibClientSystem.__instance__:
        NuoyanLibClientSystem.__instance__ = client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME)
    return NuoyanLibClientSystem.__instance__


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibClientSystem, self).__init__(namespace, system_name)
        ln = _const.LIB_NAME
        lsn = _const.LIB_SERVER_NAME
        lcn = _const.LIB_CLIENT_NAME
        self.native_listen(ln, lsn, "_SetQueryCache", self._SetQueryCache)
        self.native_listen(ln, lsn, "_SetQueryVar", self._SetQueryVar)
        self.native_listen(ln, lcn, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ln, lsn, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ln, lcn, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        self.native_listen(ln, lsn, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        _logging.info("NuoyanLibClientSystem inited, ver: %s" % _const.__version__)

    @staticmethod
    def register():
        if not client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME):
            client_api.RegisterSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME, _const.LIB_CLIENT_PATH)

    # General ==========================================================================================================

    def UiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    def broadcast_to_all_client(self, event_name, event_data, ns="", sys_name=""):
        if not ns:
            ns = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_BroadcastToAllClient", {
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    def notify_to_multi_clients(self, player_ids, event_name, event_data, ns="", sys_name=""):
        if not ns:
            ns = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_NotifyToMultiClients", {
            'player_ids': player_ids,
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    def register_and_create_ui(self, namespace, ui_key, cls_path, ui_screen_def, stack=False, param=None):
        """
        | 注册并创建UI。
        | 如果UI已创建，则返回其实例。
        | 使用该接口创建的UI，其UI类 ``.__init__()`` 方法的 ``param`` 参数会自带一个名为 ``__cs__`` 的key，对应的值为创建UI的客户端的实例，可以方便地调用客户端的属性、方法和接口。

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
        node = client_api.GetUI(namespace, ui_key)
        if node:
            return node
        if not client_api.RegisterUI(namespace, ui_key, cls_path, ui_screen_def):
            return
        if param is None:
            param = {}
        if isinstance(param, dict):
            param['__cs__'] = self
        if stack:
            return client_api.PushScreen(namespace, ui_key, param)
        else:
            return client_api.CreateUI(namespace, ui_key, param)

    # set_query_mod_var ================================================================================================

    def _SetQueryCache(self, args):
        for entity_id, queries in args.items():
            for name, value in queries.items():
                comp = CF(entity_id).QueryVariable
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    def _SetQueryVar(self, args):
        if args.get('__id__') == PLAYER_ID:
            return
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        comp = CF(entity_id).QueryVariable
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

    # call =============================================================================================================

    def _NuoyanLibCall(self, args):
        ns = args['ns']
        sys_name = args['sys_name']
        method = args['method']
        uuid = args['uuid']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        player_id = args.get('__id__')
        target_sys = client_api.GetSystem(ns, sys_name)
        def callback(cb_args):
            ret_args = {'uuid': uuid, 'cb_args': cb_args}
            if player_id:
                self.notify_to_multi_clients([player_id], "_NuoyanLibCallReturn", ret_args)
            else:
                self.NotifyToServer("_NuoyanLibCallReturn", ret_args)
        from ...utils.communicate import call_local
        call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        from ...utils.communicate import call_callback
        call_callback(uuid, **cb_args)

















