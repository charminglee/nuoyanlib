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
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-31
#
# ====================================================


import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi
from utils import Timer as _Timer
from mod.common.minecraftEnum import EffectType as _EffectType


if _clientApi.GetLocalPlayerId() == "-1":
    _IS_CLIENT = False
    _CompFactory = _serverApi.GetEngineCompFactory()
    _LEVEL_ID = _serverApi.GetLevelId()
else:
    _IS_CLIENT = True
    _CompFactory = _clientApi.GetEngineCompFactory()
    _LEVEL_ID = _clientApi.GetLevelId()
    _PLAYER_ID = _clientApi.GetLocalPlayerId()
    _ItemComp = _CompFactory.CreateItem(_PLAYER_ID)
    _CameraComp = _CompFactory.CreateCamera(_PLAYER_ID)
_GameComp = _CompFactory.CreateGame(_LEVEL_ID)
_BlockInfoComp = _CompFactory.CreateBlockInfo(_LEVEL_ID)


_timer = None
_timer1 = None


def test_mode_server(enable):
    # type: (bool) -> None
    """
    开启或关闭测试模式（服务端调用）。
    内容包括：
    1. 显示玩家坐标；
    2. 开启终为白日、保留物品栏、立即重生、作弊；
    3. 关闭天气更替；
    4. 屏蔽饥饿度。
    -----------------------------------------------------------
    【enable: bool】 是否开启
    -----------------------------------------------------------
    return -> None
    """
    global _timer
    if _timer:
        _timer.destroy()
        _timer = None
        for p in _serverApi.GetPlayerList():
            _CompFactory.CreateGame(p).SetDisableHunger(False)
    if enable:
        @_Timer.repeat(1)
        def func():
            for _p in _serverApi.GetPlayerList():
                _CompFactory.CreateEffect(_p).AddEffectToEntity(_EffectType.NIGHT_VISION, 12, 0, False)
                _CompFactory.CreateGame(_p).SetDisableHunger(True)
        _timer = func()
    _GameComp.SetGameRulesInfoServer({
        'option_info': {
            'show_coordinates': enable,
            'immediate_respawn': enable,
        },
        'cheat_info': {
            'always_day': enable,
            'keep_inventory': enable,
            'weather_cycle': not enable,
            'enable': enable,
        },
    })


def test_mode_client(enable):
    # type: (bool) -> None
    """
    开启或关闭测试模式（客户端调用）。
    内容包括：
    1. 显示准星处生物或方块的信息；
    2. 显示手持物品信息。
    -----------------------------------------------------------
    【enable: bool】 是否开启
    -----------------------------------------------------------
    return -> None
    """
    global _timer1
    if _timer1:
        _timer1.destroy()
        _timer1 = None
    if enable:
        @_Timer.repeat(0.25)
        def func():
            carried = _ItemComp.GetCarriedItem()
            if carried:
                text = "carried: %s:%d" % (carried['newItemName'], carried['newAuxValue'])
            else:
                text = "carried: None"
            facing = _CameraComp.PickFacing()
            if facing and facing['type'] != "None":
                text += "\n" + "-" * 30
                text += "\ntype: %s" % facing['type']
                if 'entityId' in facing:
                    pos = _CompFactory.CreatePos(facing['entityId']).GetFootPos()
                    text += "\nentityId: " + facing['entityId']
                    text += "\ntypeStr: " + _CompFactory.CreateEngineType(facing['entityId']).GetEngineTypeStr()
                else:
                    pos = facing['x'], facing['y'], facing['z']
                    blockInfo = _BlockInfoComp.GetBlock(pos)
                    text += "\nblock: %s:%d" % blockInfo
                text += "\npos: (%d, %d, %d)" % pos
            _GameComp.SetTipMessage(text)
        _timer1 = func()













