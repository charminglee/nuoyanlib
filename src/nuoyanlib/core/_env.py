# -*- coding: utf-8 -*-
#  =================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  =================================================


import threading
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api


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






















