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
# from ...utils.item import (
#     is_empty_item as _is_empty_item,
# )
# from ..._core._logging import log as _log
#
#
# __all__ = [
#     "ItemFlyAnim",
# ]
#
#
# _NAMESPACE = "NuoyanItemGrid"
# _ITEM_FLY_PANEL_NAME = "ny_item_fly_panel"
# _UI_NAME_ITEM_FLY_PANEL = _NAMESPACE + "." + _ITEM_FLY_PANEL_NAME
# _UI_PATH_FLY_ITEM_0 = "/%s/0" % _ITEM_FLY_PANEL_NAME
#
#
# class ItemFlyAnim(object):
#     """
#     为原版ScreenNode提供物品飞行动画支持。
#     """
#
#     def __init__(self, screen_node):
#         self.__screen_node = screen_node
#         self._item_fly_queue = []
#         self._fly_ir = []
#         self.item_fly_panel = None
#
#     def Create(self):
#         self.item_fly_panel = self.__screen_node.CreateChildControl(_UI_NAME_ITEM_FLY_PANEL, _ITEM_FLY_PANEL_NAME)
#         self._fly_ir.append(self.item_fly_panel.GetChildByPath("/0").asItemRenderer())
#         self._fly_ir.append(self.item_fly_panel.GetChildByPath("/1").asItemRenderer())
#         _log("Created: %s" % self.__class__.__module__, ItemFlyAnim)
#
#     def _clone_new_ir(self):
#         name = str(len(self._fly_ir))
#         if self.__screen_node.Clone(_UI_PATH_FLY_ITEM_0, "/" + _ITEM_FLY_PANEL_NAME, name):
#             ir = self.__screen_node.GetBaseUIControl("/%s/%s" % (_ITEM_FLY_PANEL_NAME, name)).asItemRenderer()
#             self._fly_ir.append(ir)
#             return ir
#         else:
#             _log("Clone new ItemRenderer failed", ItemFlyAnim, "ERROR")
#
#     def _get_idle_ir_index(self):
#         for i in range(len(self._fly_ir)):
#             if i not in self._item_fly_queue:
#                 return i
#
#     def PlayItemFlyAnim(self, item_dict, from_pos, to_pos, ui_size):
#         """
#         | 播放物品飞行动画。
#
#         -----
#
#         :param dict item_dict: 物品信息字典
#         :param tuple[float,float] from_pos: 动画起点坐标（全局坐标）
#         :param tuple[float,float] to_pos: 动画终点坐标（全局坐标）
#         :param float|tuple[float,float] ui_size: 物品图标尺寸，传入float时，图标长宽均设置为该值，传入tuple时，图标长宽设置为该元组对应值
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if _is_empty_item(item_dict, False):
#             return False
#         # ItemRenderer不够用时克隆出新的ItemRenderer，否则使用空闲的ItemRenderer
#         queue_len = len(self._item_fly_queue)
#         ui_count = len(self._fly_ir)
#         if queue_len >= ui_count:
#             ir = self._clone_new_ir()
#             if not ir:
#                 return False
#             index = ui_count
#         else:
#             index = self._get_idle_ir_index()
#             if index is None:
#                 return False
#             ir = self._fly_ir[index]
#         # 配置ItemRenderer
#         item_name = item_dict['newItemName']
#         aux = item_dict.get('newAuxValue', 0)
#         enchanted = bool(item_dict.get('enchantData') or item_dict.get('modEnchantData'))
#         user_data = item_dict.get('userData')
#         ir.SetUiItem(item_name, aux, enchanted, user_data)
#         ir.SetVisible(True)
#         ir.SetSize(ui_size if isinstance(ui_size, tuple) else (ui_size, ui_size), True)
#         # 设置动画
#         anim_name = "item_fly_anim_%d" % index
#         _client_api.RegisterUIAnimations({
#             'namespace': _NAMESPACE,
#             anim_name: {
#                 'anim_type': "offset",
#                 'duration': 0.125,
#                 'from': from_pos,
#                 'to': to_pos,
#             },
#         })
#         if ir.IsAnimEndCallbackRegistered(anim_name):
#             ir.RemoveAnimation("offset")
#         if not ir.SetAnimation("offset", _NAMESPACE, anim_name, True):
#             _log("SetAnimation failed", ItemFlyAnim, "ERROR")
#             return False
#         def anim_end():
#             ir.SetVisible(False)
#             self._item_fly_queue.remove(index)
#         ir.SetAnimEndCallback(anim_name, anim_end)
#         self._item_fly_queue.append(index)
#         return True
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
