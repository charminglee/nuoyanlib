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
#   Last Modified : 2023-02-11
#
# ====================================================


import mod.server.extraServerApi as _serverApi


_ServerCompFactory = _serverApi.GetEngineCompFactory()
_LEVEL_ID = _serverApi.GetLevelId()
_LevelGameComp = _ServerCompFactory.CreateGame(_LEVEL_ID)


def place_large_structure(self, pos, dimensionId, jsonList, namespace):
    """
    放置由编辑器导出的经过切分的大型结构。
    放置结构时以第一个小结构为起点开始放置。
    -----------------------------------------------------------
    【jsonList: List[dict]】 使用编辑器导出结构文件时附带的json内的列表
    【pos: Tuple[int, int, int]】 放置坐标
    【dimensionId: int】 维度ID
    -----------------------------------------------------------
    return: Dict[str, bool] -> 返回结构放置结果字典，key为各个小结构的名称，value为放置结果（成功为True，失败为False）
    """
    orgPos = jsonList[0]['pos']
    result = {}
    for i in jsonList:
        name = i['file'].split(".")[0]
        thisPos = i['pos']
        placePos = tuple(pos[p] + thisPos[p] - orgPos[p] for p in range(3))
        structureName = "%s:%s" % (namespace, name)
        result[structureName] = _LevelGameComp.PlaceStructure(None, placePos, structureName, dimensionId)
    return result


















