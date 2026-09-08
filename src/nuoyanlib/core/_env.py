# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


import threading


DEBUG = False


class __C: pass
ROOT = __C.__module__.split(".")[0]
del __C


MOD_NAME = None
CLIENT_MODULES = {}
SERVER_MODULES = {}
CLIENT_SYSTEMS = {}
SERVER_SYSTEMS = {}


from .. import __version__


LIB_VERSION = __version__.split("-")[0]
LIB_VERSION_UL = __version__.replace(".", "_").replace("-", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL


def get_cls_path(cls):
    return cls.__module__ + "." + cls.__name__


def get_env():
    return "client" if is_client() else "server"


def check_env(target):
    if target != get_env():
        from . import error
        raise error.AcrossImportError


_THREAD_LOCAL = threading.local()


def get_lib_system():
    try:
        return _THREAD_LOCAL.LIB_SYS
    except AttributeError:
        if is_client():
            from .client._lib_client import instance
        else:
            from .server._lib_server import instance
        inst = _THREAD_LOCAL.LIB_SYS = instance()
        return inst


def is_client():
    """
    判断当前环境是否是客户端。

    -----

    :return: 当前环境是否是客户端
    :rtype: bool
    """
    try:
        return _THREAD_LOCAL.IS_CLIENT
    except AttributeError:
        ic = _THREAD_LOCAL.IS_CLIENT = (threading.current_thread().name == "MainThread")
        return ic


def get_api():
    try:
        return _THREAD_LOCAL.API
    except AttributeError:
        if is_client():
            import mod.client.extraClientApi as api
        else:
            import mod.server.extraServerApi as api
        _THREAD_LOCAL.API = api
        return api


def get_lv_comp():
    try:
        return _THREAD_LOCAL.LV_COMP
    except AttributeError:
        if is_client():
            from .client.comp import LvComp
        else:
            from .server.comp import LvComp
        _THREAD_LOCAL.LV_COMP = LvComp
        return LvComp


def get_cf(entity_id):
    try:
        return _THREAD_LOCAL.CF(entity_id)
    except AttributeError:
        if is_client():
            from .client.comp import CF
        else:
            from .server.comp import CF
        _THREAD_LOCAL.CF = CF
        return CF(entity_id)


LEVEL_ID = get_api().GetLevelId()






















