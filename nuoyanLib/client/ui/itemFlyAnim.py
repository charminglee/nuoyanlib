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
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-08-16
#
# ====================================================


import mod.client.extraClientApi as _clientApi
from nuoyanScreenNode import NuoyanScreenNode as _NuoyanScreenNode
from ...utils.item import is_empty_item as _is_empty_item


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
NAMESPACE = "NuoyanLib"
UI_NAME_ITEM_FLY_ANIM = "NyItemFlyAnim"
UI_PATH_ITEM_FLY_ANIM = _PATH + "._ItemFlyAnimUI"
UI_DEF_ITEM_FLY_ANIM = "NyItemFlyAnim.main"
UI_PATH_FLY_ITEM_1 = "/item_fly_panel/item_renderer1"
UI_PATH_FLY_ITEM_2 = "/item_fly_panel/item_renderer2"


class ItemFlyAnim(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(ItemFlyAnim, self).__init__(namespace, name, param)
        self._itemFlyAnimNode = None
        self._registerItemFlyAnimUI()

    def _registerItemFlyAnimUI(self):
        uiNode = _clientApi.GetUI(NAMESPACE, UI_NAME_ITEM_FLY_ANIM)
        if uiNode:
            self._itemFlyAnimNode = uiNode
        else:
            _clientApi.RegisterUI(
                NAMESPACE, UI_NAME_ITEM_FLY_ANIM, UI_PATH_ITEM_FLY_ANIM, UI_DEF_ITEM_FLY_ANIM
            )
            self._itemFlyAnimNode = _clientApi.CreateUI(
                NAMESPACE, UI_NAME_ITEM_FLY_ANIM, {'isHud': 1, '__cs__': self}
            )

    def SetOneItemFlyAnim(self, itemDict, fromPos, toPos, uiSize):
        """
        设置单个物品飞行动画。
        -----------------------------------------------------------
        【itemDict: dict】 物品信息字典
        【fromPos: Tuple[float, float]】 动画起点坐标
        【toPos: Tuple[float, float]】 动画终点坐标
        【uiSize: Union[float, Tuple[float, float]]】 物品图标尺寸，传入float时，图标长宽均设置为该值，传入tuple时，图标长宽设置为该元组对应值
        -----------------------------------------------------------
        NoReturn
        """
        self._itemFlyAnimNode.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def SetItemsFlyAnim(self, itemAnimDataList):
        """
        设置多个物品飞行动画。
        -----------------------------------------------------------
        【itemAnimDataList: List[Dict[str, Any]]】 动画数据列表，列表每个元素为一个字典，字典的key分别为itemDict、fromPos、toPos、uiSize，对应的value的含义与SetOneItemFlyAnim方法中的参数相同。
        -----------------------------------------------------------
        NoReturn
        """
        self._itemFlyAnimNode.SetItemsFlyAnim(itemAnimDataList)


class _ItemFlyAnimUI(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemFlyAnimUI, self).__init__(namespace, name, param)
        self.itemFlyQueue = {}
        self.flyIRs = []

    def Create(self):
        self.flyIRs.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_1).asItemRenderer())
        self.flyIRs.append(self.GetBaseUIControl(UI_PATH_FLY_ITEM_2).asItemRenderer())

    # todo:==================================== System Event Callback ==================================================

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

    # todo:======================================= Basic Function ======================================================

    def _cloneNewIr(self):
        """
        克隆一个新的ItemRenderer。
        """
        name = str(len(self.flyIRs))
        if self.Clone(UI_PATH_FLY_ITEM_1, "/item_fly_panel", name):
            ir = self.GetBaseUIControl("/item_fly_panel/" + name).asItemRenderer()
            self.flyIRs.append(ir)
            return ir

    def _getIdleIrIndex(self):
        """
        获取一个空闲的ItemRenderer的索引位置。
        """
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
        dur = int(_PlayerGameComp.GetFps() * 0.175)
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














