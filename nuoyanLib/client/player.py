# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-02-06
#
# ====================================================


try:
    import mod.client.extraClientApi as _clientApi
except:
    pass


__all__ = [
    "player_plunge",
]


try:
    _PLAYER_ID = _clientApi.GetLocalPlayerId()
    _ClientCompFactory = _clientApi.GetEngineCompFactory()
except:
    pass


def player_plunge(playerId, speed):
    # type: (str, float) -> None
    """
    使玩家向准星方向以某一初始速度突进。
    -----------------------------------------------------------
    【playerId: str】 玩家实体ID
    【speed: float】 突进初始速度
    -----------------------------------------------------------
    NoReturn
    """
    rot = _ClientCompFactory.CreateRot(playerId).GetRot()
    dirRot = _clientApi.GetDirFromRot(rot)
    motion = tuple(map(lambda x: x * speed, dirRot))
    _ClientCompFactory.CreateActorMotion(playerId).SetMotion(motion)















