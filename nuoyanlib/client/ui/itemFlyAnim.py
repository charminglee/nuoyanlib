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
#   Last Modified : 2023-09-02
#
# ====================================================


"""

itemFlyAnim
===========

该模块提供了物品飞行动画的Python实现。通过ItemFlyAnim，您可以轻松实现一个像原版一样丝滑的物品飞行动画。

-----

【使用方法】

1、将NyItemFlyAnim.json放到资源包的ui文件夹内，然后在_ui_def.json中填入"ui/NyItemFlyAnim.json"。

2、将您的UI类继承ItemFlyAnim，此后无需再继承ScreenNode，例如：class MyUi(ItemFlyAnim)，然后正常注册与创建您的UI。

3、通过调用self.SetOneItemFlyAnim即可运行一个物品飞行动画，调用self.SetItemsFlyAnim可同时运行多个物品飞行动画。

-----

【注意事项】

1、建议不要同时运行较多物品飞行动画，否则可能会造成性能问题。

2、目前暂不支持通过堆栈管理方式创建的UI。

"""


import mod.client.extraClientApi as _clientApi
from ...utils.item import is_empty_item as _is_empty_item
from ..clientComps import (
    ScreenNode as _ScreenNode,
    ViewBinder as _ViewBinder,
    LevelComps as _LevelComps,
)


__all__ = [
    "ItemFlyAnim",
]


_PATH = __file__.replace(".py", "").replace("/", ".") if "/" in __file__ else __file__
_NAMESPACE = "NuoyanLib"
_UI_NAME_ITEM_FLY_ANIM = "NyItemFlyAnim"
_UI_PATH_ITEM_FLY_ANIM = _PATH + "._ItemFlyAnimUI"
_UI_DEF_ITEM_FLY_ANIM = "NyItemFlyAnim.main"
_UI_PATH_FLY_ITEM_1 = "/item_fly_panel/item_renderer1"
_UI_PATH_FLY_ITEM_2 = "/item_fly_panel/item_renderer2"


class ItemFlyAnim(_ScreenNode):
    """
    为原版ScreenNode提供物品飞行动画支持。

    -----

    【接口一览】

    1、SetOneItemFlyAnim：设置单个物品飞行动画。

    2、SetItemsFlyAnim：设置多个物品飞行动画。
    """

    def __init__(self, namespace, name, param):
        super(ItemFlyAnim, self).__init__(namespace, name, param)
        self._itemFlyAnimNode = None
        self.__registerItemFlyAnimUI()

    def __registerItemFlyAnimUI(self):
        uiNode = _clientApi.GetUI(_NAMESPACE, _UI_NAME_ITEM_FLY_ANIM)
        if uiNode:
            self._itemFlyAnimNode = uiNode
        else:
            _clientApi.RegisterUI(
                _NAMESPACE, _UI_NAME_ITEM_FLY_ANIM, _UI_PATH_ITEM_FLY_ANIM, _UI_DEF_ITEM_FLY_ANIM
            )
            self._itemFlyAnimNode = _clientApi.CreateUI(
                _NAMESPACE, _UI_NAME_ITEM_FLY_ANIM, {'isHud': 1, '__cs__': self}
            )

    def SetOneItemFlyAnim(self, itemDict, fromPos, toPos, uiSize):
        """
        设置单个物品飞行动画。

        -----

        :param dict itemDict: 物品信息字典
        :param tuple[float,float] fromPos: 动画起点坐标
        :param tuple[float,float] toPos: 动画终点坐标
        :param float|tuple[float,float] uiSize: 物品图标尺寸，传入float时，图标长宽均设置为该值，传入tuple时，图标长宽设置为该元组对应值

        :return: 无
        :rtype: None
        """
        self._itemFlyAnimNode.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def SetItemsFlyAnim(self, itemAnimDataList):
        """
        设置多个物品飞行动画。

        -----

        :param list[dict[str,Any]] itemAnimDataList: 动画数据列表，列表每个元素为一个字典，字典的key分别为itemDict、fromPos、toPos、uiSize，对应的value的含义与SetOneItemFlyAnim方法中的参数相同。

        :return: 无
        :rtype: None
        """
        self._itemFlyAnimNode.SetItemsFlyAnim(itemAnimDataList)


class _ItemFlyAnimUI(_ScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemFlyAnimUI, self).__init__(namespace, name, param)
        self.itemFlyQueue = {}
        self.flyIRs = []

    def Create(self):
        self.flyIRs.append(self.GetBaseUIControl(_UI_PATH_FLY_ITEM_1).asItemRenderer())
        self.flyIRs.append(self.GetBaseUIControl(_UI_PATH_FLY_ITEM_2).asItemRenderer())

    # ====================================== System Event Callback =====================================================

    @_ViewBinder.binding(_ViewBinder.BF_BindString, "#main.gametick")
    def OnGameTick(self):
        # 物品飞行动画
        for k, data in self.itemFlyQueue.items():
            x = data['xOff']
            y = data['yOff']
            uiCtrl = data['uiCtrl']
            pos = uiCtrl.GetPosition()
            uiCtrl.SetPosition((pos[0] + x, pos[1] + y))
            data['tick'] -= 1
            # 动画结束
            if data['tick'] <= 0:
                uiCtrl.SetVisible(False)
                del self.itemFlyQueue[k]

    # ========================================== Basic Function ========================================================

    def _cloneNewIr(self):
        name = str(len(self.flyIRs))
        if self.Clone(_UI_PATH_FLY_ITEM_1, "/item_fly_panel", name):
            ir = self.GetBaseUIControl("/item_fly_panel/" + name).asItemRenderer()
            self.flyIRs.append(ir)
            return ir

    def _getIdleIrIndex(self):
        for i in range(len(self.flyIRs)):
            if i not in self.itemFlyQueue:
                return i

    def SetOneItemFlyAnim(self, itemDict, fromPos, toPos, uiSize):
        if _is_empty_item(itemDict, False):
            return
        # ItemRenderer不够用时克隆出新的ItemRenderer，否则使用空闲的ItemRenderer
        queueLen = len(self.itemFlyQueue)
        uiCount = len(self.flyIRs)
        if queueLen >= uiCount:
            ir = self._cloneNewIr()
            if not ir:
                return
            index = uiCount
        else:
            index = self._getIdleIrIndex()
            if index is None:
                return
            ir = self.flyIRs[index]
        # 配置ItemRenderer
        itemName = itemDict['newItemName']
        aux = itemDict.get('newAuxValue', 0)
        isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
        userData = itemDict.get('userData')
        ir.SetUiItem(itemName, aux, isEnchanted, userData)
        ir.SetVisible(True)
        ir.SetPosition(fromPos)
        ir.SetSize(uiSize if isinstance(uiSize, tuple) else (uiSize,) * 2)
        # 动画持续帧数
        dur = int(_LevelComps.Game.GetFps() * 0.175)
        # x轴上每帧的偏移量
        xOff = (toPos[0] - fromPos[0]) / dur
        # y轴上每帧的偏移量
        yOff = (toPos[1] - fromPos[1]) / dur
        # 添加进动画执行队列
        self.itemFlyQueue[index] = {
            'xOff': xOff,
            'yOff': yOff,
            'tick': dur,
            'uiCtrl': ir,
        }

    def SetItemsFlyAnim(self, itemAnimDataList):
        for data in itemAnimDataList:
            self.SetOneItemFlyAnim(**data)













