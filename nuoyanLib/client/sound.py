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
#   Last Modified : 2023-02-06
#
# ====================================================


try:
    import mod.client.extraClientApi as _clientApi
except:
    pass


__all__ = [
    "play_custom_sound",
    "stop_custom_sound",
]


try:
    _LEVEL_ID = _clientApi.GetLevelId()
    _ClientCompFactory = _clientApi.GetEngineCompFactory()
    _CustomAudioComp = _ClientCompFactory.CreateCustomAudio(_LEVEL_ID)
except:
    pass


def play_custom_sound(soundName, pos=(0, 0, 0), volume=1.0, speed=1.0, isLoop=False, entityId=None):
    # type: (str, tuple[float, float, float], float, float, bool, str | None) -> str
    """
    播放场景音效。
    -----------------------------------------------------------
    【soundName: str】 音效名称
    【pos: Tuple[float, float, float] = (0, 0, 0)】 播放位置
    【volume: float = 1.0】 音量倍率，范围0-1，与json中的volume乘算后为游戏中实际播放的音量大小
    【speed: float = 1.0】 播放速度，范围0-256，1表示原速，可以从json文件里进行修改
    【isLoop: bool = False】 是否循环播放
    【entityId: Optional[str] = None】 绑定的实体id，默认为None，若有绑定的实体，则pos参数为相对于实体的坐标
    -----------------------------------------------------------
    return: str -> 音效ID
    """
    return _CustomAudioComp.PlayCustomMusic(soundName, pos, volume, speed, isLoop, entityId)


def stop_custom_sound(soundId, fadeOutTime):
    # type: (str, float) -> None
    """
    停止音效。
    -----------------------------------------------------------
    【soundId: str】 音效ID
    【fadeOutTime: float】 音效淡出时间
    -----------------------------------------------------------
    NoReturn
    """
    _CustomAudioComp.StopCustomMusicById(soundId, fadeOutTime)




















