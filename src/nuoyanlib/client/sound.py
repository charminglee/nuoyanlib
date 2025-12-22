# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from ..core.client.comp import LvComp


__all__ = [
    "play_custom_sound",
    "stop_custom_sound",
]


def play_custom_sound(sound_name, pos=(0, 0, 0), volume=1.0, speed=1.0, is_loop=False, entity_id=None):
    """
    播放场景音效。

    -----

    :param str sound_name: 音效名称
    :param tuple[float,float,float] pos: 播放位置默认为(0, 0, 0)
    :param float volume: 音量倍率，范围0-1，与json中的volume乘算后为游戏中实际播放的音量大小；默认为1.0
    :param float speed: 播放速度，范围0-256，1表示原速，可以从json文件里进行修改；默认为1.0
    :param bool is_loop: 是否循环播放；默认为False
    :param str entity_id: 绑定的实体id；默认为None，若有绑定的实体，则pos参数为相对于实体的坐标

    :return: 音效ID
    :rtype: str
    """
    return LvComp.CustomAudio.PlayCustomMusic(sound_name, pos, volume, speed, is_loop, entity_id)


def stop_custom_sound(sound_id, fade_out_time=0.0):
    """
    停止音效。

    -----

    :param str sound_id: 音效ID
    :param float fade_out_time: 音效淡出时间；默认为0.0

    :return: 是否成功
    :rtype: bool
    """
    return LvComp.CustomAudio.StopCustomMusicById(sound_id, fade_out_time)




















