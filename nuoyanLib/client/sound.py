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


_LEVEL_ID = _clientApi.GetLevelId()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_CustomAudioComp = _ClientCompFactory.CreateCustomAudio(_LEVEL_ID)


# noinspection PyUnresolvedReferences
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
    return -> None
    """
    _CustomAudioComp.StopCustomMusicById(soundId, fadeOutTime)




















