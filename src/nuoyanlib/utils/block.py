# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-28
#  ⠀
# =================================================


from ..core._utils import inject_is_client
from ..core._sys import get_lv_comp


if 0:
    is_air = lambda *_, **__: UNIVERSAL_OBJECT


__all__ = [
    "is_air",
]


_AIR_BLOCKS = {
    "minecraft:air",
    "minecraft:light_block_0",
    "minecraft:light_block_1",
    "minecraft:light_block_2",
    "minecraft:light_block_3",
    "minecraft:light_block_4",
    "minecraft:light_block_5",
    "minecraft:light_block_6",
    "minecraft:light_block_7",
    "minecraft:light_block_8",
    "minecraft:light_block_9",
    "minecraft:light_block_10",
    "minecraft:light_block_11",
    "minecraft:light_block_12",
    "minecraft:light_block_13",
    "minecraft:light_block_14",
    "minecraft:light_block_15",
    "minecraft:structure_void",
}


@inject_is_client
def is_air(__is_client__, pos, dim=None):
    """
    判断指定位置的方块是否为空气方块。

    以下方块视为空气方块：

    - ``minecraft:air`` -- 空气
    - ``minecraft:light_block_0`` -- 光源方块（亮度 0）
    - ``minecraft:light_block_1`` -- 光源方块（亮度 1）
    - ``minecraft:light_block_2`` -- 光源方块（亮度 2）
    - ``minecraft:light_block_3`` -- 光源方块（亮度 3）
    - ``minecraft:light_block_4`` -- 光源方块（亮度 4）
    - ``minecraft:light_block_5`` -- 光源方块（亮度 5）
    - ``minecraft:light_block_6`` -- 光源方块（亮度 6）
    - ``minecraft:light_block_7`` -- 光源方块（亮度 7）
    - ``minecraft:light_block_8`` -- 光源方块（亮度 8）
    - ``minecraft:light_block_9`` -- 光源方块（亮度 9）
    - ``minecraft:light_block_10`` -- 光源方块（亮度 10）
    - ``minecraft:light_block_11`` -- 光源方块（亮度 11）
    - ``minecraft:light_block_12`` -- 光源方块（亮度 12）
    - ``minecraft:light_block_13`` -- 光源方块（亮度 13）
    - ``minecraft:light_block_14`` -- 光源方块（亮度 14）
    - ``minecraft:light_block_15`` -- 光源方块（亮度 15）
    - ``minecraft:structure_void`` -- 结构空位

    -----

    :param tuple[int,int,int] pos: 坐标
    :param int|None dim: 维度ID，客户端调用时可忽略该参数

    :return:
    """
    if __is_client__:
        block = get_lv_comp().BlockInfo.GetBlock(pos)
        if block:
            block = block[0]
    else:
        block = get_lv_comp().BlockInfo.GetBlockNew(pos, dim)
        if block:
            block = block['name']
    return block and block in _AIR_BLOCKS













