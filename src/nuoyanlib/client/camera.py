# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-5
#  ⠀
#  ================================================


import math
import mod.client.extraClientApi as c_api
from mod.common.minecraftEnum import RayFilterType
from ..core.client.comp import LvComp, PLAYER_ID, CF
from ..common.mc_math.vector import dir_from_to, vec_angle_between
from ..common.mc_math.mc_math import distance


__all__ = [
    "get_entities_within_view",
]


__global_camera_viewport_args = {
    # todo
}


def __get_viewport_args():
    # todo
    pass


def get_entities_within_view(world_dist=50, screen_dist=100, angle_dist=math.pi / 5, ent_filter=None):
    """
    获取当前屏幕内的实体。

    返回实体ID列表，按与准星的屏幕距离（screen_dist）从小到大排序。

    说明
    ----

    只有同时满足世界距离、视野角度和射线无遮挡条件的实体才会被返回。
    ``ent_filter`` 会在射线检测前调用，可用于进一步限制实体类型。

    示例
    ----

    >>> targets = nyl.get_entities_within_view(
    ...     world_dist=20,
    ...     ent_filter=lambda eid: eid != player_id,
    ... )
    >>> for target in targets:
    ...     print(target)

    参见
    ----

    - ``nuoyanlib.server.entity.get_entities_by_ray()`` -- 服务端射线实体查询接口。

    -----

    :param float world_dist: 世界中实体距离准星的最大距离，超出该距离的实体不会被获取；默认为 50
    :param float screen_dist: 屏幕上实体距离准星的最大距离，超出该距离的实体不会被获取；默认为 100
    :param float angle_dist: 实体与摄像机朝向的最大夹角，单位为弧度；默认为 math.pi / 5
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个 bool 值，返回 False 时不会返回该实体；默认为 None

    :return: 实体ID列表
    :rtype: list[str]
    """
    res = []
    all_ents = c_api.GetEngineActor().keys() + c_api.GetPlayerList()
    center = LvComp.Camera.GetPosition()
    camera_dir = LvComp.Camera.GetForward()
    for eid in all_ents:
        if eid == PLAYER_ID:
            continue
        ent_pos = CF(eid).Pos.GetFootPos()
        if not ent_pos:
            continue
        target_dir = dir_from_to(center, ent_pos)
        angle = vec_angle_between(camera_dir, target_dir)
        w_dist = distance(center, ent_pos)
        s_dist = 1 # todo
        if (
                angle < angle_dist # todo
                and w_dist <= world_dist
                and s_dist <= screen_dist
                and (ent_filter is None or ent_filter(eid))
        ):
            ray_result = c_api.getEntitiesOrBlockFromRay(
                center, target_dir, int(w_dist) + 1, False, RayFilterType.BothEntitiesAndBlock
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
















