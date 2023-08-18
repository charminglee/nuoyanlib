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
#   Last Modified : 2023-08-15
#
# ====================================================


import mod.client.extraClientApi as _clientApi
from nuoyanScreenNode import NuoyanScreenNode as _NuoyanScreenNode
from ...utils.item import is_empty_item as _is_empty_item


_ScreenNode = _clientApi.GetScreenNodeCls()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_PlayerItemComp = _ClientCompFactory.CreateItem(_PLAYER_ID)
_PlayerGameComp = _ClientCompFactory.CreateGame(_PLAYER_ID)


if "/" in __file__:
    _PATH = __file__[:-3].replace("/", ".")
else:
    _PATH = __file__
NAMESPACE = "NuoyanLib"
UI_NAME_ITEM_TIPS_BOX = "NyItemTipsBox"
UI_PATH_ITEM_TIPS_BOX = _PATH + "._ItemTipsBoxUI"
UI_DEF_ITEM_TIPS_BOX = "NyItemTipsBox.main"
UI_PATH_TIPS_IMAGE = "/tips_panel/image"
UI_PATH_TIPS = "/tips_panel"
UI_PATH_TIPS_LABEL = "/tips_panel/image/label"


class ItemTipsBox(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(ItemTipsBox, self).__init__(namespace, name, param)
        self._itemTipsBoxNode = None
        self._registerItemTipsBoxUI()

    def _registerItemTipsBoxUI(self):
        uiNode = _clientApi.GetUI(NAMESPACE, UI_NAME_ITEM_TIPS_BOX)
        if uiNode:
            self._itemTipsBoxNode = uiNode
        else:
            _clientApi.RegisterUI(
                NAMESPACE, UI_NAME_ITEM_TIPS_BOX, UI_PATH_ITEM_TIPS_BOX, UI_DEF_ITEM_TIPS_BOX
            )
            self._itemTipsBoxNode = _clientApi.CreateUI(
                NAMESPACE, UI_NAME_ITEM_TIPS_BOX, {'isHud': 1, '__cs__': self}
            )

    def ShowItemTipsBox(self, itemDict):
        """
        显示物品格式化hover文本提示框。
        """
        self._itemTipsBoxNode.ShowItemTipsBox(itemDict)

    def ShowTipsBox(self, text):
        """
        显示文本提示框。
        """
        self._itemTipsBoxNode.ShowTipsBox(text)

    def HideItemTipsBox(self):
        """
        隐藏物品信息文本框。
        """
        self._itemTipsBoxNode.HideItemTipsBox()


class _ItemTipsBoxUI(_NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemTipsBoxUI, self).__init__(namespace, name, param)
        self.alphaTick = 0
        self.tipsImg = None
        self.tipsPanel = None
        self.tipsLabel = None
        self.timer1 = None
        self.timer2 = None
        self.listen()

    def Create(self):
        self.tipsLabel = self.GetBaseUIControl(UI_PATH_TIPS_LABEL).asLabel()
        self.tipsPanel = self.GetBaseUIControl(UI_PATH_TIPS)
        self.tipsImg = self.GetBaseUIControl(UI_PATH_TIPS_IMAGE).asImage()
        self.SetScreenVisible(False)

    def listen(self):
        clientNamespace = _clientApi.GetEngineNamespace()
        clientSystemName = _clientApi.GetEngineSystemName()
        self.cs.ListenForEvent(clientNamespace, clientSystemName, "OnScriptTickClient", self, self.OnScriptTick)

    # todo:==================================== System Event Callback ==================================================

    def OnGameTick(self):
        pass

    def OnScriptTick(self):
        # tips透明度动画
        if self.alphaTick:
            self.alphaTick -= 1
            alpha = self.alphaTick / 30.0
            self.tipsImg.SetAlpha(alpha)
            self.tipsLabel.SetAlpha(alpha)

    # todo:====================================== Basic Function =======================================================

    def ShowItemTipsBox(self, itemDict):
        if _is_empty_item(itemDict):
            return
        name = itemDict['newItemName']
        aux = itemDict.get('newAuxValue', 0)
        if aux == -1:
            aux = 0
        userData = itemDict.get('userData')
        text = _PlayerItemComp.GetItemFormattedHoverText(name, aux, True, userData)
        self.ShowTipsBox(text)

    def ShowTipsBox(self, text):
        # 显示文本框
        self.SetScreenVisible(True)
        self.alphaTick = 0
        self.tipsImg.SetAlpha(1.0)
        self.tipsLabel.SetAlpha(1.0)
        self.tipsLabel.SetText(text)
        # 取消正在执行的timer
        if self.timer1:
            _PlayerGameComp.CancelTimer(self.timer1)
        if self.timer2:
            _PlayerGameComp.CancelTimer(self.timer2)
        # 一秒后执行渐出动画
        def func1():
            self.alphaTick = 30
            self.timer1 = None
        self.timer1 = _PlayerGameComp.AddTimer(1, func1)
        # 两秒后隐藏文本框并恢复初始状态
        def func2():
            self.HideItemTipsBox()
            self.timer2 = None
        self.timer2 = _PlayerGameComp.AddTimer(2, func2)

    def HideItemTipsBox(self):
        if self.timer1:
            _PlayerGameComp.CancelTimer(self.timer1)
            self.timer1 = None
        if self.timer2:
            _PlayerGameComp.CancelTimer(self.timer2)
            self.timer2 = None
        self.alphaTick = 0
        self.tipsImg.SetAlpha(1.0)
        self.tipsLabel.SetAlpha(1.0)
        self.SetScreenVisible(False)

















