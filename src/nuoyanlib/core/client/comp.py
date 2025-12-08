# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-03
|
| ====================================================
"""


import mod.client.extraClientApi as c_api


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


ENGINE_NAMESPACE = c_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = c_api.GetEngineSystemName()
PLAYER_ID = c_api.GetLocalPlayerId()
LEVEL_ID = c_api.GetLevelId()
ClientSystem = c_api.GetClientSystemCls()
CompFactory = c_api.GetEngineCompFactory()


ScreenNode = c_api.GetScreenNodeCls()
ViewBinder = c_api.GetViewBinderCls()
ViewRequest = c_api.GetViewViewRequestCls()
CustomUIScreenProxy = c_api.GetUIScreenProxyCls()
CustomUIControlProxy = c_api.GetCustomUIControlProxyCls()
NativeScreenManager = c_api.GetNativeScreenManagerCls().instance()
MiniMapScreenNode = c_api.GetMiniMapScreenNodeCls()


class CF(object):
    __cache__ = {}

    def __new__(cls, target):
        if target not in cls.__cache__:
            cls.__cache__[target] = object.__new__(cls)
        return cls.__cache__[target]

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        comp = getattr(CompFactory, "Create" + name)(self._target)
        if not comp:
            return
        setattr(self, name, comp)
        return comp


PlrComp = CF(PLAYER_ID)
"""
本地玩家组件工厂。
"""
LvComp = CF(LEVEL_ID)
"""
使用 Level Id 创建的组件工厂。
"""








