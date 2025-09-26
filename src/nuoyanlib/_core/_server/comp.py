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


import mod.server.extraServerApi as server_api


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


LvComp = CF(LEVEL_ID)










