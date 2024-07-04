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


from developer_mods.nuoyanlibDev.nuoyanlibScripts._core._server import LvComp as _LvComp


__all__ = [
    "place_large_structure",
]


def place_large_structure(pos, dimension_id, json_list, namespace):
    """
    | 放置由编辑器导出的经过切分的大型结构。放置结构时以第一个小结构为起点开始放置。

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
        result[structureName] = _LvComp.Game.PlaceStructure(
            None, placePos, structureName, dimension_id
        )
    return result


















