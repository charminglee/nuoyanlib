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
#   Last Modified : 2023-09-06
#
# ====================================================


"""

sound
=====

该模块提供了与音效有关的工具。

"""


from clientComps import ClientLevelComps as _ClientLevelComps


__all__ = [
    "play_custom_sound",
    "stop_custom_sound",
]


def play_custom_sound(soundName, pos=(0, 0, 0), volume=1.0, speed=1.0, isLoop=False, entityId=None):
    """
    播放场景音效。

    -----

    :param str soundName: 音效名称
    :param tuple[float, float, float] pos: 播放位置默认为(0, 0, 0)
    :param float volume: 音量倍率，范围0-1，与json中的volume乘算后为游戏中实际播放的音量大小，默认为1.0
    :param float speed: 播放速度，范围0-256，1表示原速，可以从json文件里进行修改，默认为1.0
    :param bool isLoop: 是否循环播放，默认为False
    :param str entityId: 绑定的实体id，默认为None，若有绑定的实体，则pos参数为相对于实体的坐标

    :return: 音效ID
    :rtype: str
    """
    return _ClientLevelComps.CustomAudio.PlayCustomMusic(soundName, pos, volume, speed, isLoop, entityId)


def stop_custom_sound(soundId, fadeOutTime=0.0):
    """
    停止音效。

    -----

    :param str soundId: 音效ID
    :param float fadeOutTime: 音效淡出时间，默认为0.0

    :return: 是否成功
    :rtype: bool
    """
    return _ClientLevelComps.CustomAudio.StopCustomMusicById(soundId, fadeOutTime)




















