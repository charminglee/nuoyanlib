# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


import mod.client.extraClientApi as c_api
from ..core.client.comp import PlrComp


__all__ = [
    "player_plunge",
]


def player_plunge(speed):
    """
    使玩家向准星方向以指定初始速度突进。

    -----

    :param float speed: 初始速度

    :return: 无
    :rtype: None
    """
    rot = PlrComp.Rot.GetRot()
    dir_rot = c_api.GetDirFromRot(rot)
    motion = tuple(map(lambda x: x * speed, dir_rot))
    PlrComp.ActorMotion.SetMotion(motion)















