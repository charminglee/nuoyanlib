# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-06
|
| ==============================================
"""


from .._core._sys import get_lib_system
from .._core._server.comp import LvComp, CF
from .._core._utils import kwargs_setter
from .._core._doc import signature
from .._core import _const
from ..utils.mc_random import random_even_poses
from ..utils.mc_math import pos_floor


__all__ = [
    "spawn_ground_shatter_effect",
]


@signature("pos, dim, r, num, block_dist=1.0, *, time=3.0, tilt_angle=22.0, min_height=0.0, max_height=0.3, in_time=0.2, out_time=0.5, in_dist=0.5, out_dist=0.5")
@kwargs_setter(
    time=3.0,
    tilt_angle=22.0,
    min_height=0.0,
    max_height=0.3,
    in_time=0.2,
    out_time=0.5,
    in_dist=0.5,
    out_dist=0.5,
)
def spawn_ground_shatter_effect(pos, dim, r, num, block_dist=1.0, **kwargs):
    """
    | 在指定位置生成裂地效果。

    -----

    :param tuple[float,float,float] pos: 生成位置
    :param int dim: 维度ID
    :param float r: 生成半径
    :param int num: 裂地方块数量
    :param float block_dist: 裂地方块之间的最小距离，默认为1.0
    :param float time: [仅关键字参数] 裂地效果持续时间，包括上浮和下沉阶段，单位为秒，默认为3.0
    :param float tilt_angle: [仅关键字参数] 裂地方块最大倾斜角度，默认为22.0
    :param float min_height: [仅关键字参数] 裂地方块最小高度，默认为0.0
    :param float max_height: [仅关键字参数] 裂地方块最大高度，默认为0.3
    :param float in_time: [仅关键字参数] 上浮阶段持续时间，默认为0.2
    :param float out_time: [仅关键字参数] 下沉阶段持续时间，默认为0.5
    :param float in_dist: [仅关键字参数] 上浮距离，默认为0.5
    :param float out_dist: [仅关键字参数] 下沉距离，默认为0.5

    :return: list[str]
    :rtype: 生成的裂地方块的实体ID列表
    """
    lib_sys = get_lib_system()
    eid_list = []
    for p in random_even_poses(pos, r, num, fixed_y=True, min_distance=block_dist):
        block = LvComp.BlockInfo.GetBlockNew(pos_floor(p), dim)
        if not block or block['name'] == "minecraft:air":
            continue
        kwargs['block'] = (block['name'], block['aux'])

        spawn_pos = (p[0], p[1] + 1.01, p[2])
        block = LvComp.BlockInfo.GetBlockNew(pos_floor(spawn_pos), dim)
        if not block or block['name'] != "minecraft:air":
            continue

        entity_id = lib_sys.CreateEngineEntityByTypeStr(
            _const.TypeStr.GROUND_SHATTER_EFFECT, spawn_pos, (0, 0), dim
        )
        if not entity_id:
            continue

        cf = CF(entity_id)
        cf.Attr.SetPersistent(False)
        cf.EntityEvent.AddActorComponent(
            "minecraft:timer",
            """{
                "looping": false,
                "time": %f,
                "time_down_event": {
                    "event": "nuoyanlib:times_up"
                }
            }""" % kwargs['time']
        )
        cf.ModAttr.SetAttr(_const.GSE_ATTR, kwargs, True)

        eid_list.append(entity_id)
    return eid_list
