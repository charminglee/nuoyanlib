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
#   Last Modified : 2025-02-03
#
# ====================================================


from math import pi as _pi
import mod.client.extraClientApi as _client_api
from mod.common.minecraftEnum import RayFilterType as _RayFilterType
from .._core._client._comp import (
    CompFactory as _CompFactory,
    PLAYER_ID as _PLAYER_ID,
    LvComp as _LvComp,
)
from ..utils.vector import (
    vec_p2p as _vec_p2p,
    vec_angle as _vec_angle,
)
from ..utils.mc_math import (
    pos_distance as _pos_distance,
)


__all__ = [
    "get_entities_within_view",
]


__global_camera_viewport_args = {
    # todo
}


def __get_viewport_args():
    # todo
    pass


def get_entities_within_view(world_dist=50, screen_dist=100, angle_dist=_pi / 5, ent_filter=None):
    """
    获取当前屏幕内的实体，返回实体ID列表，按与准星的屏幕距离（screen_dist）从小到大排序。

    -----

    :param float world_dist: 世界中实体距离准星的最大距离，超出该距离的实体不会被获取，默认为50
    :param float screen_dist: 屏幕上实体距离准星的最大距离，超出该距离的实体不会被获取，默认为100
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None

    :return: 实体ID列表
    :rtype: list[str]
    """
    res = []
    all_ents = _client_api.GetEngineActor().keys() + _client_api.GetPlayerList()
    center = _LvComp.Camera.GetPosition()
    camera_dir = _LvComp.Camera.GetForward()
    for eid in all_ents:
        if eid == _PLAYER_ID:
            continue
        ent_pos = _CompFactory.CreatePos(eid).GetFootPos()
        target_dir = _vec_p2p(center, ent_pos)
        angle = _vec_angle(camera_dir, target_dir)
        w_dist = _pos_distance(center, ent_pos)
        s_dist = 1 # todo
        if (
                angle < angle_dist # todo
                and w_dist <= world_dist
                and s_dist <= screen_dist
                and (ent_filter is None or ent_filter(eid))
        ):
            ray_result = _client_api.getEntitiesOrBlockFromRay(
                center, target_dir, int(w_dist) + 1, False, _RayFilterType.BothEntitiesAndBlock
            )
            for r in ray_result:
                if r['type'] == "Entity" and r['entityId'] == eid:
                    res.append((eid, angle))
                    break
                if r['type'] == "Block":
                    break
    res.sort(key=lambda x: x[1]) # todo: 改成按与准星的屏幕距离排序
    res = [x[0] for x in res]
    return res



















