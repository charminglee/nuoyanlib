# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-22
|
| ==============================================
"""


import mod.client.extraClientApi as client_api


__all__ = [
    "ENGINE_NAMESPACE",
    "ENGINE_SYSTEM_NAME",
    "PLAYER_ID",
    "LEVEL_ID",
    "ClientSystem",
    "CompFactory",
    "ScreenNode",
    "ViewBinder",
    "ViewRequest",
    "CustomUIScreenProxy",
    "CustomUIControlProxy",
    "NativeScreenManager",
    "MiniMapScreenNode",
    "CF",
    "PlrComp",
    "LvComp",
]


ENGINE_NAMESPACE = client_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = client_api.GetEngineSystemName()
PLAYER_ID = client_api.GetLocalPlayerId()
LEVEL_ID = client_api.GetLevelId()
ClientSystem = client_api.GetClientSystemCls()
CompFactory = client_api.GetEngineCompFactory()


ScreenNode = client_api.GetScreenNodeCls()
ViewBinder = client_api.GetViewBinderCls()
ViewRequest = client_api.GetViewViewRequestCls()
CustomUIScreenProxy = client_api.GetUIScreenProxyCls()
CustomUIControlProxy = client_api.GetCustomUIControlProxyCls()
NativeScreenManager = client_api.GetNativeScreenManagerCls().instance() # NOQA
MiniMapScreenNode = client_api.GetMiniMapScreenNodeCls()


class CF(object):
    __slots__ = ('_target', '_comp_cache')
    __cache__ = {}

    def __new__(cls, target):
        if target not in cls.__cache__:
            cls.__cache__[target] = object.__new__(cls)
        return cls.__cache__[target]

    def __init__(self, target):
        self._target = target
        self._comp_cache = {}

    def __getattr__(self, name):
        if name not in self._comp_cache:
            self._comp_cache[name] = getattr(CompFactory, "Create" + name)(self._target)
        return self._comp_cache[name]


PlrComp = CF(PLAYER_ID)
LvComp = CF(LEVEL_ID)








