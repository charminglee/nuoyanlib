# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-23
#  ⠀
# =================================================


import mod.server.extraServerApi as s_api


__all__ = [
    "ENGINE_NAMESPACE",
    "ENGINE_SYSTEM_NAME",
    "LEVEL_ID",
    "ServerSystem",
    "CompFactory",
    "CF",
    "LvComp",
]


ENGINE_NAMESPACE = s_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = s_api.GetEngineSystemName()
LEVEL_ID = s_api.GetLevelId()
ServerSystem = s_api.GetServerSystemCls()
CompFactory = s_api.GetEngineCompFactory()


class CF(object):
    _cache = {}

    def __new__(cls, target):
        if target not in cls._cache:
            cls._cache[target] = object.__new__(cls)
        return cls._cache[target]

    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        comp = getattr(CompFactory, "Create" + name)(self._target)
        if not comp:
            return
        setattr(self, name, comp)
        return comp


LvComp = CF(LEVEL_ID)
"""
使用 Level Id 创建的组件工厂。
"""


def __test__():
    assert CF("-1") is CF("-1")
    assert CF("-1") is not CF("-2")
    assert LvComp.BlockInfo is LvComp.BlockInfo


def __benchmark__(n, timer, **kwargs):
    import random
    id_pool = tuple(str(i) for i in xrange(2560))
    rand_eid = tuple(random.choice(id_pool) for _ in xrange(n))
    timer.start()
    for eid in rand_eid:
        CF(eid).Pos
    timer.end()










