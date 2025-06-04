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
from .._core._client._comp import PlrComp as _PlrComp


__all__ = [
    "player_plunge",
]


def player_plunge(speed):
    """
    | 使玩家向准星方向以指定初始速度突进。

    -----

    :param float speed: 初始速度

    :return: 无
    :rtype: None
    """
    rot = _PlrComp.Rot.GetRot()
    dir_rot = _client_api.GetDirFromRot(rot)
    motion = tuple(map(lambda x: x * speed, dir_rot))
    _PlrComp.ActorMotion.SetMotion(motion)















