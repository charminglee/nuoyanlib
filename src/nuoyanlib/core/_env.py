# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-14
#  ⠀
#  ================================================


import threading
import traceback


__all__ = [
    "MOD_NAME",
    "CLIENT_MODULES",
    "SERVER_MODULES",
    "CLIENT_SYSTEMS",
    "SERVER_SYSTEMS",
    "get_system",
    "LIB_VERSION",
    "LIB_NAME",
    "LIB_CLIENT_NAME",
    "LIB_SERVER_NAME",
    "get_cls_path",
    "get_file_path",
    "is_client",
    "get_api",
    "get_lv_comp",
    "get_cf",
    "LEVEL_ID",
]


DEBUG = False


class __C: pass
ROOT = __C.__module__.split(".")[0]
del __C


MOD_NAME = None
CLIENT_MODULES = {}
SERVER_MODULES = {}
CLIENT_SYSTEMS = {}
SERVER_SYSTEMS = {}


def get_system(system_name, mod_name=None):
    if not mod_name or mod_name == MOD_NAME:
        if is_client():
            return CLIENT_SYSTEMS.get(system_name)
        else:
            return SERVER_SYSTEMS.get(system_name)
    else:
        get_api().GetSystem(mod_name, system_name)


from .. import __version__


LIB_VERSION = __version__.split("-")[0]
LIB_VERSION_UL = __version__.replace(".", "_").replace("-", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL


def get_cls_path(cls):
    return cls.__module__ + "." + cls.__name__


def get_file_path(index=-2):
    stack = traceback.extract_stack()
    return stack[index][0] if stack else ""


def get_env():
    return "client" if is_client() else "server"


def check_env(target):
    if target != get_env():
        from . import error
        raise error.AcrossImportError


_L = threading.local()


def get_lib_system():
    try:
        return _L.LIB_SYS
    except AttributeError:
        if is_client():
            from .client._lib_client import instance
        else:
            from .server._lib_server import instance
        inst = _L.LIB_SYS = instance()
        return inst


def is_client():
    """
    判断当前环境是否是客户端。

    -----

    :return: 当前环境是否是客户端
    :rtype: bool
    """
    try:
        return _L.IS_CLIENT
    except AttributeError:
        ic = _L.IS_CLIENT = (threading.current_thread().name == "MainThread")
        return ic


def get_api():
    try:
        return _L.API
    except AttributeError:
        if is_client():
            import mod.client.extraClientApi as api
        else:
            import mod.server.extraServerApi as api
        _L.API = api
        return api


def get_lv_comp():
    try:
        return _L.LV_COMP
    except AttributeError:
        if is_client():
            from .client.comp import LvComp
        else:
            from .server.comp import LvComp
        _L.LV_COMP = LvComp
        return LvComp


def get_cf(entity_id):
    try:
        return _L.CF(entity_id)
    except AttributeError:
        if is_client():
            from .client.comp import CF
        else:
            from .server.comp import CF
        _L.CF = CF
        return CF(entity_id)


LEVEL_ID = get_api().GetLevelId()






















