# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-04-09
#
# ====================================================


import mod.client.extraClientApi as _clientApi
from nuoyanScreenNode import NuoyanScreenNode as _NuoyanScreenNode
from ....nuoyanLib.utils.item import is_empty_item as _is_empty_item
from ..._config import MOD_NAME


_ClientSystem = _clientApi.GetClientSystemCls()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_PlayerItemComp = _ClientCompFactory.CreateItem(_PLAYER_ID)
_PlayerGameComp = _ClientCompFactory.CreateGame(_PLAYER_ID)
_ViewBinder = _clientApi.GetViewBinderCls()


if "/" in __file__:
    _PATH = __file__[:-3].replace("/", ".")
else:
    _PATH = __file__
UI_NAME_ITEM_FLY_ANIM = "ItemFlyAnim"
UI_PATH_ITEM_FLY_ANIM = _PATH + "._ItemFlyAnimUI"
UI_DEF_ITEM_FLY_ANIM = "ItemFlyAnim.main"
UI_PATH_FLY_ITEM_1 = "/item_fly_panel/item_renderer1"
UI_PATH_FLY_ITEM_2 = "/item_fly_panel/item_renderer2"


class ItemFlyAnim(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(ItemFlyAnim, self).__init__(namespace, name, param)
        self._itemFlyAnimNode = None
        self._registerItemFlyAnimUI()

    def _registerItemFlyAnimUI(self):
        uiNode = _clientApi.GetUI(MOD_NAME, UI_NAME_ITEM_FLY_ANIM)
        if uiNode:
            self._itemFlyAnimNode = uiNode
        else:
            self._itemFlyAnimNode = self.cs.RegisterAndCreateUI(
                UI_NAME_ITEM_FLY_ANIM, UI_PATH_ITEM_FLY_ANIM, UI_DEF_ITEM_FLY_ANIM
            )

    def SetOneItemFlyAnim(self, itemDict, fromPos, toPos, uiSize):
        """
        设置单个物品飞行动画。
        """
        self._itemFlyAnimNode.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def SetItemsFlyAnim(self, itemAnimDataList):
        """
        设置多个物品飞行动画。
        """
        self._itemFlyAnimNode.SetItemsFlyAnim(itemAnimDataList)


class _ItemFlyAnimUI(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemFlyAnimUI, self).__init__(namespace, name, param)
        self.itemFlyData = []
        self.flyIRs = []

    def Create(self):
        self.flyIRs.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_1).asItemRenderer())
        self.flyIRs.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_2).asItemRenderer())

    # todo:==================================== System Event Callback ==================================================

    @_ViewBinder.binding(_ViewBinder.BF_BindString, "#main.gametick")
    def OnGameTick(self):
        # 物品飞行动画
        for _, data in enumerate(self.itemFlyData):
            x = data['xOff']
            y = data['yOff']
            uiCtrl = data['uiCtrl']
            pos = uiCtrl.GetPosition()
            uiCtrl.SetPosition((pos[0] + x, pos[1] + y))
            data['tick'] -= 1
            # 动画结束
            if not data['tick']:
                uiCtrl.SetVisible(False)
                self.itemFlyData.remove(data)

    # todo:======================================= Basic Function ======================================================

    def SetOneItemFlyAnim(self, itemDict, fromPos, toPos, uiSize):
        if _is_empty_item(itemDict, False):
            return
        # ItemRenderer不够用时克隆新的ItemRenderer
        # 初始只有2个ItemRenderer用于物品飞行动画，但同时使用的ItemRenderer可能是多个
        num = len(self.itemFlyData)
        if num > len(self.flyIRs) - 1:
            name = str(num)
            if self.Clone(UI_PATH_FLY_ITEM_1, "/item_fly_panel", name):
                newIR = self.GetBaseUIControl("/item_fly_panel/" + name).asItemRenderer()
                self.flyIRs.append(newIR)
        # 配置ItemRenderer
        itemName = itemDict['newItemName']
        aux = itemDict['newAuxValue']
        isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
        userData = itemDict.get('userData')
        ir = self.flyIRs[num]
        ir.SetUiItem(itemName, aux, isEnchanted, userData)
        ir.SetVisible(True)
        ir.SetPosition(fromPos)
        ir.SetSize(uiSize, True)
        # 动画持续帧数
        dur = int(_PlayerGameComp.GetFps() * 0.175)
        # x轴上每帧的偏移量
        xOff = (toPos[0] - fromPos[0]) / dur
        # y轴上每帧的偏移量
        yOff = (toPos[1] - fromPos[1]) / dur
        # 添加进动画执行队列
        self.itemFlyData.append({
            'xOff': xOff,
            'yOff': yOff,
            'tick': dur,
            'uiCtrl': ir
        })

    def SetItemsFlyAnim(self, itemAnimDataList):
        for data in itemAnimDataList:
            self.SetOneItemFlyAnim(**data)














