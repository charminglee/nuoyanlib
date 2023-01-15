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
#   Last Modified : 2023-01-16
#
# ====================================================


import mod.server.extraServerApi as _serverApi
from ..util.util import Timer as _Timer
from mod.common.minecraftEnum import EffectType as _EffectType


_CompFactory = _serverApi.GetEngineCompFactory()
_LEVEL_ID = _serverApi.GetLevelId()
_GameComp = _CompFactory.CreateGame(_LEVEL_ID)


_timer = None


def test_mode(enable):
    # type: (bool) -> None
    """
    开启或关闭测试模式。
    测试模式内容包括：
    1. 显示准星处生物或方块的信息；
    2. 显示玩家坐标；
    3. 开启终为白日、保留物品栏、立即重生、作弊；
    4. 关闭天气更替；
    5. 屏蔽饥饿度。
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
                _CompFactory.CreateEffect(_p).AddEffectToEntity(_EffectType.NIGHT_VISION, 2, 0, False)
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












