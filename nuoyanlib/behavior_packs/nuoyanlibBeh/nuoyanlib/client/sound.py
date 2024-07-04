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


from behavior_packs.nuoyanlibBeh.nuoyanlibScripts._core._client import LvComp as _LvComp


__all__ = [
    "play_custom_sound",
    "stop_custom_sound",
]


def play_custom_sound(sound_name, pos=(0.0, 0.0, 0.0), volume=1.0, speed=1.0, is_loop=False, entity_id=None):
    """
    | 播放场景音效。

    -----

    :param str sound_name: 音效名称
    :param tuple[float, float, float] pos: 播放位置默认为(0.0, 0.0, 0.0)
    :param float volume: 音量倍率，范围0-1，与json中的volume乘算后为游戏中实际播放的音量大小，默认为1.0
    :param float speed: 播放速度，范围0-256，1表示原速，可以从json文件里进行修改，默认为1.0
    :param bool is_loop: 是否循环播放，默认为False
    :param str entity_id: 绑定的实体id，默认为None，若有绑定的实体，则pos参数为相对于实体的坐标

    :return: 音效ID
    :rtype: str
    """
    return _LvComp.CustomAudio.PlayCustomMusic(sound_name, pos, volume, speed, is_loop, entity_id)


def stop_custom_sound(sound_id, fade_out_time=0.0):
    """
    | 停止音效。

    -----

    :param str sound_id: 音效ID
    :param float fade_out_time: 音效淡出时间，默认为0.0

    :return: 是否成功
    :rtype: bool
    """
    return _LvComp.CustomAudio.StopCustomMusicById(sound_id, fade_out_time)




















