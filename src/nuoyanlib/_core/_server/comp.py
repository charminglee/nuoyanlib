# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-05
|
| ==============================================
"""


import mod.server.extraServerApi as server_api
from .._utils import CachedObject


__all__ = [
    "ENGINE_NAMESPACE",
    "ENGINE_SYSTEM_NAME",
    "LEVEL_ID",
    "ServerSystem",
    "CompFactory",
    "CF",
    "LvComp",
]


ENGINE_NAMESPACE = server_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = server_api.GetEngineSystemName()
LEVEL_ID = server_api.GetLevelId()
ServerSystem = server_api.GetServerSystemCls()
CompFactory = server_api.GetEngineCompFactory()


class CF(CachedObject):
    __cache__ = {}

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        return getattr(CompFactory, "Create" + name)(self._target)


LvComp = CF(LEVEL_ID)










