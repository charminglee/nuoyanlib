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
#   Last Modified : 2024-01-15
#
# ====================================================


import mod.client.extraClientApi as _api
from ...utils.item import is_empty_item as _is_empty_item
from ..comp import (
    LvComp as _LvComp,
    ScreenNode as _ScreenNode,
    CLIENT_ENGINE_NAMESPACE as _CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME as _CLIENT_ENGINE_SYSTEM_NAME,
)
from ...config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
)


__all__ = [
    "ItemTipsBox",
]


_TIPS_PANEL_NAME = "ny_tips_panel"
_UI_NAME_ITEM_TIPS_BOX = "NyItemTipsBox." + _TIPS_PANEL_NAME


class ItemTipsBox(_ScreenNode):
    """
    为原版ScreenNode提供物品悬浮文本显示支持。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(ItemTipsBox, self).__init__(namespace, name, param)
        self._alpha_tick = 0
        self._tips_img = None
        self._tips_panel = None
        self._tips_label = None
        self.__timer1 = None
        self.__timer2 = None
        self.__cs = _api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        self.__listen()

    def __listen(self):
        self.__cs.ListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "OnScriptTickClient", self, self._OnTickItemTipsBox
        )

    def Create(self):
        """
        *[event]*

        UI生命周期函数，当UI创建成功时调用。

        若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：

        >>> class MyUI(ItemTipsBox):
        ...     def Create(self):
        ...         super(MyUI, self).Create()

        -----

        :return: 无
        :rtype: None
        """
        # noinspection PySuperArguments
        super(ItemTipsBox, self).Create()
        self._tips_panel = self.CreateChildControl(_UI_NAME_ITEM_TIPS_BOX, _TIPS_PANEL_NAME)
        self._tips_img = self._tips_panel.GetChildByName("image").asImage()
        self._tips_label = self._tips_img.GetChildByName("label").asLabel()
        self._tips_panel.SetVisible(False)

    def Destroy(self):
        """
        *[event]*

        UI生命周期函数，当UI销毁时调用。

        若重写了该方法，请调用一次父类的同名方法。如：

        >>> class MyUI(ItemTipsBox):
        ...     def Destroy(self):
        ...         super(MyUI, self).Destroy()

        -----

        :return: 无
        :rtype: None
        """
        # noinspection PySuperArguments
        super(ItemTipsBox, self).Destroy()
        self.__cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "OnScriptTickClient",
            self, self._OnTickItemTipsBox
        )

    def _OnTickItemTipsBox(self):
        # 透明度动画
        if self._alpha_tick:
            self._alpha_tick -= 1
            alpha = self._alpha_tick / 30.0
            self._tips_img.SetAlpha(alpha)
            self._tips_label.SetAlpha(alpha)

    def ShowItemHoverTipsBox(self, item_dict):
        """
        根据物品信息显示悬浮文本框。

        -----

        :param dict item_dict: 物品信息字典

        :return: 无
        :rtype: None
        """
        if _is_empty_item(item_dict):
            return
        name = item_dict['newItemName']
        aux = item_dict.get('newAuxValue', 0)
        if aux == -1:
            aux = 0
        user_data = item_dict.get('userData')
        text = _LvComp.Item.GetItemFormattedHoverText(name, aux, True, user_data)
        self.ShowTipsBox(text)

    def ShowTipsBox(self, text):
        """
        显示自定义内容的悬浮文本框。

        -----

        :param str text: 文本内容

        :return: 无
        :rtype: None
        """
        # 显示文本框
        self._tips_panel.SetVisible(True)
        self._alpha_tick = 0
        self._tips_img.SetAlpha(1.0)
        self._tips_label.SetAlpha(1.0)
        self._tips_label.SetText(text)
        # 取消正在执行的timer
        if self.__timer1:
            _LvComp.Game.CancelTimer(self.__timer1)
        if self.__timer2:
            _LvComp.Game.CancelTimer(self.__timer2)
        # 一秒后执行渐出动画
        def func1():
            self._alpha_tick = 30
            self.__timer1 = None
        self.__timer1 = _LvComp.Game.AddTimer(1, func1)
        # 两秒后隐藏文本框并恢复初始状态
        def func2():
            self.HideTipsBox()
            self.__timer2 = None
        self.__timer2 = _LvComp.Game.AddTimer(2, func2)

    def HideTipsBox(self):
        """
        立即隐藏悬浮文本框。

        -----

        :return: 无
        :rtype: None
        """
        if self.__timer1:
            _LvComp.Game.CancelTimer(self.__timer1)
            self.__timer1 = None
        if self.__timer2:
            _LvComp.Game.CancelTimer(self.__timer2)
            self.__timer2 = None
        self._alpha_tick = 0
        self._tips_img.SetAlpha(1.0)
        self._tips_label.SetAlpha(1.0)
        self._tips_panel.SetVisible(False)


















