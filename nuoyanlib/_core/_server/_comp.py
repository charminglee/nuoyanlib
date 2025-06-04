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


import mod.server.extraServerApi as _server_api
from .._utils import CacheObject as _CacheObject


ENGINE_NAMESPACE = _server_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = _server_api.GetEngineSystemName()
LEVEL_ID = _server_api.GetLevelId()
ServerSystem = _server_api.GetServerSystemCls()
CompFactory = _server_api.GetEngineCompFactory()


class CF(_CacheObject):
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(CompFactory, "Create" + name)(self._target)


LvComp = CF(LEVEL_ID)










