# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from ..core.server.comp import LvComp


__all__ = [
    "place_large_structure",
]


def place_large_structure(pos, dimension_id, json_list, namespace):
    """
    放置由编辑器导出的经过切分的大型结构。

    放置结构时以第一个小结构为起点开始放置。

    -----

    :param tuple[float,float,float] pos: 放置坐标
    :param int dimension_id: 维度ID
    :param list[dict] json_list: 使用编辑器导出结构文件时附带的json，直接将整个json复制过来即可
    :param str namespace: 结构文件所在文件夹名称

    :return: 返回结构放置结果字典，key为各个小结构的名称，value为放置结果（成功为True，失败为False）
    :rtype: dict[str, bool]
    """
    orgPos = json_list[0]['pos']
    result = {}
    for i in json_list:
        name = i['file'].split(".")[0]
        thisPos = i['pos']
        placePos = tuple(pos[p] + thisPos[p] - orgPos[p] for p in range(3))
        structureName = "%s:%s" % (namespace, name)
        result[structureName] = LvComp.Game.PlaceStructure(
            None, placePos, structureName, dimension_id
        )
    return result


















