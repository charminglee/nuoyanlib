# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Email         : 1279735247@qq.com
#   Last Modified : 2023-01-13
#
# ====================================================


import mod.client.extraClientApi as _clientApi


_PLAYER_ID = _clientApi.GetLocalPlayerId()
_ClientCompFactory = _clientApi.GetEngineCompFactory()


def player_plunge(playerId, speed):
    # type: (str, float) -> None
    """
    使玩家向准星方向以某一初始速度突进。
    -----------------------------------------------------------
    【playerId: str】 玩家实体ID
    【speed: float】 突进初始速度
    -----------------------------------------------------------
    return -> None
    """
    rot = _ClientCompFactory.CreateRot(playerId).GetRot()
    dirRot = _clientApi.GetDirFromRot(rot)
    motion = tuple(map(lambda x: x * speed, dirRot))
    _ClientCompFactory.CreateActorMotion(playerId).SetMotion(motion)















