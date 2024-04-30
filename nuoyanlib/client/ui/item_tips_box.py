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
#   Last Modified : 2024-04-28
#
# ====================================================


import mod.client.extraClientApi as _api
from ...utils.item import is_empty_item as _is_empty_item
from ..comp import (
    LvComp as _LvComp,
    ScreenNode as _ScreenNode,
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
        super(ItemTipsBox, self).__init__(namespace, name, param)
        self.__screen_node = param['_screen_node'] if param and '_screen_node' in param else self
        self._alpha_tick = 0
        self.item_tips_bg = None
        self.item_tips_panel = None
        self.item_tips_label = None
        self.__timer1 = None
        self.__timer2 = None
        self.__follow = False
        self.__path = ""

    def Create(self):
        """
        *[event]*

        | UI生命周期函数，当UI创建成功时调用。
        | 若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：
        ::

            class MyUI(ItemTipsBox):
                def Create(self):
                    super(MyUI, self).Create()

        -----

        :return: 无
        :rtype: None
        """
        super(ItemTipsBox, self).Create()
        self.item_tips_panel = self.__screen_node.GetBaseUIControl(self.__path)
        if not self.__path or not self.item_tips_panel:
            self.item_tips_panel = self.__screen_node.CreateChildControl(_UI_NAME_ITEM_TIPS_BOX, _TIPS_PANEL_NAME)
            self.__path = self.item_tips_panel.GetPath()
        self.item_tips_bg = self.item_tips_panel.GetChildByName("image").asImage()
        self.item_tips_label = self.item_tips_bg.GetChildByName("label").asLabel()
        self.item_tips_panel.SetVisible(False)

    def Update(self):
        """
        *[tick]* *[event]*

        | 客户端每帧调用。
        | 若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：
        ::

            class MyUI(ItemTipsBox):
                def Update(self):
                    super(MyUI, self).Update()

        -----

        :return: 无
        :rtype: None
        """
        super(ItemTipsBox, self).Update()
        if self.__follow and self.item_tips_panel:
            pos = _LvComp.ActorMotion.GetMousePosition() or _api.GetTouchPos()
            if pos:
                self.item_tips_panel.SetPosition(pos)
        # 透明度动画
        if self._alpha_tick:
            self._alpha_tick -= 1
            alpha = self._alpha_tick / 30.0
            self.item_tips_bg.SetAlpha(alpha)
            self.item_tips_label.SetAlpha(alpha)

    def ShowItemHoverTipsBox(self, item_dict):
        """
        | 根据物品信息显示悬浮文本框。

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

    def ShowTipsBox(self, text, follow=False):
        """
        | 显示自定义内容的悬浮文本框。

        -----

        :param str text: 文本内容
        :param bool follow: 是否跟随鼠标指针或手指位置

        :return: 无
        :rtype: None
        """
        # 显示文本框
        self.item_tips_panel.SetVisible(True)
        self._alpha_tick = 0
        self.item_tips_bg.SetAlpha(1.0)
        self.item_tips_label.SetAlpha(1.0)
        self.item_tips_label.SetText(text)
        # 取消正在执行的timer
        if self.__timer1:
            _LvComp.Game.CancelTimer(self.__timer1)
        if self.__timer2:
            _LvComp.Game.CancelTimer(self.__timer2)
        if not follow:
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
        else:
            self.__follow = True

    def HideTipsBox(self):
        """
        | 立即隐藏悬浮文本框。

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
        self.item_tips_bg.SetAlpha(1.0)
        self.item_tips_label.SetAlpha(1.0)
        self.item_tips_panel.SetVisible(False)
        self.__follow = False


















