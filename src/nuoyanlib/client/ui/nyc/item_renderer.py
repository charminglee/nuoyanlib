# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core import error
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyItemRenderer",
]


class NyItemRenderer(NyControl):
    """
    物品渲染器控件类。

    示例
    ----

    >>> self.item_renderer = nyl.NyItemRenderer(self, "/panel/item_renderer")
    >>> self.item_renderer.item = "minecraft:diamond", 0
    >>> self.item_renderer.is_enchanted = True

    参见
    ----

    - ``NyItemRenderer.item`` -- 获取/设置物品渲染器显示的物品的 identifier 和特殊值。
    - ``NyItemRenderer.is_enchanted`` -- 获取/设置物品渲染器显示的物品是否附魔。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该物品渲染器控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.ITEM_RENDERER

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def item(self):
        """
        [可读写属性]

        物品渲染器显示的物品的 identifier 和特殊值。

        :rtype: tuple[str,int]
        """
        item = self._base_control.GetUiItem()
        return item.get('itemName', ""), item.get('auxValue', 0)

    @item.setter
    def item(self, val):
        """
        [可读写属性]

        物品渲染器显示的物品的 identifier 和特殊值。

        :type val: tuple[str,int]
        """
        self._base_control.SetUiItem(val[0], val[1], self.is_enchanted)

    @property
    def is_enchanted(self):
        """
        [可读写属性]

        物品渲染器显示的物品是否附魔。

        :rtype: bool
        """
        return self._base_control.GetUiItem().get('isEnchanted', False)

    @is_enchanted.setter
    def is_enchanted(self, val):
        """
        [可读写属性]

        物品渲染器显示的物品是否附魔。

        :type val: bool
        """
        item = self.item
        self._base_control.SetUiItem(item[0], item[1], val)

    @property
    def user_data(self):
        """
        [只写属性]

        设置物品渲染器显示的物品的 UserData 。

        :rtype: None
        """
        raise error.GetPropertyError("user_data")

    @user_data.setter
    def user_data(self, val):
        """
        [只写属性]

        设置物品渲染器显示的物品的 UserData 。

        :type val: dict|None
        """
        item = self.item
        self._base_control.SetUiItem(item[0], item[1], self.is_enchanted, val)

    # endregion

    # region Compatibility =============================================================================================

    set_ui_item = SetUiItem = lambda s, *a, **k: s._base_control.SetUiItem(*a, **k)
    get_ui_item = GetUiItem = lambda s, *a, **k: s._base_control.GetUiItem(*a, **k)

    # endregion





