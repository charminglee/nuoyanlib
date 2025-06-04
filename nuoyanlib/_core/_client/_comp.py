# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


import mod.client.extraClientApi as _client_api
from .._utils import CacheObject as _CacheObject


ENGINE_NAMESPACE = _client_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = _client_api.GetEngineSystemName()
PLAYER_ID = _client_api.GetLocalPlayerId()
LEVEL_ID = _client_api.GetLevelId()
ClientSystem = _client_api.GetClientSystemCls()
CompFactory = _client_api.GetEngineCompFactory()


ScreenNode = _client_api.GetScreenNodeCls()
ViewBinder = _client_api.GetViewBinderCls()
ViewRequest = _client_api.GetViewViewRequestCls()
CustomUIScreenProxy = _client_api.GetUIScreenProxyCls()
CustomUIControlProxy = _client_api.GetCustomUIControlProxyCls()
NativeScreenManager = _client_api.GetNativeScreenManagerCls().instance() # NOQA
MiniMapScreenNode = _client_api.GetMiniMapScreenNodeCls()


class CF(_CacheObject):
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(CompFactory, "Create" + name)(self._target)


PlrComp = CF(PLAYER_ID)
LvComp = CF(LEVEL_ID)









