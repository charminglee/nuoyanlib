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
#
#
# import mod.client.extraClientApi as _client_api
# from ..._core._client._comp import (
#     LvComp as _LvComp,
# )
# from ...utils.item import (
#     is_empty_item as _is_empty_item,
# )
# from ..._core._logging import log as _log
#
#
# __all__ = [
#     "ItemTipsBox",
# ]
#
#
# _NAMESPACE = "NuoyanItemGrid"
# _TIPS_PANEL_NAME = "ny_tips_panel"
# _UI_NAME_ITEM_TIPS_BOX = _NAMESPACE + "." + _TIPS_PANEL_NAME
# _ANIM_NAME = "ny_tips_panel_alpha_anim"
# _UI_PATH_TIPS_BG = "/image"
# _UI_PATH_TIPS_LABEL = "/image/label"
#
#
# _client_api.RegisterUIAnimations({
#     'namespace': _NAMESPACE,
#     _ANIM_NAME: {
#         'anim_type': "alpha",
#         'duration': 1.0,
#         'from': 1.0,
#         'to': 1.0,
#         'next': "@%s.ny_tips_panel_alpha_pre_anim" % _NAMESPACE
#     },
#     'ny_tips_panel_alpha_pre_anim': {
#         'anim_type': "alpha",
#         'duration': 1.0,
#         'from': 1.0,
#         'to': 0.0,
#     },
# })
#
#
# class ItemTipsBox(object):
#     """
#     为原版ScreenNode提供物品悬浮文本显示支持。
#     """
#
#     def __init__(self, screen_node):
#         self.__screen_node = screen_node
#         self.item_tips_panel = None
#         self.item_tips_bg = None
#         self.item_tips_label = None
#         self.__follow = False
#         self.__orig_pos = None
#
#     def Create(self):
#         self.item_tips_panel = self.__screen_node.CreateChildControl(_UI_NAME_ITEM_TIPS_BOX, _TIPS_PANEL_NAME)
#         self.__orig_pos = self.item_tips_panel.GetPosition()
#         self.item_tips_panel.SetLayer(10000)
#         self.item_tips_panel.SetAnimation("alpha", _NAMESPACE, _ANIM_NAME)
#         self.item_tips_bg = self.item_tips_panel.GetChildByPath(_UI_PATH_TIPS_BG).asImage()
#         self.item_tips_label = self.item_tips_panel.GetChildByPath(_UI_PATH_TIPS_LABEL).asLabel()
#         self.item_tips_panel.SetVisible(False)
#         _log("Created: %s" % self.__class__.__module__, ItemTipsBox)
#
#     def Update(self):
#         # 文本框跟随
#         if self.__follow:
#             self._update_pos()
#
#     def _update_pos(self):
#         if not self.item_tips_panel:
#             return
#         pos = _LvComp.ActorMotion.GetMousePosition() or _client_api.GetTouchPos()
#         if pos:
#             self.item_tips_panel.SetPosition(pos)
#
#     def ShowItemHoverTipsBox(self, item_dict, show_category=True, show_user_data=True, follow=False):
#         """
#         | 根据物品信息字典显示悬浮文本框。
#
#         -----
#
#         :param dict item_dict: 物品信息字典
#         :param bool show_category: 是否显示创造栏分类，默认为True
#         :param bool show_user_data: 显示内容是否包含UserData，默认为True
#         :param bool follow: 是否跟随鼠标指针或手指位置，默认为False
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if _is_empty_item(item_dict):
#             return False
#         name = item_dict['newItemName']
#         aux = item_dict.get('newAuxValue', 0)
#         user_data = item_dict.get('userData') if show_user_data else None
#         text = _LvComp.Item.GetItemFormattedHoverText(name, aux, show_category, user_data)
#         if not text:
#             return False
#         return self.ShowHoverTipsBox(text, follow)
#
#     def ShowHoverTipsBox(self, text, follow=False):
#         """
#         | 显示自定义内容的悬浮文本框。
#
#         -----
#
#         :param str text: 文本内容
#         :param bool follow: 是否跟随鼠标指针或手指位置，默认为False
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         self.item_tips_label.SetText(text)
#         self.item_tips_panel.StopAnimation("alpha")
#         if follow:
#             self._update_pos()
#         else:
#             self.item_tips_panel.SetPosition(self.__orig_pos)
#             self.item_tips_panel.PlayAnimation("alpha")
#         self.item_tips_panel.SetVisible(True)
#         self.__follow = follow
#         return True
#
#     def HideHoverTipsBox(self):
#         """
#         | 立即隐藏悬浮文本框。
#
#         -----
#
#         :return: 无
#         :rtype: None
#         """
#         self.item_tips_panel.SetVisible(False)
#         self.__follow = False
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
