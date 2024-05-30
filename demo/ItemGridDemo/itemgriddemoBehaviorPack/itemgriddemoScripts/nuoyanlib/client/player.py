# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-31
#
# ====================================================


import mod.client.extraClientApi as api
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
    dir_rot = api.GetDirFromRot(rot)
    motion = tuple(map(lambda x: x * speed, dir_rot))
    _PlrComp.ActorMotion.SetMotion(motion)















