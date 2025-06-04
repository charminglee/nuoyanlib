# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Dict, List, Tuple
from .._listener import EventArgsProxy


class EventArgs0(EventArgsProxy):
    changedList: Tuple[dict]
    """
    修改后的按钮列表
    """

class EventArgs1(EventArgsProxy):
    blockPos: Tuple[float, float, float]
    """
    方块坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """

class EventArgs2(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    victimId: str
    """
    受击者的实体ID
    """
    damage: float
    """
    客户端收到的是真实伤害值，且修改无效
    """
    isCrit: bool
    """
    本次攻击是否产生暴击，不支持修改
    """

class EventArgs3(EventArgsProxy):
    actionType: int
    """
    动作事件枚举，详见Minecraft枚举值文档的 `PlayerActionType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerActionType.html>`_
    """

class EventArgs4(EventArgsProxy):
    pass

class EventArgs5(EventArgsProxy):
    pass

class EventArgs6(EventArgsProxy):
    xDiff: float
    """
    x轴角速度，单位为弧度/s
    """
    yDiff: float
    """
    y轴角速度，单位为弧度/s
    """
    zDiff: float
    """
    z轴角速度，单位为弧度/s
    """
    orientation: int
    """
    当前屏幕朝向，0竖屏正向，1横屏向左，2竖屏倒置，3横屏向右
    """
    timestamp: float
    """
    触发时间戳，秒
    """

class EventArgs7(EventArgsProxy):
    posX: int
    """
    自定义方块实体的位置X
    """
    posY: int
    """
    自定义方块实体的位置Y
    """
    posZ: int
    """
    自定义方块实体的位置Z
    """
    dimensionId: int
    """
    维度ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """

class EventArgs8(EventArgsProxy):
    posX: int
    """
    自定义方块实体的位置X
    """
    posY: int
    """
    自定义方块实体的位置Y
    """
    posZ: int
    """
    自定义方块实体的位置Z
    """
    dimensionId: int
    """
    维度ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """

class EventArgs9(EventArgsProxy):
    oldPosition: Tuple[float, float]
    """
    移动前该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
    """
    newPosition: Tuple[float, float]
    """
    移动后该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
    """

class EventArgs10(EventArgsProxy):
    action: str
    """
    行为
    """
    newKey: int
    """
    修改后的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
    """
    oldKey: int
    """
    修改前的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
    """

class EventArgs11(EventArgsProxy):
    action: str
    """
    行为
    """
    newKey: int
    """
    修改后的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
    """
    oldKey: int
    """
    修改前的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
    """

class EventArgs12(EventArgsProxy):
    key: int
    """
    键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
    """
    magnitude: float
    """
    扣动扳机的力度，取值为 0 ~ 1.0
    """

class EventArgs13(EventArgsProxy):
    key: int
    """
    键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
    """
    x: float
    """
    摇杆水平方向的值，从左到右取值为 -1.0 ~ 1.0
    """
    y: float
    """
    摇杆竖直方向的值，从下到上取值为 -1.0 ~ 1.0
    """

class EventArgs14(EventArgsProxy):
    screenName: str
    """
    当前screenName
    """
    key: int
    """
    键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
    """
    isDown: str
    """
    是否按下，按下为1，弹起为0
    """

class EventArgs15(EventArgsProxy):
    posX: int
    """
    自定义方块实体的位置X
    """
    posY: int
    """
    自定义方块实体的位置Y
    """
    posZ: int
    """
    自定义方块实体的位置Z
    """
    dimensionId: int
    """
    维度ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """

class EventArgs16(EventArgsProxy):
    pass

class EventArgs17(EventArgsProxy):
    screenName: str
    """
    UI名字
    """
    screenDef: str
    """
    包含命名空间的UI名字，格式为namespace.screenName
    """

class EventArgs18(EventArgsProxy):
    pass

class EventArgs19(EventArgsProxy):
    cancel: bool
    """
    设置为True可拦截原版的攻击或放置响应
    """

class EventArgs20(EventArgsProxy):
    pass

class EventArgs21(EventArgsProxy):
    cancel: bool
    """
    设置为True可拦截原版的物品使用/实体交互响应
    """

class EventArgs22(EventArgsProxy):
    isDown: str
    """
    是否按下，按下为1，弹起为0
    """
    mousePositionX: float
    """
    按下时的x坐标
    """
    mousePositionY: float
    """
    按下时的y坐标
    """

class EventArgs23(EventArgsProxy):
    screenName: str
    """
    当前screenName
    """
    key: str
    """
    键码（注：这里的int型被转成了str型，比如"1"对应的就是枚举值文档中的1），详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
    """
    isDown: str
    """
    是否按下，按下为1，弹起为0
    """

class EventArgs24(EventArgsProxy):
    pass

class EventArgs25(EventArgsProxy):
    pass

class EventArgs26(EventArgsProxy):
    pass

class EventArgs27(EventArgsProxy):
    direction: int
    """
    1为向上滚动，0为向下滚动
    """

class EventArgs28(EventArgsProxy):
    pass

class EventArgs29(EventArgsProxy):
    cancel: bool
    """
    设置为True可拦截原版的挖方块或攻击响应
    """

class EventArgs30(EventArgsProxy):
    cancel: bool
    """
    设置为True可拦截原版的挖方块/使用物品/与实体交互响应
    """

class EventArgs31(EventArgsProxy):
    x: int
    """
    手指点击位置x坐标
    """
    y: int
    """
    手指点击位置y坐标
    """

class EventArgs32(EventArgsProxy):
    pass

class EventArgs33(EventArgsProxy):
    pass

class EventArgs34(EventArgsProxy):
    continueJump: bool
    """
    设置是否执行跳跃逻辑
    """

class EventArgs35(EventArgsProxy):
    name: str
    """
    即资源包中sounds/sound_definitions.json中的key
    """
    pos: Tuple[float, float, float]
    """
    音效播放的位置，UI音效为(0,0,0)
    """
    volume: float
    """
    音量，范围为0-1
    """
    pitch: float
    """
    播放速度，正常速度为1
    """
    cancel: bool
    """
    设为True可屏蔽该次音效播放
    """

class EventArgs36(EventArgsProxy):
    name: str
    """
    即资源包中sounds/music_definitions.json中的event_name，并且对应sounds/sound_definitions.json中的key
    """
    cancel: bool
    """
    设为True可屏蔽该次音效播放
    """

class EventArgs37(EventArgsProxy):
    musicName: str
    """
    音乐名称
    """

class EventArgs38(EventArgsProxy):
    beforeX: float
    """
    屏幕大小改变前的宽度
    """
    beforeY: float
    """
    屏幕大小改变前的高度
    """
    afterX: float
    """
    屏幕大小改变后的宽度
    """
    afterY: float
    """
    屏幕大小改变后的高度
    """

class EventArgs39(EventArgsProxy):
    screenName: str
    """
    UI名字
    """
    screenDef: str
    """
    包含命名空间的UI名字，格式为namespace.screenName
    """

class EventArgs40(EventArgsProxy):
    screenName: str
    """
    UI名字
    """
    screenDef: str
    """
    包含命名空间的UI名字，格式为"namespace.screenName"
    """

class EventArgs41(EventArgsProxy):
    pass

class EventArgs42(EventArgsProxy):
    slotIndex: int
    """
    点击的物品槽的编号，编号对应位置详见 `物品栏 <https://minecraft.fandom.com/zh/wiki/%E7%89%A9%E5%93%81%E6%A0%8F>`_
    """

class EventArgs43(EventArgsProxy):
    path: str
    """
    grid网格所在的路径（从UI根节点算起）
    """

class EventArgs44(EventArgsProxy):
    isCreative: bool
    """
    是否是创造模式背包界面
    """
    cancel: bool
    """
    是否取消打开物品背包界面。
    """

class EventArgs45(EventArgsProxy):
    pass

class EventArgs46(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    x: int
    """
    箱子x坐标
    """
    y: int
    """
    箱子y坐标
    """
    z: int
    """
    箱子z坐标
    """

class EventArgs47(EventArgsProxy):
    pass

class EventArgs48(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs49(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs50(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs51(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs52(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs53(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs54(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
    `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    是否取消此次操作
    """

class EventArgs55(EventArgsProxy):
    itemDict: dict | None
    """
    切换后的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs56(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    durationLeft: float
    """
    蓄力剩余时间（当物品缺少"minecraft:maxduration"组件时，蓄力剩余时间为负数）
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    maxUseDuration: int
    """
    最大蓄力时长
    """
    cancel: bool
    """
    设置为True可以取消，需要同时取消服务端事件ItemReleaseUsingServerEvent
    """

class EventArgs57(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    slot: int
    """
    背包槽位
    """
    oldItemDict: dict | None
    """
    变化前槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    newItemDict: dict | None
    """
    变化后槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs58(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    oldItemDict: dict
    """
    合成前的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第一个物品）
    """
    additionalItemDict: dict
    """
    作为合成材料的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第二个物品）
    """
    newItemDict: dict
    """
    合成后的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    exp: int
    """
    本次合成返还的经验
    """

class EventArgs59(EventArgsProxy):
    recipeId: str
    """
    配方ID，对应配方json文件中的identifier字段
    """

class EventArgs60(EventArgsProxy):
    entityId: str
    """
    玩家实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    blockAuxValue: int
    """
    方块的附加值
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """
    ret: bool
    """
    设为True可取消物品的使用
    """

class EventArgs61(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    是否取消使用物品
    """

class EventArgs62(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemShowName: str
    """
    合成后的物品显示名称
    """
    itemDict: dict
    """
    合成后的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    oldItemDict: dict
    """
    合成前的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第一个物品）
    """
    materialItemDict: dict
    """
    合成所使用材料的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第二个物品）
    """

class EventArgs63(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    useMethod: int
    """
    使用物品的方法，详见 `ItemUseMethodEnum枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemUseMethodEnum.html?key=ItemUseMethodEnum&docindex=1&type=0>`_
    """

class EventArgs64(EventArgsProxy):
    actor: str
    """
    获得物品玩家实体ID
    """
    secondaryActor: str
    """
    物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
    """
    itemDict: dict
    """
    获取到的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    acquireMethod: int
    """
    获得物品的方法，详见 `ItemAcquisitionMethod <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemAcquisitionMethod.html?key=ItemAcquisitionMethod&docindex=1&type=0>`_
    """

class EventArgs65(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续原版逻辑
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    entityId: str
    """
    实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs66(EventArgsProxy):
    pos: Tuple[float, float, float]
    """
    方块的坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    playerId: str
    """
    玩家的实体ID
    """
    cancel: bool
    """
    修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockServerEvent一起修改。
    """
    face: int
    """
    方块被敲击面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html>`_
    """

class EventArgs67(EventArgsProxy):
    blockX: int
    """
    方块位置x
    """
    blockY: int
    """
    方块位置y
    """
    blockZ: int
    """
    方块位置z
    """
    entityId: str
    """
    实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs68(EventArgsProxy):
    blockX: int
    """
    方块位置x
    """
    blockY: int
    """
    方块位置y
    """
    blockZ: int
    """
    方块位置z
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    dropName: str
    """
    触发剪刀效果的掉落物identifier，包含命名空间及名称
    """
    dropCount: int
    """
    触发剪刀效果的掉落物数量
    """
    playerId: str
    """
    触发剪刀效果的玩家实体ID
    """
    dimensionId: int
    """
    玩家触发时的维度ID
    """
    cancelShears: bool
    """
    是否取消剪刀效果
    """

class EventArgs69(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    face: int
    """
    方块被敲击的面向ID，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    playerId: str
    """
    试图破坏方块的玩家的实体ID
    """
    cancel: bool
    """
    默认为False，在脚本层设置为True就能取消该方块的破坏
    """

class EventArgs70(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    dimensionId: int
    """
    实体所在维度ID
    """
    posX: float
    """
    实体位置x
    """
    posY: float
    """
    实体位置y
    """
    posZ: float
    """
    实体位置z
    """
    motionX: float
    """
    瞬时移动x方向的力
    """
    motionY: float
    """
    瞬时移动y方向的力
    """
    motionZ: float
    """
    瞬时移动z方向的力
    """
    blockX: int
    """
    方块位置x
    """
    blockY: int
    """
    方块位置y
    """
    blockZ: int
    """
    方块位置z
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    cancel: bool
    """
    可由脚本层回传True给引擎，阻止触发后续原版逻辑
    """

class EventArgs71(EventArgsProxy):
    effectName: str
    """
    创建成功的特效的自定义键值名称
    """
    id: int
    """
    该特效的ID
    """
    effectType: int
    """
    该特效的类型，0为粒子特效，1为序列帧特效
    """
    blockPos: Tuple[float, float, float]
    """
    该特效绑定的自定义方块实体的世界坐标
    """

class EventArgs72(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    dimensionId: int
    """
    实体所在维度ID
    """
    slowdownMultiX: float
    """
    实体移速x方向的减速比例
    """
    slowdownMultiY: float
    """
    实体移速y方向的减速比例
    """
    slowdownMultiZ: float
    """
    实体移速z方向的减速比例
    """
    blockX: int
    """
    方块位置x
    """
    blockY: int
    """
    方块位置y
    """
    blockZ: int
    """
    方块位置z
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    cancel: bool
    """
    可由脚本层回传True给引擎，阻止触发后续原版逻辑
    """

class EventArgs73(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    posX: float
    """
    实体位置x
    """
    posY: float
    """
    实体位置y
    """
    posZ: float
    """
    实体位置z
    """
    motionX: float
    """
    瞬时移动x方向的力
    """
    motionY: float
    """
    瞬时移动y方向的力
    """
    motionZ: float
    """
    瞬时移动z方向的力
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    calculate: bool
    """
    是否按脚本层传值计算力
    """

class EventArgs74(EventArgsProxy):
    fallingBlockId: str
    """
    下落的方块实体ID
    """
    fallingBlockX: float
    """
    下落的方块实体位置x
    """
    fallingBlockY: float
    """
    下落的方块实体位置y
    """
    fallingBlockZ: float
    """
    下落的方块实体位置z
    """
    blockName: str
    """
    重力方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    下落的方块实体维度ID
    """
    collidingEntitys: List[str] | None
    """
    当前碰撞到的实体ID列表（客户端只能获取到玩家），如果没有的话是None
    """
    fallTickAmount: int
    """
    下落的方块实体持续下落了多少tick
    """
    fallDistance: float
    """
    下落的方块实体持续下落了多少距离
    """
    isHarmful: bool
    """
    客户端始终为false，因为客户端不会计算伤害值
    """
    fallDamage: int
    """
    对实体的伤害
    """

class EventArgs75(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    aux: int
    """
    方块附加值
    """
    cancel: bool
    """
    设置为True可拦截与方块交互的逻辑
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """

class EventArgs76(EventArgsProxy):
    from: int
    """
    切换前的视角
    """
    to: int
    """
    切换后的视角
    """

class EventArgs77(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    posX: int
    """
    碰撞方块x坐标
    """
    posY: int
    """
    碰撞方块y坐标
    """
    posZ: int
    """
    碰撞方块z坐标
    """
    blockId: str
    """
    碰撞方块的identifier
    """
    auxValue: int
    """
    碰撞方块的附加值
    """

class EventArgs78(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    oldGameType: int
    """
    切换前的游戏模式
    """
    newGameType: int
    """
    切换后的游戏模式
    """

class EventArgs79(EventArgsProxy):
    pos: Tuple[float, float, float]
    """
    火焰方块的坐标
    """
    playerId: str
    """
    玩家的实体ID
    """
    cancel: bool
    """
    修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireServerEvent一起修改。
    """

class EventArgs80(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    fromDimensionId: int
    """
    维度改变前的维度
    """
    toDimensionId: int
    """
    维度改变后的维度
    """
    toPos: Tuple[float, float, float]
    """
    改变后的位置(x,y,z)，其中y值为脚底加上角色的身高值
    """

class EventArgs81(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    fromDimensionId: int
    """
    维度改变前的维度
    """
    toDimensionId: int
    """
    维度改变后的维度
    """
    fromX: float
    """
    改变前的位置x
    """
    fromY: float
    """
    改变前的位置y
    """
    fromZ: float
    """
    改变前的位置z
    """
    toX: float
    """
    改变后的位置x
    """
    toY: float
    """
    改变后的位置y
    """
    toZ: float
    """
    改变后的位置z
    """

class EventArgs82(EventArgsProxy):
    motionId: int
    """
    运动器ID
    """
    remove: bool
    """
    是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除
    """

class EventArgs83(EventArgsProxy):
    motionId: int
    """
    运动器ID
    """

class EventArgs84(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    entityId: str
    """
    远离的生物的实体ID
    """

class EventArgs85(EventArgsProxy):
    actorId: str
    """
    骑乘者的实体ID
    """
    victimId: str
    """
    被骑乘者的实体ID
    """

class EventArgs86(EventArgsProxy):
    mobId: str
    """
    当前生物的实体ID
    """
    hittedMobList: List[str]
    """
    当前生物碰撞到的其他所有生物的实体ID的list
    """

class EventArgs87(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs88(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    from: float
    """
    变化前的生命值
    """
    to: float
    """
    变化后的生命值
    """

class EventArgs89(EventArgsProxy):
    id: str
    """
    实体ID
    """
    rideId: str
    """
    坐骑的实体ID
    """
    exitFromRider: bool
    """
    是否下坐骑
    """
    entityIsBeingDestroyed: bool
    """
    坐骑是否将要销毁
    """
    switchingRides: bool
    """
    是否换乘坐骑
    """
    cancel: bool
    """
    设置为True可以取消（需要与服务端事件一同取消）
    """

class EventArgs90(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    newModel: str
    """
    新的模型名字
    """
    oldModel: str
    """
    旧的模型名字
    """

class EventArgs91(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    entityId: str
    """
    靠近的生物的实体ID
    """

class EventArgs92(EventArgsProxy):
    pass

class EventArgs93(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs94(EventArgsProxy):
    id: str
    """
    移除的实体ID
    """

class EventArgs95(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs96(EventArgsProxy):
    command: str
    """
    命令名称
    """
    message: str
    """
    命令返回的消息
    """

class EventArgs97(EventArgsProxy):
    pass

class EventArgs98(EventArgsProxy):
    dimension: int
    """
    区块所在维度
    """
    chunkPosX: int
    """
    区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
    """
    chunkPosZ: int
    """
    区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
    """

class EventArgs99(EventArgsProxy):
    dimension: int
    """
    区块所在维度
    """
    chunkPosX: int
    """
    区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
    """
    chunkPosZ: int
    """
    区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
    """

class EventArgs100(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs101(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs102(EventArgsProxy):
    id: str
    """
    实体ID
    """
    posX: float
    """
    位置x
    """
    posY: float
    """
    位置y
    """
    posZ: float
    """
    位置z
    """
    dimensionId: int
    """
    实体维度
    """
    isBaby: bool
    """
    是否为幼儿
    """
    engineTypeStr: str
    """
    实体类型
    """
    itemName: str
    """
    物品identifier（仅当物品实体时存在该字段）
    """
    auxValue: int
    """
    物品附加值（仅当物品实体时存在该字段）
    """

class EventArgs103(EventArgsProxy):
    pass

class EventArgs104(EventArgsProxy):
    pass

class EventArgs105(EventArgsProxy):
    itemDict: dict
    """
    尝试放入物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    collectionName: str
    """
    放入容器名称，目前仅支持netease_container和netease_ui_container
    """
    collectionIndex: int
    """
    放入容器索引
    """
    playerId: str
    """
    玩家实体ID
    """
    x: float
    """
    容器方块x坐标
    """
    y: float
    """
    容器方块y坐标
    """
    z: float
    """
    容器方块z坐标
    """
    cancel: bool
    """
    是否取消该操作，默认为False，事件中改为True时拒绝此次放入自定义容器的操作
    """

class EventArgs106(EventArgsProxy):
    eid: str
    """
    生物实体ID
    """
    pid: str
    """
    玩家实体ID
    """

class EventArgs107(EventArgsProxy):
    playerId: str
    """
    玩家实体ID
    """
    actionType: int
    """
    动作事件枚举，详见Minecraft枚举值文档的 `PlayerActionType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerActionType.html>`_
    """

class EventArgs108(EventArgsProxy):
    command: str
    """
    自定义命令名称，对应json中的name字段
    """
    args: List[dict]
    """
    自定义命令参数，详情见上方
    """
    variant: int
    """
    表示是哪条变体，范围[0, 9]，对应json中args键中的数字，未配置变体则为0
    """
    origin: dict
    """
    触发源的信息，详情见上方
    """
    return_failed: bool
    """
    设置自定义命令是否执行失败，默认为False，如果执行失败，返回信息以红色字体显示
    """
    return_msg_key: str
    """
    设置返回给玩家或命令方块的信息，支持在语言文件（.lang）中定义，默认值为commands.custom.success（自定义命令执行成功）
    """

class EventArgs109(EventArgsProxy):
    entityId: str
    """
    执行命令的实体ID，命令方块执行时没有该参数
    """
    command: str
    """
    命令
    """
    blockPos: Tuple[int, int, int]
    """
    执行命令的实体或方块的方块坐标
    """
    dimension: int
    """
    执行命令的实体或方块所在维度ID
    """
    cancel: bool
    """
    设置为True可以取消命令执行
    """

class EventArgs110(EventArgsProxy):
    playerId: str
    """
    玩家实体ID
    """
    arrowId: str
    """
    抛射物实体ID
    """
    itemDict: dict
    """
    触碰的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    设置为True时将取消本次拾取
    """
    pickupDelay: int
    """
    取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取，每秒30帧
    """

class EventArgs111(EventArgsProxy):
    dieEntityId: str
    """
    死亡实体ID
    """
    attacker: str
    """
    伤害来源实体ID
    """
    itemList: List[dict]
    """
    掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    itemEntityIdList: List[str]
    """
    掉落物品的实体ID列表
    """

class EventArgs112(EventArgsProxy):
    playerId: str
    """
    玩家实体ID
    """
    hungerBefore: float
    """
    变化前的饥饿度
    """
    hunger: float
    """
    变化后的饥饿度
    """
    cancel: bool
    """
    是否取消饥饿度变化
    """

class EventArgs113(EventArgsProxy):
    entityId: str
    """
    物品拥有者的实体ID
    """
    itemDict: dict
    """
    物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    durabilityBefore: int
    """
    变化前耐久度
    """
    durability: int
    """
    变化后耐久度，支持修改。但是请注意修改范围，支持范围为[-32768,32767)
    """
    canChange: bool
    """
    是否支持修改，为True时支持通过durability修改，为False时不支持
    """

class EventArgs114(EventArgsProxy):
    dimensionId: int
    """
    维度ID
    """
    pos: Tuple[int, int]
    """
    中心结构放置坐标(x, z)
    """
    rot: int
    """
    中心结构顺时针旋转角度
    """
    depth: int
    """
    大型结构递归深度
    """
    centerPool: str
    """
    中心池的identifier
    """
    ignoreFitInContext: bool
    """
    是否允许生成过结构的地方继续生成结构
    """
    cancel: bool
    """
    设置为True时可阻止该大型结构的放置
    """

class EventArgs115(EventArgsProxy):
    playerId: str
    """
    主动命名生物的玩家的实体ID
    """
    entityId: str
    """
    被命名生物的实体ID
    """
    preName: str
    """
    实体当前的名字
    """
    afterName: str
    """
    实体重命名后的名字
    """
    cancel: bool
    """
    是否取消触发，默认为False，若设为True，可阻止触发后续的实体命名逻辑
    """

class EventArgs116(EventArgsProxy):
    playerId: str
    """
    主动喂养生物的玩家的实体ID
    """
    entityId: str
    """
    被喂养生物的实体ID
    """
    itemDict: dict
    """
    当前玩家手持物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    是否取消触发，默认为False，若设为True，可阻止触发后续的生物喂养逻辑
    """

class EventArgs117(EventArgsProxy):
    eid: str
    """
    玩家的实体ID
    """
    buyItem: bool
    """
    玩家登录时为False，玩家购买了商品时为True
    """

class EventArgs118(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs119(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    isCreative: str
    """
    是否是创造模式背包界面
    """

class EventArgs120(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs121(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs122(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs123(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs124(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs125(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    slot: int
    """
    容器槽位，含义见： `PlayerUISlot枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerUISlot.html?key=PlayerUISlot&docindex=1&type=0>`_
    """
    oldItemDict: dict
    """
    旧 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    newItemDict: dict
    """
    生成的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs126(EventArgsProxy):
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: str
    """
    方块附加值
    """
    dropName: str
    """
    触发剪刀效果的掉落物identifier，包含命名空间及名称
    """
    dropCount: str
    """
    触发剪刀效果的掉落物数量
    """
    entityId: str
    """
    触发剪刀效果的实体ID，目前仅玩家会触发
    """
    dimensionId: int
    """
    维度ID
    """
    cancelShears: int
    """
    是否取消剪刀效果
    """

class EventArgs127(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    entityId: str
    """
    物品的实体ID
    """
    itemDict: dict
    """
    `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    设置为True时将取消本次拾取
    """
    pickupDelay: int
    """
    取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取
    """

class EventArgs128(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancel: bool
    """
    设为True可取消物品的使用
    """

class EventArgs129(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemEntityId: str
    """
    物品的实体ID
    """

class EventArgs130(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    sourceId: str
    """
    伤害来源实体ID，没有实体返回"-1"
    """
    itemDict: dict
    """
    盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    damage: float
    """
    抵挡的伤害数值
    """

class EventArgs131(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    sourceId: str
    """
    伤害来源实体ID，没有实体返回"-1"
    """
    itemDict: dict
    """
    盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    damage: float
    """
    抵挡的伤害数值
    """

class EventArgs132(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    isActive: str
    """
    True:尝试激活，False:尝试取消激活
    """
    itemDict: dict
    """
    盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    cancelable: bool
    """
    是否可以取消。如果玩家在潜行状态切换盾牌，则无法取消
    """
    cancel: bool
    """
    是否取消这次激活
    """

class EventArgs133(EventArgsProxy):
    oldArmorDict: dict | None
    """
    旧物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧物品为空时，此项属性为None
    """
    newArmorDict: dict | None
    """
    新物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新物品为空时，此项属性为None
    """
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs134(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    slot: int
    """
    槽位ID
    """
    oldArmorDict: dict | None
    """
    旧装备的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧装备为空时，此项属性为None
    """
    newArmorDict: dict | None
    """
    新装备的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新装备为空时，此项属性为None
    """

class EventArgs135(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    slotType: int
    """
    玩家放入物品的EnchantSlotType
    """
    options: List[dict]
    """
    附魔台选项
    """
    change: bool
    """
    传入True时，附魔台选项会被新传入的options覆盖
    """

class EventArgs136(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    blockAuxValue: int
    """
    方块的附加值
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs137(EventArgsProxy):
    entityId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs138(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    durationLeft: float
    """
    蓄力剩余时间(当物品缺少"minecraft:maxduration"组件时,蓄力剩余时间为负数)
    """
    itemDict: dict
    """
    使用的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    maxUseDuration: int
    """
    最大蓄力时长
    """
    cancel: bool
    """
    设置为True可以取消，需要同时取消客户端事件ItemReleaseUsingClientEvent
    """
    changeItem: bool
    """
    如果要在该事件的回调中修改当前使用槽位的物品，需设置这个参数为True，否则将修改物品失败，例如修改耐久度或者替换成新物品
    """

class EventArgs139(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    slot: int
    """
    背包槽位
    """
    oldItemDict: dict | None
    """
    变化前的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    newItemDict: dict | None
    """
    变化后的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs140(EventArgsProxy):
    dimensionId: int
    """
    维度ID
    """
    posX: float
    """
    位置x
    """
    posY: float
    """
    位置y
    """
    posZ: float
    """
    位置z
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs141(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
    `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    screenContainerType: int
    """
    当前界面类型，类型含义见： `ContainerType枚举枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ContainerType.html?key=ContainerType&docindex=1&type=0>`_
    """
    cancel: bool
    """
    是否取消生成物品
    """

class EventArgs142(EventArgsProxy):
    pos: Tuple[int, int, int]
    """
    容器坐标
    """
    containerType: int
    """
    容器类型，类型含义见： `ContainerType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ContainerType.html?key=ContainerType&docindex=1&type=0>`_
    """
    slot: int
    """
    容器槽位
    """
    dimensionId: int
    """
    维度ID
    """
    oldItemDict: dict | None
    """
    旧 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    newItemDict: dict | None
    """
    新 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """

class EventArgs143(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    entityId: str
    """
    实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs144(EventArgsProxy):
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    entityId: str
    """
    实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs145(EventArgsProxy):
    pos: Tuple[float, float, float]
    """
    方块坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    playerId: str
    """
    玩家的实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    cancel: bool
    """
    修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockClientEvent一起修改
    """
    face: int
    """
    方块被敲击面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html>`_
    """

class EventArgs146(EventArgsProxy):
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    dropName: str
    """
    触发剪刀效果的掉落物identifier，包含命名空间及名称
    """
    dropCount: int
    """
    触发剪刀效果的掉落物数量
    """
    playerId: str
    """
    玩家的实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    cancelShears: bool
    """
    是否取消剪刀效果
    """

class EventArgs147(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    face: int
    """
    方块被敲击的面向id，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    playerId: str
    """
    试图破坏方块的玩家的实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    cancel: bool
    """
    默认为False，在脚本层设置为True就能取消该方块的破坏
    """
    spawnResources: bool
    """
    是否生成掉落物，默认为True，在脚本层设置为False就能取消生成掉落物
    """

class EventArgs148(EventArgsProxy):
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimension: int
    """
    维度ID
    """
    posX: int
    """
    方块x坐标
    """
    posY: int
    """
    方块y坐标
    """
    posZ: int
    """
    方块z坐标
    """

class EventArgs149(EventArgsProxy):
    x: int
    """
    方块x坐标，支持修改
    """
    y: int
    """
    方块y坐标，支持修改
    """
    z: int
    """
    方块z坐标，支持修改
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称，支持修改
    """
    auxData: int
    """
    方块附加值，支持修改
    """
    entityId: str
    """
    试图放置方块的生物的实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    cancel: bool
    """
    默认为False，在脚本层设置为True就能取消该方块的放置
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """

class EventArgs150(EventArgsProxy):
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimension: int
    """
    维度ID
    """
    posX: int
    """
    方块x坐标
    """
    posY: int
    """
    方块y坐标
    """
    posZ: int
    """
    方块z坐标
    """

class EventArgs151(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续的事件
    """
    action: str
    """
    推送时=expanding；缩回时=retracting
    """
    pistonFacing: int
    """
    活塞的朝向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    pistonMoveFacing: int
    """
    活塞的运动方向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    dimensionId: int
    """
    维度ID
    """
    pistonX: int
    """
    活塞方块的x坐标
    """
    pistonY: int
    """
    活塞方块的y坐标
    """
    pistonZ: int
    """
    活塞方块的z坐标
    """
    blockList: List[Tuple[int, int, int]]
    """
    活塞运动影响到产生被移动效果的方块坐标(x,y,z)，均为int类型
    """
    breakBlockList: List[Tuple[int, int, int]]
    """
    活塞运动影响到产生被破坏效果的方块坐标(x,y,z)，均为int类型
    """
    entityList: List[str]
    """
    活塞运动影响到产生被移动或被破坏效果的实体ID列表
    """

class EventArgs152(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    posX: float
    """
    实体位置x
    """
    posY: float
    """
    实体位置y
    """
    posZ: float
    """
    实体位置z
    """
    motionX: float
    """
    瞬时移动x方向的力
    """
    motionY: float
    """
    瞬时移动y方向的力
    """
    motionZ: float
    """
    瞬时移动z方向的力
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    cancel: bool
    """
    可由脚本层回传True给引擎，阻止触发后续原版逻辑
    """

class EventArgs153(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    fallDistance: float
    """
    实体下降距离，可在脚本层传给引擎
    """
    cancel: bool
    """
    是否取消引擎对实体下降伤害的计算
    """

class EventArgs154(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    posX: float
    """
    实体位置x
    """
    posY: float
    """
    实体位置y
    """
    posZ: float
    """
    实体位置z
    """
    motionX: float
    """
    瞬时移动x方向的力
    """
    motionY: float
    """
    瞬时移动y方向的力
    """
    motionZ: float
    """
    瞬时移动z方向的力
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    calculate: bool
    """
    是否按脚本层传值计算力
    """

class EventArgs155(EventArgsProxy):
    x: int
    """
    漏斗x坐标
    """
    y: int
    """
    漏斗y坐标
    """
    z: int
    """
    漏斗z坐标
    """
    attachedPosX: int
    """
    交互的容器的x坐标
    """
    attachedPosY: int
    """
    交互的容器的y坐标
    """
    attachedPosZ: int
    """
    交互的容器的z坐标
    """
    dimensionId: int
    """
    维度ID
    """
    canHopper: bool
    """
    是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
    """

class EventArgs156(EventArgsProxy):
    x: int
    """
    漏斗x坐标
    """
    y: int
    """
    漏斗y坐标
    """
    z: int
    """
    漏斗z坐标
    """
    abovePosX: int
    """
    交互的容器位置x
    """
    abovePosY: int
    """
    交互的容器位置y
    """
    abovePosZ: int
    """
    交互的容器位置z
    """
    dimensionId: int
    """
    维度ID
    """
    canHopper: bool
    """
    是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
    """

class EventArgs157(EventArgsProxy):
    fallingBlockId: str
    """
    下落的方块实体ID
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs158(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """

class EventArgs159(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    setBlockType: int
    """
    耕地退化为泥土的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
    """

class EventArgs160(EventArgsProxy):
    fallingBlockId: str
    """
    下落的方块实体ID
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    heavyBlockName: int
    """
    重力方块的identifier，包含命名空间及名称
    """
    prevHereBlockName: int
    """
    变回重力方块时，原本方块位置的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """
    fallTickAmount: int
    """
    下落的方块实体持续下落了多少tick
    """

class EventArgs161(EventArgsProxy):
    fallingBlockId: str
    """
    下落的方块实体ID
    """
    fallingBlockX: float
    """
    下落的方块实体位置x
    """
    fallingBlockY: float
    """
    下落的方块实体位置y
    """
    fallingBlockZ: float
    """
    下落的方块实体位置z
    """
    blockName: str
    """
    重力方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """
    collidingEntitys: List[str] | None
    """
    当前碰撞到的实体ID的列表，如果没有的话是None
    """
    fallTickAmount: int
    """
    下落的方块实体持续下落了多少tick
    """
    fallDistance: float
    """
    下落的方块实体持续下落了多少距离
    """
    isHarmful: bool
    """
    是否计算对实体的伤害，引擎传来的值由json配置和伤害是否大于0决定，可在脚本层修改传回引擎
    """
    fallDamage: int
    """
    对实体的伤害，引擎传来的值距离和json配置决定，可在脚本层修改传回引擎
    """

class EventArgs162(EventArgsProxy):
    fallingBlockId: str
    """
    下落的方块实体ID
    """
    fallingBlockX: float
    """
    下落的方块实体位置x
    """
    fallingBlockY: float
    """
    下落的方块实体位置y
    """
    fallingBlockZ: float
    """
    下落的方块实体位置z
    """
    blockName: str
    """
    重力方块的identifier，包含命名空间及名称
    """
    fallTickAmount: int
    """
    下落的方块实体持续下落了多少tick
    """
    dimensionId: int
    """
    维度ID
    """
    cancelDrop: bool
    """
    是否取消方块物品掉落，可以在脚本层中设置
    """

class EventArgs163(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    entityId: str
    """
    实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """

class EventArgs164(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """

class EventArgs165(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    playerUid: long
    """
    玩家的uid
    """
    command: str
    """
    企图修改的命令方块中的命令内容字符串
    """
    isBlock: bool
    """
    是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
    """
    blockX: int
    """
    命令方块位置x，当isBlock为True时有效
    """
    blockY: int
    """
    命令方块位置y，当isBlock为True时有效
    """
    blockZ: int
    """
    命令方块位置z，当isBlock为True时有效
    """
    victimId: str
    """
    命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
    """
    cancel: bool
    """
    修改为True时，可以阻止玩家修改命令方块的内置命令
    """

class EventArgs166(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    isBlock: bool
    """
    是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
    """
    blockX: int
    """
    命令方块位置x，当isBlock为True时有效
    """
    blockY: int
    """
    命令方块位置y，当isBlock为True时有效
    """
    blockZ: int
    """
    命令方块位置z，当isBlock为True时有效
    """
    victimId: str
    """
    命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
    """
    cancel: bool
    """
    修改为True时，可以阻止玩家打开命令方块的设置界面
    """

class EventArgs167(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止小箱子组合成为一个大箱子
    """
    blockX: int
    """
    小箱子方块x坐标
    """
    blockY: int
    """
    小箱子方块y坐标
    """
    blockZ: int
    """
    小箱子方块z坐标
    """
    otherBlockX: int
    """
    将要与之组合的另外一个小箱子方块x坐标
    """
    otherBlockY: int
    """
    将要与之组合的另外一个小箱子方块y坐标
    """
    otherBlockZ: int
    """
    将要与之组合的另外一个小箱子方块z坐标
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs168(EventArgsProxy):
    posX: int
    """
    方块x坐标
    """
    posY: int
    """
    方块y坐标
    """
    posZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    newStrength: int
    """
    变化后的红石信号量
    """
    oldStrength: int
    """
    变化前的红石信号量
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs169(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    turnSnow: bool
    """
    是否转为含雪，true则转为含雪，false则脱离含雪
    """
    setBlockType: int
    """
    方块进入脱离含雪的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
    """

class EventArgs170(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    turnSnow: bool
    """
    是否转为含雪，true则转为含雪，false则脱离含雪
    """
    setBlockType: int
    """
    方块进入脱离含雪的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
    """

class EventArgs171(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    dimension: int
    """
    维度ID
    """

class EventArgs172(EventArgsProxy):
    dimensionId: int
    """
    维度ID
    """
    posX: int
    """
    方块x坐标
    """
    posY: int
    """
    方块y坐标
    """
    posZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块名称
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """

class EventArgs173(EventArgsProxy):
    dimensionId: int
    """
    维度ID
    """
    posX: int
    """
    方块x坐标
    """
    posY: int
    """
    方块y坐标
    """
    posZ: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    neighborPosX: int
    """
    变化方块x坐标
    """
    neighborPosY: int
    """
    变化方块y坐标
    """
    neighborPosZ: int
    """
    变化方块z坐标
    """
    fromBlockName: str
    """
    方块变化前的identifier，包含命名空间及名称
    """
    fromBlockAuxValue: int
    """
    方块变化前附加值
    """
    toBlockName: str
    """
    方块变化后的identifier，包含命名空间及名称
    """
    toAuxValue: int
    """
    方块变化后附加值
    """

class EventArgs174(EventArgsProxy):
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    turnLiquid: bool
    """
    是否转为含水，True则转为含水，False则脱离含水
    """

class EventArgs175(EventArgsProxy):
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxValue: int
    """
    方块的附加值
    """
    dimension: int
    """
    维度ID
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    turnLiquid: bool
    """
    是否转为含水，True则转为含水，False则脱离含水
    """

class EventArgs176(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    liquidName: str
    """
    流体方块identifier
    """
    blockName: str
    """
    方块的identifier
    """
    auxValue: int
    """
    方块的附加值
    """
    dimensionId: int
    """
    方块所在维度ID
    """

class EventArgs177(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs178(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    experienceValue: int
    """
    经验球经验值
    """
    cancel: bool
    """
    是否取消
    """

class EventArgs179(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    cancel: bool
    """
    是否取消
    """

class EventArgs180(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """

class EventArgs181(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs182(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs183(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs184(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """

class EventArgs185(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    attacker: str
    """
    伤害来源实体ID，若没有实体攻击，例如高空坠落，该值为"-1"
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs186(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
    食物的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    hunger: int
    """
    食物增加的饥饿值，可修改
    """
    nutrition: float
    """
    食物的营养价值，回复饱和度 = 食物增加的饥饿值 * 食物的营养价值 * 2，饱和度最大不超过当前饥饿值，可修改
    """

class EventArgs187(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    attacker: str
    """
    伤害来源的实体ID
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs188(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    posX: int
    """
    碰撞方块x坐标
    """
    posY: int
    """
    碰撞方块y坐标
    """
    posY: int
    """
    碰撞方块z坐标
    """
    blockId: float
    """
    碰撞方块的identifier
    """
    auxValue: int
    """
    碰撞方块的附加值
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs189(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID， `SetDefaultGameType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E4%B8%96%E7%95%8C/%E6%B8%B8%E6%88%8F%E8%A7%84%E5%88%99.html?key=SetDefaultGameType&docindex=2&type=0>`_ 接口改变游戏模式时该参数为空字符串
    """
    oldGameType: int
    """
    切换前的游戏模式
    """
    newGameType: int
    """
    切换后的游戏模式
    """

class EventArgs190(EventArgsProxy):
    pos: Tuple[float, float, float]
    """
    火焰方块的坐标
    """
    playerId: str
    """
    玩家的实体ID
    """
    cancel: bool
    """
    修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireClientEvent一起修改
    """

class EventArgs191(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    fromDimensionId: int
    """
    维度改变前的维度ID
    """
    toDimensionId: int
    """
    维度改变前的维度ID
    """
    fromX: float
    """
    改变前的位置x
    """
    fromY: float
    """
    改变前的位置y
    """
    fromZ: float
    """
    改变前的位置z
    """
    toX: float
    """
    改变后的位置x
    """
    toY: float
    """
    改变后的位置y
    """
    toZ: float
    """
    改变后的位置z
    """

class EventArgs192(EventArgsProxy):
    level: int
    """
    玩家当前等级
    """
    levelUpCostExp: int
    """
    当前等级升级到下个等级需要的经验值，当设置升级经验小于1时会被强制调整到1
    """
    changed: bool
    """
    设置为True，重载玩家升级经验才会生效
    """

class EventArgs193(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    addLevel: int
    """
    增加的等级值
    """
    newLevel: int
    """
    新的等级
    """

class EventArgs194(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    addExp: int
    """
    增加的经验值
    """

class EventArgs195(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续的传送
    """
    entityId: str
    """
    实体ID
    """
    fromDimensionId: int
    """
    传送前所在的维度
    """
    toDimensionId: int
    """
    传送后的目标维度
    """
    fromX: float
    """
    传送前的位置x
    """
    fromY: float
    """
    传送前的位置y
    """
    fromZ: float
    """
    传送前的位置z
    """
    toX: float
    """
    传送后的位置x
    """
    toY: float
    """
    传送后的位置y
    """
    toZ: float
    """
    传送后的位置z
    """
    cause: str
    """
    传送理由，详情见EntityTeleportCause枚举
    """

class EventArgs196(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    effectName: str
    """
    状态效果的名字
    """
    effectDuration: int
    """
    状态效果的持续时间，单位秒
    """
    effectAmplifier: int
    """
    状态效果等级
    """
    cancel: bool
    """
    设置为True可以取消
    """
    damage: float
    """
    状态将会造成的伤害值，如药水；需要注意，该值不一定是最终的伤害值，例如被伤害吸收效果扣除。只有持续时间为0时有用
    """

class EventArgs197(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续的实体交互事件
    """
    actorId: str
    """
    骑乘者的实体ID
    """
    victimId: str
    """
    被骑乘的实体ID
    """

class EventArgs198(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    effectName: str
    """
    被移除状态效果的名字
    """
    effectDuration: int
    """
    被移除状态效果的剩余持续时间，单位秒
    """
    effectAmplifier: int
    """
    被移除状态效果等级
    """

class EventArgs199(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    effectName: str
    """
    更新状态效果的名字
    """
    effectDuration: int
    """
    更新后状态效果剩余持续时间，单位秒
    """
    effectAmplifier: int
    """
    更新后的状态效果放大倍数
    """
    damage: float
    """
    状态造成的伤害值，如药水
    """

class EventArgs200(EventArgsProxy):
    id: str
    """
    抛射物的实体ID
    """
    targetId: str
    """
    碰撞目标的实体ID
    """

class EventArgs201(EventArgsProxy):
    mobId: str
    """
    当前生物的实体ID
    """
    hittedMobList: List[str]
    """
    当前生物碰撞到的其他所有生物实体ID的list
    """

class EventArgs202(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs203(EventArgsProxy):
    victim: str
    """
    受伤实体ID
    """
    src: str
    """
    火焰创建者的实体ID
    """
    fireTime: float
    """
    着火时间，单位秒，不支持修改
    """
    cancel: bool
    """
    是否取消此处火焰伤害
    """
    cancelIgnite: bool
    """
    是否取消点燃效果
    """

class EventArgs204(EventArgsProxy):
    cancel: bool
    """
    是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
    """
    blockX: int
    """
    方块x坐标
    """
    blockY: int
    """
    方块y坐标
    """
    blockZ: int
    """
    方块z坐标
    """
    entityId: str
    """
    实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs205(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    from: str
    """
    变化前的生命值
    """
    to: str
    """
    变化后的生命值
    """
    byScript: str
    """
    是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
    """

class EventArgs206(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    identifier: str
    """
    实体identifier
    """

class EventArgs207(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    secondaryActor: str
    """
    物品给予者的实体ID（一般是玩家），如果不存在给予者的话，这里为空字符串
    """

class EventArgs208(EventArgsProxy):
    motionId: int
    """
    运动器ID
    """
    entityId: str
    """
    实体ID
    """
    remove: bool
    """
    是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除，该参数设置只对非玩家实体有效
    """

class EventArgs209(EventArgsProxy):
    motionId: int
    """
    运动器ID
    """
    entityId: str
    """
    实体ID
    """

class EventArgs210(EventArgsProxy):
    args: list
    """
    该事件的参数为长度为2的list，而非dict，其中list的第一个元素为实体ID
    """

class EventArgs211(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    damage: float
    """
    伤害值（伤害吸收后实际扣血量），负数表示生命回复量
    """
    attributeBuffType: int
    """
    状态类型，参考 `AttributeBuffType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/AttributeBuffType.html?key=AttributeBuffType&docindex=1&type=0>`_
    """
    duration: float
    """
    状态持续时间，单位秒
    """
    lifeTimer: float
    """
    状态生命时间，单位秒
    """
    isInstantaneous: bool
    """
    是否为立即生效状态
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
    """

class EventArgs212(EventArgsProxy):
    entityId: str
    """
    生物的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    itemEntityId: str
    """
    物品的实体ID
    """

class EventArgs213(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    fromDimensionId: int
    """
    维度改变前的维度ID
    """
    toDimensionId: int
    """
    维度改变后的维度ID
    """
    fromX: float
    """
    改变前的位置x
    """
    fromY: float
    """
    改变前的位置y
    """
    fromZ: float
    """
    改变前的位置z
    """
    toX: float
    """
    改变后的位置x
    """
    toY: float
    """
    改变后的位置y
    """
    toZ: float
    """
    改变后的位置z
    """

class EventArgs214(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    formState: bool
    """
    事件触发前，实体是否在游泳状态
    """
    toState: bool
    """
    事件触发后，实体是否在游泳状态
    """

class EventArgs215(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    effectName: str
    """
    实体获得状态效果的名字
    """
    effectDuration: int
    """
    状态效果的持续时间，单位秒
    """
    effectAmplifier: int
    """
    状态效果的等级
    """
    damage: float
    """
    状态造成的伤害值（真实扣除生命值的量）。只有持续时间为0时有用
    """

class EventArgs216(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_
    """
    damage: float
    """
    伤害值（被伤害吸收后的值），不可修改
    """
    absorbedDamage: int
    """
    被伤害吸收效果吸收的伤害值
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs217(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    identifier: str
    """
    生成实体的命名空间
    """
    type: str
    """
    生成实体的类型，参考 `EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_
    """
    baby: str
    """
    生成怪物是否是幼年怪
    """
    x: str
    """
    生成实体坐标x
    """
    y: str
    """
    生成实体坐标y
    """
    z: str
    """
    生成实体坐标z
    """
    dimensionId: int
    """
    生成实体的维度ID，默认值为0（0为主世界，1为地狱，2为末地）
    """
    realIdentifier: int
    """
    生成实体的命名空间，通过MOD API生成的生物在这个参数也能获取到真正的命名空间，而不是以custom开头的
    """
    cancel: bool
    """
    是否取消生成该实体
    """

class EventArgs218(EventArgsProxy):
    enable: bool
    """
    是否允许继续生成。若设为False，可阻止生成生物
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    dimensionId: int
    """
    维度ID
    """
    entityWillBeGenerated: str
    """
    即将生成生物的名字，如"minecraft:pig"
    """

class EventArgs219(EventArgsProxy):
    entityId: str
    """
    生成生物的实体ID
    """
    entityGenerated: str
    """
    生成生物的名字，如"minecraft:pig"
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs220(EventArgsProxy):
    username: str
    """
    玩家名称
    """
    playerId: str
    """
    玩家的实体ID
    """
    message: str
    """
    玩家发送的聊天消息内容
    """
    cancel: bool
    """
    是否取消这个聊天事件，若取消可以设置为True
    """
    bChatById: bool
    """
    是否把聊天消息发送给指定在线玩家，而不是广播给所有在线玩家，若只发送某些玩家可以设置为True
    """
    bForbid: bool
    """
    是否禁言，仅apollo可用。True：被禁言，玩家聊天会提示“你已被管理员禁言”
    """
    toPlayerIds: List[str]
    """
    接收聊天消息的玩家实体ID的列表，bChatById为True时生效
    """
    gameChatPrefix: str
    """
    设置当前玩家在网易聊天界面中的前缀，字数限制4，从字符串头部开始取。前缀文本输入非字符串格式时会被置为空。若cancel为True，会取消掉本次的前缀修改
    """
    gameChatPrefixColorR: float
    """
    设置当前玩家在网易聊天界面中前缀颜色rgb的r值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
    """
    gameChatPrefixColorG: float
    """
    设置当前玩家在网易聊天界面中前缀颜色rgb的g值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
    """
    gameChatPrefixColorB: float
    """
    设置当前玩家在网易聊天界面中前缀颜色rgb的b值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
    """

class EventArgs221(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    name: str
    """
    玩家昵称
    """
    cancel: bool
    """
    是否显示提示文字，允许修改。True：不显示提示
    """
    message: str
    """
    玩家离开游戏的提示文字，允许修改
    """

class EventArgs222(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    name: str
    """
    玩家昵称
    """
    cancel: bool
    """
    是否显示提示文字，允许修改。True：不显示提示
    """
    message: str
    """
    玩家加入游戏的提示文字，允许修改
    """

class EventArgs223(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs224(EventArgsProxy):
    structureName: str
    """
    结构名称
    """
    x: int
    """
    结构坐标最小方块所在的x坐标
    """
    y: int
    """
    结构坐标最小方块所在的y坐标
    """
    z: int
    """
    结构坐标最小方块所在的z坐标
    """
    biomeType: int
    """
    该feature所放置区块的生物群系类型
    """
    biomeName: int
    """
    该feature所放置区块的生物群系名称
    """
    dimensionId: int
    """
    维度ID
    """
    cancel: bool
    """
    设置为True时可阻止该结构的放置
    """

class EventArgs225(EventArgsProxy):
    oldLevel: float
    """
    改变前的下雨强度
    """
    newLevel: float
    """
    改变后的下雨强度
    """

class EventArgs226(EventArgsProxy):
    oldLevel: float
    """
    改变前的下雨强度
    """
    newLevel: float
    """
    改变后的下雨强度
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs227(EventArgsProxy):
    oldLevel: float
    """
    改变前的打雷强度
    """
    newLevel: float
    """
    改变后的打雷强度
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs228(EventArgsProxy):
    oldLevel: float
    """
    改变前的打雷强度
    """
    newLevel: float
    """
    改变后的打雷强度
    """

class EventArgs229(EventArgsProxy):
    loottable: str
    """
    奖励箱子所读取的loottable的json路径
    """
    playerId: str
    """
    打开奖励箱子的玩家的实体ID
    """
    itemList: List[dict]
    """
    掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    dirty: bool
    """
    默认为False，如果需要修改掉落列表需将该值设为True
    """

class EventArgs230(EventArgsProxy):
    command: str
    """
    命令名称
    """
    message: str
    """
    命令返回的消息
    """

class EventArgs231(EventArgsProxy):
    name: str
    """
    感应区域的名称
    """
    enteredEntities: List[str]
    """
    进入该感应区域的实体ID列表
    """
    leftEntities: List[str]
    """
    离开该感应区域的实体ID列表
    """

class EventArgs232(EventArgsProxy):
    pass

class EventArgs233(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    isTransfer: bool
    """
    是否是切服时退出服务器，仅用于Apollo。如果是True，则表示切服时退出服务器；若是False，则表示退出网络游戏
    """
    uid: long
    """
    玩家的netease uid，玩家的唯一标识
    """

class EventArgs234(EventArgsProxy):
    entityId: str
    """
    玩家的实体ID
    """
    command: str
    """
    指令字符串
    """
    cancel: bool
    """
    是否取消
    """

class EventArgs235(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs236(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    chunkPosX: int
    """
    区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
    """
    chunkPosZ: int
    """
    区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
    """
    blockEntities: List[dict]
    """
    随区块加载而加载进世界的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标，blockName表示方块的identifier，包含命名空间及名称
    """

class EventArgs237(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    chunkPosX: int
    """
    区块的x坐标，对应方块x坐标区间为[chunkPosX * 16, chunkPosX * 16 + 15]
    """
    chunkPosZ: int
    """
    区块的z坐标，对应方块z坐标区间为[chunkPosZ * 16, chunkPosZ * 16 + 15]
    """
    blockEntityData: List[dict] | None
    """
    该区块中的自定义方块实体列表，通常是由自定义特征生成的自定义方块，没有自定义方块实体时该值为None。列表元素dict的结构如下：{'blockName': str, 'posX': int, 'posY': int, 'posZ': int}
    """

class EventArgs238(EventArgsProxy):
    dimension: int
    """
    维度ID
    """
    chunkPosX: int
    """
    区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
    """
    chunkPosZ: int
    """
    区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
    """
    entities: List[str]
    """
    随区块卸载而从世界移除的实体ID的列表。注意事件触发时已经无法获取到这些实体的信息，仅供脚本资源回收用
    """
    blockEntities: List[dict]
    """
    随区块卸载而从世界移除的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标。注意事件触发时已经无法获取到这些方块实体的信息，仅供脚本资源回收用
    """

class EventArgs239(EventArgsProxy):
    id: str
    """
    玩家的实体ID
    """
    isTransfer: bool
    """
    是否是切服时进入服务器，仅用于Apollo。如果是True，则表示切服时加入服务器，若是False，则表示登录进入网络游戏
    """
    isReconnect: bool
    """
    是否是断线重连，仅用于Apollo。如果是True，则表示本次登录是断线重连，若是False，则表示本次是正常登录或者转服
    """
    isPeUser: bool
    """
    是否从手机端登录，仅用于Apollo。如果是True，则表示本次登录是从手机端登录，若是False，则表示本次登录是从PC端登录
    """
    transferParam: str
    """
    切服传入参数，仅用于Apollo。调用TransferToOtherServer或TransferToOtherServerById传入的切服参数
    """
    uid: long
    """
    仅用于Apollo，玩家的netease uid，玩家的唯一标识
    """
    proxyId: int
    """
    仅用于Apollo，当前客户端连接的proxy服务器id
    """

class EventArgs240(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    rootNodeId: str
    """
    所属的页面的根节点成就ID
    """
    achievementId: str
    """
    达成的成就ID
    """
    title: str
    """
    成就标题
    """
    description: str
    """
    成就描述
    """

class EventArgs241(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    victimId: str
    """
    受击者的实体ID
    """
    damage: float
    """
    伤害值，引擎传过来的值是0，允许脚本层修改为其他数
    """
    isValid: int
    """
    脚本是否设置伤害值：1表示是，0表示否
    """
    cancel: bool
    """
    是否取消该次攻击，默认不取消
    """
    isKnockBack: bool
    """
    是否支持击退效果，默认支持，当不支持时将屏蔽武器击退附魔效果
    """
    isCrit: bool
    """
    本次攻击是否产生暴击，不支持修改
    """

class EventArgs242(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    aux: int
    """
    方块附加值
    """
    cancel: bool
    """
    设置为True可拦截与方块交互的逻辑
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    itemDict: dict
    """
    使用的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs243(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs244(EventArgsProxy):
    projectileId: str
    """
    抛射物的实体ID
    """
    projectileIdentifier: str
    """
    抛射物的identifier
    """
    spawnerId: str
    """
    发射者的实体ID，没有发射者时为-1
    """

class EventArgs245(EventArgsProxy):
    dieEntityId: str
    """
    死亡实体ID
    """
    attacker: str
    """
    伤害来源实体ID
    """
    itemList: List[dict]
    """
    掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    dirty: bool
    """
    默认为False，如果需要修改掉落列表需将该值设为True
    """

class EventArgs246(EventArgsProxy):
    srcId: str
    """
    伤害源实体ID
    """
    projectileId: str
    """
    抛射物实体ID
    """
    entityId: str
    """
    受伤的实体ID
    """
    damage: float
    """
    伤害值（被伤害吸收后的值），允许修改，设置为0则此次造成的伤害为0，若设置数值和原来一样则视为没有修改
    """
    invulnerableTime: int
    """
    实体受击后，剩余的无懈可击帧数，在无懈可击时间内，damage为超过上次伤害的部分
    """
    lastHurt: float
    """
    实体上次受到的伤害
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs247(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    from: float
    """
    变化前的生命值
    """
    to: float
    """
    将要变化到的生命值，cancel设置为True时可以取消该变化，但是此参数不变
    """
    byScript: bool
    """
    是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
    """
    cancel: bool
    """
    是否取消该变化
    """

class EventArgs248(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    fromDimensionId: int
    """
    维度改变前的维度
    """
    toDimensionId: int
    """
    维度改变后的维度
    """
    toPos: Tuple[float, float, float]
    """
    改变后的位置，其中y值为脚底加上角色的身高值
    """

class EventArgs249(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    eventName: str
    """
    触发的事件名称
    """

class EventArgs250(EventArgsProxy):
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    interactEntityId: str
    """
    交互生物的实体ID
    """

class EventArgs251(EventArgsProxy):
    cancel: bool
    """
    是否取消触发，默认为False，若设为True，可阻止触发后续的实体交互事件
    """
    playerId: str
    """
    玩家的实体ID
    """
    itemDict: dict
    """
    玩家手持物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    victimId: str
    """
    交互生物的实体ID
    """

class EventArgs252(EventArgsProxy):
    id: str
    """
    实体ID
    """
    attacker: str
    """
    攻击者实体ID
    """
    cause: str
    """
    伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs253(EventArgsProxy):
    id: str
    """
    实体ID
    """
    posX: float
    """
    实体位置x
    """
    posY: float
    """
    实体位置y
    """
    posZ: float
    """
    实体位置z
    """
    dimensionId: int
    """
    维度ID
    """
    isBaby: bool
    """
    是否为幼儿
    """
    engineTypeStr: str
    """
    实体类型，即实体identifier
    """
    itemName: str
    """
    物品identifier（仅当物品实体时存在该字段）
    """
    auxValue: int
    """
    物品附加值（仅当物品实体时存在该字段）
    """

class EventArgs254(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    posX: int
    """
    碰撞方块x坐标
    """
    posY: int
    """
    碰撞方块y坐标
    """
    posZ: int
    """
    碰撞方块z坐标
    """
    blockId: str
    """
    碰撞方块的identifier
    """
    auxValue: int
    """
    碰撞方块的附加值
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs255(EventArgsProxy):
    entityId: str
    """
    实体ID
    """
    slowdownMultiX: float
    """
    实体移速x方向的减速比例，可在脚本层被修改
    """
    slowdownMultiY: float
    """
    实体移速y方向的减速比例，可在脚本层被修改
    """
    slowdownMultiZ: float
    """
    实体移速z方向的减速比例，可在脚本层被修改
    """
    blockX: int
    """
    方块位置x
    """
    blockY: int
    """
    方块位置y
    """
    blockZ: int
    """
    方块位置z
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    cancel: bool
    """
    可由脚本层回传True给引擎，阻止触发后续原版逻辑
    """

class EventArgs256(EventArgsProxy):
    id: str
    """
    骑乘者实体ID
    """
    rideId: str
    """
    坐骑实体ID
    """

class EventArgs257(EventArgsProxy):
    id: str
    """
    实体ID
    """
    rideId: str
    """
    坐骑的实体ID
    """
    exitFromRider: bool
    """
    是否下坐骑
    """
    entityIsBeingDestroyed: bool
    """
    坐骑是否将要销毁
    """
    switchingRides: bool
    """
    是否换乘坐骑
    """
    cancel: bool
    """
    设置为True可以取消（需要与客户端事件一同取消）
    """

class EventArgs258(EventArgsProxy):
    entityId: str
    """
    玩家实体ID
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    blockName: str
    """
    方块的identifier，包含命名空间及名称
    """
    blockAuxValue: int
    """
    方块的附加值
    """
    face: int
    """
    点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    clickX: float
    """
    点击点的x比例位置
    """
    clickY: float
    """
    点击点的y比例位置
    """
    clickZ: float
    """
    点击点的z比例位置
    """
    ret: bool
    """
    设为True可取消物品的使用
    """

class EventArgs259(EventArgsProxy):
    playerId: str
    """
    玩家的实体id
    """
    itemDict: dict
    """
     `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    useMethod: int
    """
    使用物品的方法，详见 `ItemUseMethodEnum枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemUseMethodEnum.html?key=ItemUseMethodEnum&docindex=1&type=0>`_
    """

class EventArgs260(EventArgsProxy):
    actor: str
    """
    获得物品玩家实体ID
    """
    secondaryActor: str
    """
    物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
    """
    itemDict: dict
    """
    获得的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
    """
    acquireMethod: int
    """
    获得物品的方法，详见 `ItemAcquisitionMethod枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemAcquisitionMethod.html?key=ItemAcquisitionMethod&docindex=1&type=0>`_
    """

class EventArgs261(EventArgsProxy):
    x: int
    """
    方块x坐标
    """
    y: int
    """
    方块y坐标
    """
    z: int
    """
    方块z坐标
    """
    face: int
    """
    方块被敲击的面向id，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    fullName: str
    """
    方块的identifier，包含命名空间及名称
    """
    auxData: int
    """
    方块附加值
    """
    playerId: str
    """
    破坏方块的玩家实体ID
    """
    dimensionId: int
    """
    维度ID
    """
    dropEntityIds: List[str]
    """
    掉落物实体ID列表
    """

class EventArgs262(EventArgsProxy):
    srcId: str
    """
    伤害源实体ID
    """
    projectileId: str
    """
    投射物实体ID
    """
    entityId: str
    """
    受伤实体ID
    """
    damage: int
    """
    伤害值（被伤害吸收前的值），允许修改，设置为0则此次造成的伤害为0
    """
    damage_f: float
    """
    伤害值（被伤害吸收前的值），不允许修改
    """
    absorption: int
    """
    伤害吸收生命值，详见 `AttrType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/AttrType.html?key=AttrType&docindex=1&type=0>`_ 枚举的ABSORPTION
    """
    cause: str
    """
    伤害来源，详见 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举
    """
    knock: bool
    """
    是否击退被攻击者，允许修改，设置该值为False则不产生击退
    """
    ignite: bool
    """
    是否点燃被伤害者，允许修改，设置该值为True产生点燃效果，反之亦然
    """
    customTag: str
    """
    使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
    """

class EventArgs263(EventArgsProxy):
    blocks: List[List[int, int, int, bool]]
    """
    爆炸涉及到的方块列表，每个方块以一个列表表示，前三个元素分别为方块坐标xyz，第四个元素为是否取消爆炸对该方块的影响，将第四个元素设置为True即可取消。
    """
    victims: List[str] | None
    """
    受伤实体ID列表，当该爆炸创建者实体ID为None时，victims也为None
    """
    sourceId: str | None
    """
    爆炸创建者实体ID
    """
    explodePos: List[float, float, float]
    """
    爆炸位置[x, y, z]
    """
    dimensionId: int
    """
    维度ID
    """

class EventArgs264(EventArgsProxy):
    id: str
    """
    子弹的实体ID
    """
    hitTargetType: str
    """
    碰撞目标类型，"ENTITY"或"BLOCK"
    """
    targetId: str
    """
    碰撞目标的实体ID
    """
    hitFace: int
    """
    撞击在方块上的面ID，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
    """
    x: float
    """
    碰撞x坐标
    """
    y: float
    """
    碰撞y坐标
    """
    z: float
    """
    碰撞z坐标
    """
    blockPosX: int
    """
    碰撞是方块时，方块x坐标
    """
    blockPosY: int
    """
    碰撞是方块时，方块y坐标
    """
    blockPosZ: int
    """
    碰撞是方块时，方块z坐标
    """
    srcId: str
    """
    抛射物创建者的实体ID
    """
    cancel: bool
    """
    是否取消这个碰撞事件，若取消可以设置为True
    """

class EventArgs265(EventArgsProxy):
    oldItemDict: dict | None
    """
    旧物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧物品为空时，此项属性为None
    """
    newItemDict: dict | None
    """
    新物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新物品为空时，此项属性为None
    """
    playerId: str
    """
    玩家的实体ID
    """

class EventArgs266(EventArgsProxy):
    id: str
    """
    实体ID
    """

class EventArgs267(EventArgsProxy):
    pass

class EventArgs268(EventArgsProxy):
    player_id: str
    """
    玩家的实体ID
    """
    pos: Tuple[str, int]
    """
    发生变化的方格位置元组
    """
    old_item: dict | None
    """
    变化前的物品信息字典
    """
    new_item: dict | None
    """
    变化后的物品信息字典
    """
    cancel: bool
    """
    是否取消本次变化
    """

class EventArgs269(EventArgsProxy):
    __id__: str
    """
    玩家的实体ID
    """

