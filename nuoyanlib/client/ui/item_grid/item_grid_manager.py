# # -*- coding: utf-8 -*-
# # ====================================================
# #
# #   Copyright (c) 2023 Nuoyan
# #   nuoyanlib is licensed under Mulan PSL v2.
# #   You can use this software according to the terms and conditions of the Mulan PSL v2.
# #   You may obtain a copy of Mulan PSL v2 at:
# #            http://license.coscl.org.cn/MulanPSL2
# #   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# #   See the Mulan PSL v2 for more details.
# #
# #   Author        : 诺言Nuoyan
# #   Email         : 1279735247@qq.com
# #   Gitee         : https://gitee.com/charming-lee
# #   Last Modified : 2025-03-26
# #
# # ====================================================
#
#
# """
#
# item_grid_manager
# =================
# 该模块提供了物品网格的Python实现。将自定义UI类继承 ``ItemGridManager`` ，即可轻松实现一个功能完备的背包UI。
#
# -----
#
# 【名词解释】
#
# - 网格：即Grid控件，一种能够对模板控件多次克隆并排列成网状的控件。
# - 方格：即网格的单个子控件，也称为网格的元素，本质上是个按钮控件。
# - 网格的key：在 ``ItemGridManager`` 中，每个网格都有一个唯一的key，数据类型为字符串，可自定义，或使用预设的key来启用特定功能。
# - 方格索引：类似于物品栏槽位，从0开始，网格的第一个方格的索引为0，第二个为1，以此类推，从左到右从上到下递增。
# - 方格位置元组：用于表示指定方格，由两个元素组成：(方格所在网格的key, 方格索引)。
# - 方格路径：即方格控件的UI路径。
# - 分堆数据字典：保存了当前物品分堆数据的字典。
# ::
#
#     +----------------+----------------------+--------------------+
#     |     字典键      |        数据类型       |        解释         |
#     +================+======================+====================+
#     |    item_dict   |         dict         |     物品信息字典     |
#     +----------------+----------------------+--------------------+
#     |   cell_path    |         str          |      方格的路径      |
#     +----------------+----------------------+--------------------+
#     |   cell_pos     |    Tuple[str, int]   |     方格位置元组     |
#     +----------------+----------------------+--------------------+
#     | selected_count |         int          | 当前分堆选中的物品数量 |
#     +----------------+----------------------+--------------------+
#     |   animating    |         bool         | 分堆进度条动画是否运行 |
#     +----------------+----------------------+--------------------+
#     |    bar_ctrl    | ProgressBarUIControl |  分堆进度条控件实例   |
#     +----------------+----------------------+--------------------+
#
# * 选中数据字典：保存了当前选中物品的数据的字典。
# ::
#
#     +-----------+-----------------+--------------------+
#     |   字典键   |     数据类型     |        解释         |
#     +===========+=================+====================+
#     | item_dict |      dict       |     物品信息字典     |
#     +-----------+-----------------+--------------------+
#     | cell_path |       str       |    选中方格的路径    |
#     +-----------+-----------------+--------------------+
#     | cell_pos  | Tuple[str, int] |  选中的方格位置元组   |
#     +-----------+-----------------+--------------------+
#
# -----
#
# 【使用方法】
#
# | 1、将您的客户端继承 ``NuoyanClientSystem`` ，此后无需再继承 ``ClientSystem`` 。
# | 2、在客户端使用接口 ``RegisterItemGrid`` 注册一个物品网格。
# | 3、将您的UI类继承 ``ItemGridManager`` ，此后无需再继承 ``ScreenNode`` ，然后在客户端正常注册与创建您的UI。
# | 4、网格第一次显示时，调用 ``self.InitItemGrids`` 对网格进行初始化，第二次显示时无需再次调用该接口。网格何时第一次显示取决于您的设置，如果您的网格在创建UI时就立即显示，则在 ``Create`` 方法内执行上述初始化操作即可。
# | 5、完成上述步骤后您就可以调用其他接口对网格进行操作，如设置网格物品、设置指定位置物品的数量等。
#
# -----
#
# 【注意事项】
#
# | 1、如果您的UI类重写了 ``Update`` 方法，请在该方法内调用一次父类同名方法，例如： ``super(你的UI类, self).Update()`` 或 ``ItemGridManager.Update()`` 。
#
# """
#
#
# from mod.common.minecraftEnum import ItemPosType as _ItemPosType
# from ..._core._const import (
#     LIB_NAME as _LIB_NAME,
#     LIB_SERVER_NAME as _LIB_SERVER_NAME,
#     SHORTCUT as _SHORTCUT,
#     INV27 as _INV27,
#     INV36 as _INV36,
# )
# from ..._core._client._comp import (
#     LvComp as _LvComp,
#     PLAYER_ID as _PLAYER_ID,
#     ENGINE_NAMESPACE as _ENGINE_NAMESPACE,
#     ENGINE_SYSTEM_NAME as _ENGINE_SYSTEM_NAME,
# )
# from ..._core._client._lib_client import (
#     instance as _instance,
# )
# from ..._core._listener import (
#     event as _event,
#     lib_sys_event as _lib_sys_event,
# )
# from ...utils.item import (
#     is_same_item as _is_same_item,
#     is_empty_item as _is_empty_item,
#     get_max_stack as _get_max_stack,
#     deepcopy_item_dict as _deepcopy_item_dict,
# )
# from .ui_utils import (
#     get_direct_children_path as _get_direct_children_path,
# )
# from ..._core._logging import log as _log
#
#
# __all__ = [
#     "ItemGridManager",
# ]
#
#
# _IMAGE_PATH_ITEM_CELL_SELECTED = "textures/ui/recipe_book_button_borderless_lightpressed"
# _IMAGE_PATH_ITEM_CELL_DEFAULT = "textures/ui/cell_image"
# _UI_PATH_COUNT = "/count"
# _UI_PATH_ITEM_RENDERER = "/item_renderer"
# _UI_PATH_DURABILITY = "/durability"
# _UI_PATH_DEFAULT = "/default"
# _UI_PATH_HEAP = "/heap"
# _UI_PATH_ITEM_BG = "/item_bg"
#
#
# _INV_POS_TYPE = _ItemPosType.INVENTORY
#
#
# class ItemGridManager(object):
#     """
#     物品网格管理器，实现了类似于原版背包的诸多物品功能。
#     """
#
#     def __init__(self, nuoyan_screen_node, item_fly_anim, item_tips_box):
#         self.__lib_sys = _instance()
#         self.__nsn_ins = nuoyan_screen_node
#         self.__ifa_ins = item_fly_anim
#         self.__itb_ins = item_tips_box
#         self.__screen_node = self.__nsn_ins._ScreenNodeExtension__screen_node
#         self._item_heap_data = {}
#         self._selected_item = {}
#         self._cell_paths = {}
#         self._cell_poses = {}
#         self._cell_ui_ctrls = {}
#         self._locked_cells = set()
#         self._locked_grids = set()
#         self.__move_in_cell_list = []
#         self.__src_item = None
#         self._inited_keys = set()
#         self._inv36_keys = set()
#         self._inv27_keys = set()
#         self._shortcut_keys = set()
#         self.__tick = 0
#         self.__cancel_hide_tips = 0
#         _log("Inited: %s" % self.__class__.__module__, ItemGridManager)
#
#     # System Event Callbacks ===========================================================================================
#
#     def Destroy(self):
#         self.__lib_sys.UnListenForEvent(
#             _ENGINE_NAMESPACE, _ENGINE_SYSTEM_NAME, "GetEntityByCoordReleaseClientEvent",
#             self, self._on_get_entity_by_coord_release
#         )
#         self.__lib_sys.UnListenForEvent(
#             _LIB_NAME, _LIB_SERVER_NAME, "_UpdateItemGrids", self, self._on_update_item_grids
#         )
#
#     def Update(self):
#         # 物品分堆
#         self.__tick += 1
#         if self._item_heap_data and self._item_heap_data['animating']:
#             count = self._item_heap_data['item_dict']['count']
#             if count > 1:
#                 tick = round(45.0 / (count - 1))
#                 if tick < 1:
#                     tick = 1
#                 if not self.__tick % tick and self._item_heap_data['selected_count'] < count:
#                     self._item_heap_data['selected_count'] += 1
#                     bar_ctrl = self._item_heap_data['bar_ctrl']
#                     bar_ctrl.SetValue(float(self._item_heap_data['selected_count']) / count)
#
#     @_event("GetEntityByCoordReleaseClientEvent")
#     def _on_get_entity_by_coord_release(self, args):
#         if len(self.__move_in_cell_list) >= 2:
#             self.SetSelectedItemData(self._selected_item['cell_path'], False)
#         self.__move_in_cell_list = []
#         self.__src_item = None
#
#     @_lib_sys_event("_UpdateItemGrids")
#     def _on_update_item_grids(self, args):
#         data = args['data']
#         update_inv = args['update_inv']
#         for key, item_list in data.items():
#             if self._is_grid_inited(key):
#                 self._set_grid_ui_item(key, item_list)
#         if update_inv:
#             self._update_inv_grids(update_inv)
#         _log("Updated item grids: %s" % (data.keys() + update_inv), ItemGridManager)
#
#     @_event("InventoryItemChangedClientEvent")
#     def _on_inv_item_changed(self, args):
#         player_id = args['playerId']
#         slot = args['slot']
#         item_dict = args['newItemDict']
#         if player_id != _PLAYER_ID:
#             return
#         # 背包物品变化时同步更新UI
#         for k in self._inv36_keys:
#             self._set_cell_ui_item((k, slot), item_dict)
#         if slot >= 9:
#             for k in self._inv27_keys:
#                 self._set_cell_ui_item((k, slot - 9), item_dict)
#         else:
#             for k in self._shortcut_keys:
#                 self._set_cell_ui_item((k, slot), item_dict)
#
#     # New Event Callbacks ==============================================================================================
#
#     def OnMoveItemsBefore(self, args):
#         """
#         | 物品发生移动前触发。
#
#         -----
#
#         | 【from_path: str】 起始位置的方格路径
#         | 【to_path: str】 终点位置的方格路径
#         | 【from_pos: Tuple[str, int]】 起始位置的方格位置元组
#         | 【to_pos: Tuple[str, int]】 终点位置的方格位置元组
#         | 【$move_count: int】 移动数量，可修改
#         | 【$fly_anim: bool】 是否播放物品飞行动画，设置为False则不会显示物品飞行动画
#         | 【$force: bool】 是否强制移动，若设置为True，则本次移动会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品
#         | 【$cancel: bool】 是否取消本次移动，设置为True即可取消
#
#         -----
#
#         :param dict args: 参数字典，参数解释见上方
#
#         :return: 无
#         :rtype: None
#         """
#
#     def OnItemGridSelectOrUnselectItem(self, args):
#         """
#         | 网格内的物品被选中或取消选中时触发。
#
#         -----
#
#         | 【item_dict: dict】 物品信息字典
#         | 【cell_path: str】 方格路径
#         | 【cell_pos: Tuple[str, int]】 方格位置元组
#         | 【$cancel: bool】 是否取消本次操作
#         | 【selected: bool】 物品被选中时为True，取消选中时为False
#
#         -----
#
#         :param dict args: 参数字典，参数解释见上方
#
#         :return: 无
#         :rtype: None
#         """
#
#     # Basic Functions ==================================================================================================
#
#     @property
#     def _grid_path(self):
#         return self.__lib_sys.item_grid_path
#
#     @property
#     def _grid_size(self):
#         return self.__lib_sys.item_grid_size
#
#     @property
#     def _grid_items(self):
#         return self.__lib_sys.item_grid_items
#
#     @property
#     def _registered_keys(self):
#         cls = self.__nsn_ins.__class__
#         return self.__lib_sys.registered_keys[cls.__module__ + "." + cls.__name__]
#
#     def _parse_keys(self, keys):
#         if not keys:
#             return tuple(self._inited_keys)
#         elif isinstance(keys, str):
#             return (keys,) if self._is_grid_inited(keys) else ()
#         return self._filter_inited_keys(keys)
#
#     def _filter_registered_keys(self, keys):
#         return filter(lambda k: k in self._registered_keys, keys)
#
#     def _filter_inited_keys(self, keys):
#         return filter(self._is_grid_inited, keys)
#
#     def _is_inv_key(self, *keys):
#         return all(k in self._inv36_keys or k in self._inv27_keys or k in self._shortcut_keys for k in keys)
#
#     def _is_inv36_key(self, key):
#         return key in self._inv36_keys
#
#     def _is_inv27_key(self, key):
#         return key in self._inv27_keys
#
#     def _is_shortcut_key(self, key):
#         return key in self._shortcut_keys
#
#     def _is_cell_exist(self, *cell):
#         return all(self.GetItemCellPos(c) in self._cell_paths for c in cell)
#
#     def InitItemGrids(self, keys=None, callback=None):
#         """
#         | 初始化网格。初始化前请先使用 ``RegisterItemGrid`` 注册网格。
#         | 由于Grid的渲染机制，该接口需要在网格显示在屏幕上时调用才有效。
#
#         -----
#
#         :param str|tuple[str]|None keys: 网格的key，多个网格可使用元组，传入None时表示所有已注册网格；默认为None
#         :param function|None callback: 初始化完成后调用的函数，默认为None；该函数需要接受两个参数：第一个参数为keys，网格的key的元组；第二个参数为result，初始化结果元组，与keys一一对应，成功为True，失败为False
#
#         :return: 无
#         :rtype: None
#         """
#         if not keys:
#             keys = self._registered_keys
#         elif isinstance(keys, str):
#             keys = (keys,)
#         _LvComp.Game.AddTimer(0, self._init_item_grids, keys, callback)
#
#     def _init_item_grids(self, keys, callback):
#         res = []
#         valid_keys = []
#         for key in keys:
#             if key not in self._registered_keys:
#                 res.append(False)
#                 continue
#             grid_path, is_single = self._grid_path[key]
#             grid_size = self._grid_size[key]
#             # 获取网格所有直接子控件的路径
#             if is_single:
#                 all_children = [grid_path]
#             else:
#                 all_children = _get_direct_children_path(grid_path, self.__screen_node)
#             if len(all_children) != grid_size:
#                 res.append(False)
#                 continue
#             # 初始化操作
#             cell_poses = {}
#             cell_paths = {}
#             cell_ui_ctrls = {}
#             for i, path in enumerate(all_children):
#                 btn = self.__screen_node.GetBaseUIControl(path)
#                 if not btn:
#                     res.append(False)
#                     break
#                 btn = btn.asButton()
#                 btn.AddHoverEventParams()
#                 btn.SetButtonTouchMoveInCallback(self._on_item_cell_touch_move_in)
#                 btn.SetButtonTouchMoveCallback(self.OnItemCellTouchMove)
#                 btn.SetButtonHoverInCallback(self._on_item_cell_hover_in)
#                 btn.SetButtonHoverOutCallback(self._on_item_cell_hover_out)
#                 self.__nsn_ins.SetButtonDoubleClickCallback(
#                     path,
#                     self._on_item_cell_double_click,
#                     self._on_item_cell_touch_up,
#                 )
#                 self.__nsn_ins.SetButtonLongClickCallback(
#                     path,
#                     self._on_item_cell_long_click,
#                     self._on_item_cell_touch_up,
#                     self.OnItemCellTouchMoveOut,
#                     self._on_item_cell_touch_down,
#                     self.OnItemCellTouchCancel,
#                 )
#                 btn.GetChildByPath(_UI_PATH_HEAP).SetVisible(False)
#                 pos = (key, i)
#                 self.SetItemCellRenderer(pos)
#                 self.SetItemCellCountLabel(pos)
#                 self.SetItemCellDurabilityBar(pos)
#                 cell_poses[path] = pos
#                 cell_paths[pos] = path
#                 cell_ui_ctrls[pos] = btn
#             else:
#                 self._cell_poses.update(cell_poses)
#                 self._cell_paths.update(cell_paths)
#                 self._cell_ui_ctrls.update(cell_ui_ctrls)
#                 self._inited_keys.add(key)
#                 if key.endswith(_INV36):
#                     self._inv36_keys.add(key)
#                 elif key.endswith(_INV27):
#                     self._inv27_keys.add(key)
#                 elif key.endswith(_SHORTCUT):
#                     self._shortcut_keys.add(key)
#                 res.append(True)
#                 valid_keys.append(key)
#         if valid_keys:
#             self._update_inv_grids(valid_keys)
#             self.__lib_sys.NotifyToServer("_OnClientItemGridInitFinished", {'keys': valid_keys})
#         if callback:
#             callback(keys, tuple(res))
#
#     def _is_grid_inited(self, key):
#         return key in self._inited_keys
#
#     def AllItemGridsInited(self, keys=None):
#         """
#         | 判断网格是否完成初始化。
#
#         -----
#
#         :param str|tuple[str]|None keys: 网格的key，多个网格可使用元组，传入None时表示所有已注册网格；默认为None
#
#         :return: 传入的所有网格均已完成初始化时返回True，否则返回False
#         :rtype: bool
#         """
#         if not keys:
#             keys = self._registered_keys
#         elif isinstance(keys, str):
#             keys = (keys,)
#         return all(self._is_grid_inited(k) for k in keys)
#
#     def GetItemGridKey(self, cell):
#         """
#
#         | 获取方格所在网格的key。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 方格所在网格的key，获取不到返回None
#         :rtype: str|None
#         """
#         if isinstance(cell, tuple):
#             key = cell[0]
#         elif cell in self._cell_poses:
#             key = self._cell_poses[cell][0]
#         else:
#             key = None
#         return key if key in self._registered_keys else None
#
#     def GetItemCellPath(self, cell):
#         """
#         | 根据方格位置元组获取方格路径。若传入方格路径，则返回其本身。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 方格路径，获取不到返回None
#         :rtype: str|None
#         """
#         if cell in self._cell_poses:
#             return cell
#         return self._cell_paths.get(cell)
#
#     def GetItemCellPos(self, cell):
#         """
#         | 根据方格路径获取方格位置元组。若传入方格位置元组，则返回其本身。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 方格位置元组，获取不到返回None
#         :rtype: tuple[str,int]|None
#         """
#         if cell in self._cell_paths:
#             return cell
#         return self._cell_poses.get(cell)
#
#     # UI Callbacks =====================================================================================================
#
#     def OnItemCellTouchUp(self, args):
#         """
#         | 方格抬起时触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_touch_up(self, args):
#         self.OnItemCellTouchUp(args)
#         bp = args['ButtonPath']
#         if self.IsItemCellLocked(bp):
#             return
#         item_dict = self._get_cell_item(bp)
#         if self._selected_item:
#             from_path = self._selected_item['cell_path']
#             count = self._item_heap_data['selected_count'] if self._item_heap_data else -1
#             self.MoveItem(from_path, bp, count)
#             self.SetSelectedItemData(from_path, False)
#         elif not _is_empty_item(item_dict):
#             self.SetSelectedItemData(bp, True)
#         self.PauseItemHeapProgressBar()
#
#     def OnItemCellTouchMoveIn(self, args):
#         """
#         | 手指移动到方格内时触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_touch_move_in(self, args):
#         self.OnItemCellTouchMoveIn(args)
#         bp = args['ButtonPath']
#         if self.IsItemCellLocked(bp):
#             return
#         if self._item_heap_data or not self._selected_item:
#             return
#         from_path = self._selected_item['cell_path']
#         item_dict = self._get_cell_item(bp)
#         if bp == from_path or not _is_empty_item(item_dict):
#             return
#         if not self.__move_in_cell_list:
#             self.__src_item = self._selected_item['item_dict']
#         if bp not in self.__move_in_cell_list:
#             self.__move_in_cell_list.append(bp)
#         if len(self.__move_in_cell_list) >= 2:
#             self.DivideItemEvenly(from_path, self.__move_in_cell_list, self.__src_item)
#
#     def OnItemCellDoubleClick(self, args):
#         """
#         | 双击方格触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_double_click(self, args):
#         self.OnItemCellDoubleClick(args)
#         bp = args['ButtonPath']
#         if self.IsItemCellLocked(bp):
#             return
#         if self._item_heap_data:
#             return
#         item_dict = self._get_cell_item(bp)
#         if _is_empty_item(item_dict):
#             return
#         max_stack = _get_max_stack(item_dict)
#         if item_dict['count'] < max_stack:
#             self.MergeItems(bp)
#         self.SetSelectedItemData(bp, False)
#
#     def OnItemCellLongClick(self, args):
#         """
#         | 长按方格触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_long_click(self, args):
#         self.OnItemCellLongClick(args)
#         bp = args['ButtonPath']
#         if self.IsItemCellLocked(bp):
#             return
#         item_dict = self._get_cell_item(bp)
#         if self._selected_item:
#             self.SetSelectedItemData(self._selected_item['cell_path'], False)
#         if not _is_empty_item(item_dict) and item_dict['count'] >= 2:
#             self.SetItemHeapData(bp, 1)
#             self.StartItemHeapProgressBar()
#
#     def OnItemCellTouchDown(self, args):
#         """
#         | 方格按下时触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_touch_down(self, args):
#         self.OnItemCellTouchDown(args)
#         bp = args['ButtonPath']
#         item_dict = self._get_cell_item(bp)
#         self.__itb_ins.ShowItemHoverTipsBox(item_dict)
#
#     def OnItemCellTouchMove(self, args):
#         """
#         | 手指在方格上移动时每帧触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def OnItemCellTouchMoveOut(self, args):
#         """
#         | 手指移出方格时触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def OnItemCellTouchCancel(self, args):
#         """
#         | 方格取消按下时触发的回调函数。
#
#         -----
#
#         :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同
#
#         :return: 无
#         :rtype: None
#         """
#
#     def _on_item_cell_hover_in(self, args):
#         bp = args['ButtonPath']
#         item_dict = self._get_cell_item(bp)
#         if _is_empty_item(item_dict):
#             self.__itb_ins.HideHoverTipsBox()
#         else:
#             self.__itb_ins.ShowItemHoverTipsBox(item_dict, follow=True)
#         self.__cancel_hide_tips += 1
#
#     def _on_item_cell_hover_out(self, args):
#         if self.__cancel_hide_tips == 1:
#             self.__itb_ins.HideHoverTipsBox()
#             self.__cancel_hide_tips = 0
#         else:
#             self.__cancel_hide_tips = 1
#
#     # UI Operations ====================================================================================================
#
#     def _set_cell_ui_item(self, cell, item_dict):
#         self.SetItemCellRenderer(cell, item_dict)
#         self.SetItemCellCountLabel(cell, item_dict=item_dict)
#         self.SetItemCellDurabilityBar(cell, item_dict=item_dict)
#
#     def _set_grid_ui_item(self, key, item_dict_list):
#         for i, item_dict in enumerate(item_dict_list):
#             self._set_cell_ui_item((key, i), item_dict)
#
#     def GetAllItemCellUIControls(self, key):
#         """
#         | 获取指定网格中所有方格的 ``ButtonUIControl`` 实例。
#
#         -----
#
#         :param str key: 网格的key
#
#         :return: 网格中所有方格的ButtonUIControl实例的列表，获取不到时返回空列表
#         :rtype: list[ButtonUIControl]
#         """
#         return self._cell_ui_ctrls.get(key, [])
#
#     def GetItemCellUIControl(self, cell):
#         """
#         | 获取指定方格的 ``ButtonUIControl`` 。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 指定方格的ButtonUIControl实例，获取不到时返回None
#         :rtype: ButtonUIControl|None
#         """
#         pos = self.GetItemCellPos(cell)
#         return self._cell_ui_ctrls[pos] if pos else None
#
#     def SetItemCellDurabilityBar(self, cell, val=1.0, item_dict=None, auto=False):
#         """
#         | 设置指定方格的物品耐久显示。该接口仅改变UI显示，并不实际改变该方格内物品的耐久。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param float val: 耐久度百分比，范围为[0, 1]，默认为1.0
#         :param dict|None item_dict: 物品信息字典，默认为None
#         :param bool auto: 是否自动设置，默认为False；设置为True时将忽略val和item_dict参数，根据方格的物品数据进行设置，相当于刷新作用
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         dur_ctrl = self.GetItemCellUIControl(cell).GetChildByPath(_UI_PATH_DURABILITY).asProgressBar()
#         if auto:
#             item_dict = self._get_cell_item(cell)
#         if not _is_empty_item(item_dict):
#             dur = item_dict.get('durability', 0)
#             item_name, aux = item_dict['newItemName'], item_dict.get('newAuxValue', 0)
#             basic_info = _LvComp.Item.GetItemBasicInfo(item_name, aux)
#             if not basic_info:
#                 return False
#             max_dur = basic_info['maxDurability']
#             val = float(dur) / (max_dur if max_dur > 0 else 1.0)
#         dur_ctrl.SetVisible(val < 1)
#         dur_ctrl.SetValue(val)
#         return True
#
#     def SetItemCellRenderer(self, cell, item_dict=None, auto=False):
#         """
#         | 设置指定方格的物品渲染器显示物品。该接口仅改变UI显示，并不实际改变该方格内物品。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param dict item_dict: 物品信息字典，默认为None
#         :param bool auto: 是否自动设置，默认为False，设置为True时将忽略item_dict参数，根据方格的物品数据进行设置，相当于刷新作用
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         cell = self.GetItemCellUIControl(cell)
#         ir = cell.GetChildByPath(_UI_PATH_ITEM_RENDERER).asItemRenderer()
#         item_bg = cell.GetChildByPath(_UI_PATH_ITEM_BG)
#         if auto:
#             item_dict = self._get_cell_item(cell)
#         if not _is_empty_item(item_dict):
#             ir.SetVisible(True)
#             name = item_dict['newItemName']
#             aux = item_dict.get('newAuxValue', 0)
#             is_enchanted = bool(item_dict.get('enchantData') or item_dict.get('modEnchantData'))
#             user_data = item_dict.get('userData')
#             ir.SetUiItem(name, aux, is_enchanted, user_data)
#             item_bg.SetVisible(False)
#         else:
#             ir.SetVisible(False)
#             item_bg.SetVisible(True)
#         return False
#
#     def SetItemCellCountLabel(self, cell, count=0, item_dict=None, auto=False):
#         """
#         | 设置指定方格的物品数量文本。该接口仅改变UI显示，并不实际改变该方格内物品的数量，如需设置物品数量，请使用 ``SetItemCellCount`` 。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param int count: 数量，默认为0
#         :param dict|None item_dict: 物品信息字典，默认为None
#         :param bool auto: 是否自动设置，默认为False，设置为True时将忽略count和item_dict参数，根据方格的物品数据进行设置，相当于刷新作用
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         label = self.GetItemCellUIControl(cell).GetChildByPath(_UI_PATH_COUNT).asLabel()
#         if auto:
#             item_dict = self._get_cell_item(cell)
#         count = count if _is_empty_item(item_dict) else item_dict.get('count', 1)
#         label.SetVisible(count >= 2)
#         label.SetText(str(int(count)))
#         return True
#
#     def UpdateItemGrids(self, keys=None):
#         """
#         | 刷新物品网格。
#
#         -----
#
#         :param str|tuple[str]|None keys: 网格的key，多个网格可使用元组，传入None时表示所有已初始化的网格；默认为None
#
#         :return: 无
#         :rtype: None
#         """
#         keys = self._parse_keys(keys)
#         if keys:
#             self._update_inv_grids(keys)
#             self.__lib_sys.NotifyToServer("_UpdateItemGrids", {'keys': keys})
#
#     def _update_inv_grids(self, keys):
#         inv_items = _LvComp.Item.GetPlayerAllItems(_INV_POS_TYPE, True)
#         for k in keys:
#             if self._is_inv36_key(k):
#                 self._set_grid_ui_item(k, inv_items)
#             elif self._is_inv27_key(k):
#                 self._set_grid_ui_item(k, inv_items[9:])
#             elif self._is_shortcut_key(k):
#                 self._set_grid_ui_item(k, inv_items[:9])
#
#     def ClearItemGridState(self):
#         """
#         | 清除网格状态（包括物品选中状态和长按分堆状态）。
#
#         -----
#
#         :return: 无
#         :rtype: None
#         """
#         if self._selected_item:
#             bp = self._selected_item['cell_path']
#             default_img = self.GetItemCellUIControl(bp).GetChildByPath(_UI_PATH_DEFAULT).asImage()
#             default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
#             self._selected_item.clear()
#         if self._item_heap_data:
#             self._item_heap_data['bar_ctrl'].SetVisible(False)
#             self._item_heap_data.clear()
#
#     def _set_item_fly_anim(self, item_dict, from_cell, to_cell):
#         from_ui = self.GetItemCellUIControl(from_cell)
#         from_pos = from_ui.GetGlobalPosition()
#         ui_size = from_ui.GetSize()
#         to_pos = self.GetItemCellUIControl(to_cell).GetGlobalPosition()
#         self.__ifa_ins.PlayItemFlyAnim(item_dict, from_pos, to_pos, ui_size)
#
#     def StartItemHeapProgressBar(self):
#         """
#         | 启动物品分堆进度条动画。需要先调用 ``SetItemHeapData`` 设置物品分堆数据后才有效。
#
#         -----
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._item_heap_data:
#             return False
#         self._item_heap_data['bar_ctrl'].SetVisible(True)
#         self._item_heap_data['animating'] = True
#         self.__tick = 0
#         return True
#
#     def PauseItemHeapProgressBar(self):
#         """
#         | 暂停物品分堆进度条动画。需要先调用 ``SetItemHeapData`` 设置物品分堆数据后才有效。
#
#         -----
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._item_heap_data:
#             return False
#         self._item_heap_data['animating'] = False
#         return True
#
#     def LockItemGrid(self, key, lock):
#         """
#         | 锁定或解锁指定网格，锁定后该网格内的所有方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。
#
#         -----
#
#         :param str key: 网格的key
#         :param bool lock: 是否锁定
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if self._is_grid_inited(key):
#             return False
#         if lock:
#             self._locked_grids.add(key)
#         else:
#             self._locked_grids.discard(key)
#         return True
#
#     def IsItemGridLocked(self, key):
#         """
#         | 获取指定网格是否被锁定。
#
#         -----
#
#         :param str key: 网格的key
#
#         :return: 是否被锁定，是则返回True，否则返回False
#         :rtype: bool
#         """
#         return key in self._locked_grids
#
#     def LockItemCell(self, cell, lock):
#         """
#         | 锁定或解锁指定方格，锁定后该方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param bool lock: 是否锁定
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         pos = self.GetItemCellPos(cell)
#         if lock:
#             self._locked_cells.add(pos)
#         else:
#             self._locked_cells.discard(pos)
#         return True
#
#     def IsItemCellLocked(self, cell):
#         """
#         | 获取指定方格是否被锁定。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 是否被锁定，是则返回True，否则返回False
#         :rtype: bool
#         """
#         pos = self.GetItemCellPos(cell)
#         return pos and (pos in self._locked_cells or pos[0] in self._locked_grids)
#
#     # Item Operations ==================================================================================================
#
#     def _sync_item_operation(self, op, *args):
#         self.__lib_sys.NotifyToServer("_SyncItemOperation", {'op': op, 'args': args})
#
#     def SetItemGridItems(self, key, item_dict_list):
#         """
#         | 将物品一键设置到网格的每个方格上。
#
#         -----
#
#         :param str key: 网格的key
#         :param list[dict] item_dict_list: 物品信息字典列表
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_grid_inited(key):
#             return False
#         self._set_grid_ui_item(key, item_dict_list)
#         self._sync_item_operation("set_grid", key, item_dict_list)
#         return True
#
#     def _get_grid_items(self, key, deepcopy=False):
#         if self._is_inv36_key(key):
#             return _LvComp.Item.GetPlayerAllItems(_INV_POS_TYPE, True)
#         elif self._is_inv27_key(key):
#             return _LvComp.Item.GetPlayerAllItems(_INV_POS_TYPE, True)[9:]
#         elif self._is_shortcut_key(key):
#             return _LvComp.Item.GetPlayerAllItems(_INV_POS_TYPE, True)[:9]
#         else:
#             items = self._grid_items.get(key, [])
#             return _deepcopy_item_dict(items) if deepcopy else items
#
#     def GetItemGridItems(self, key):
#         """
#         | 获取网格内的所有物品。
#
#         -----
#
#         :param str key: 网格的key
#
#         :return: 物品信息字典列表，获取不到时返回空列表
#         :rtype: list[dict|None]
#         """
#         return self._get_grid_items(key, True)
#
#     def SetItemCellItem(self, cell, item_dict):
#         """
#         | 将物品设置到指定方格上。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param dict item_dict: 物品信息字典
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         self._set_cell_ui_item(cell, item_dict)
#         self._sync_item_operation("set_cell", self.GetItemCellPos(cell), item_dict)
#         return True
#
#     def _get_cell_item(self, cell, deepcopy=False):
#         pos = self.GetItemCellPos(cell)
#         if not pos:
#             return
#         key, index = pos
#         if self._is_inv36_key(key) or self._is_shortcut_key(key):
#             return _LvComp.Item.GetPlayerItem(_INV_POS_TYPE, index, True)
#         elif self._is_inv27_key(key):
#             return _LvComp.Item.GetPlayerItem(_INV_POS_TYPE, index + 9, True)
#         else:
#             item = self._grid_items[key][index]
#             return _deepcopy_item_dict(item) if deepcopy else item
#
#     def GetItemCellItem(self, cell):
#         """
#         | 获取方格的物品信息字典。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 物品信息字典，获取不到返回None
#         :rtype: dict|None
#         """
#         return self._get_cell_item(cell, True)
#
#     def MoveItem(self, from_cell, to_cell, move_count=-1, fly_anim=True, force=False):
#         """
#         | 移动物品。
#         | 当起始位置为空气时，本次移动无效。
#         | 当终点位置有物品且 ``force`` 参数为 ``False`` 时，会发生物品交换，有两次物品移动操作，第一次为起始位置物品→终点位置，第二次为终点位置物品→起始位置。第二次移动本质上是第一次移动的“副作用”，不会再次触发 ``OnMoveItemsBefore`` 事件。
#
#         -----
#
#         :param str|tuple[str,int] from_cell: 起始位置的方格路径或方格位置元组
#         :param str|tuple[str,int] to_cell: 终点位置的方格路径或方格位置元组
#         :param int move_count: 移动数量，默认为-1，表示移动全部数量
#         :param bool fly_anim: 是否播放物品飞行动画，默认为True
#         :param bool force: 是否强制移动，默认为False；若强制移动，该接口会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(from_cell, to_cell):
#             return False
#         from_item = self._get_cell_item(from_cell)
#         to_item = self._get_cell_item(to_cell)
#         if _is_empty_item(from_item):
#             return False
#         args = {
#             'from_path': self.GetItemCellPath(from_cell),
#             'to_path': self.GetItemCellPath(to_cell),
#             'from_pos': self.GetItemCellPos(from_cell),
#             'to_pos': self.GetItemCellPos(to_cell),
#             'move_count': move_count,
#             'fly_anim': fly_anim,
#             'force': force,
#             'cancel': False,
#         }
#         self.OnMoveItemsBefore(args)
#         if args['cancel']:
#             return False
#         move_count = args['move_count']
#         fly_anim = args['fly_anim']
#         force = args['force']
#         if move_count <= -1:
#             move_count = from_item['count']
#         if force or _is_empty_item(to_item):
#             self._move_item_to_empty(from_cell, to_cell, move_count)
#         elif _is_same_item(from_item, to_item):
#             if from_cell != to_cell:
#                 self._move_item_to_same(from_cell, to_cell, move_count)
#         else:
#             self._exchange_items(from_cell, to_cell)
#             if fly_anim:
#                 self._set_item_fly_anim(to_item, to_cell, from_cell)
#         if fly_anim:
#             self._set_item_fly_anim(from_item, from_cell, to_cell)
#         return True
#
#     def _exchange_items(self, from_cell, to_cell):
#         from_item = self._get_cell_item(from_cell)
#         to_item = self._get_cell_item(to_cell)
#         self._set_cell_ui_item(from_cell, to_item)
#         self._set_cell_ui_item(to_cell, from_item)
#         self._sync_item_operation("exchange", self.GetItemCellPos(from_cell), self.GetItemCellPos(to_cell))
#
#     def _move_item_to_empty(self, from_cell, to_cell, count):
#         from_item = self._get_cell_item(from_cell, True)
#         from_new_count = from_item['count'] - count
#         from_item['count'] = count
#         self._set_cell_ui_item(to_cell, from_item)
#         from_item['count'] = from_new_count
#         self._set_cell_ui_item(from_cell, from_item)
#         self._sync_item_operation("move", self.GetItemCellPos(from_cell), self.GetItemCellPos(to_cell), count)
#
#     def _move_item_to_same(self, from_cell, to_cell, count):
#         overflow_count = self.SetItemCellCount(to_cell, +count)
#         self.SetItemCellCount(from_cell, -count + overflow_count)
#
#     def MergeItems(self, to_cell, fly_anim=True):
#         """
#         | 将所有其他同类物品与指定物品进行合堆。
#
#         -----
#
#         :param str|tuple[str,int] to_cell: 要合堆的方格路径或方格位置元组
#         :param bool fly_anim: 是否播放物品飞行动画，默认为True
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(to_cell):
#             return False
#         to_pos = self.GetItemCellPos(to_cell)
#         to_item = self._get_cell_item(to_pos)
#         if _is_empty_item(to_item):
#             return False
#         max_stack = _get_max_stack(to_item)
#         count = to_item['count']
#         for from_key in self._inited_keys:
#             from_all_items = self._get_grid_items(from_key)
#             if count >= max_stack:
#                 break
#             for from_index, from_item in enumerate(from_all_items):
#                 if count >= max_stack:
#                     break
#                 from_pos = (from_key, from_index)
#                 if self.IsItemCellLocked(from_pos):
#                     continue
#                 if from_pos == to_pos:
#                     continue
#                 if _is_empty_item(from_item) or not _is_same_item(from_item, to_item):
#                     continue
#                 from_count = from_item['count']
#                 if from_count == max_stack:
#                     continue
#                 self._move_item_to_same(from_pos, to_pos, from_count)
#                 count += from_count
#                 if fly_anim:
#                     self._set_item_fly_anim(from_item, from_pos, to_pos)
#         return True
#
#     def DivideItemEvenly(self, from_cell, to_cell_list, override=False, src_item=None):
#         """
#         | 将指定位置物品均匀地分到多个方格上。与原版背包的滑动均分效果相同。
#         | 均分必须满足以下规则，否则会失败：
#         - ``from_cell`` 物品不是空气；
#         - ``from_cell`` 物品数量必须大于 ``to_cell_list`` 的长度。
#         | 以上条件满足时，物品将会尽可能地被均分到 ``to_cell_list`` 的每个方格上，多余的无法被均分的物品会留在 ``from_cell`` 。
#
#         -----
#
#         :param str|tuple[str,int] from_cell: 要进行均分的物品所在的方格路径或方格位置元组
#         :param list[str|tuple[str,int]] to_cell_list: 均分位置的方格路径或方格位置元组的列表，表示将物品均分到哪些位置
#         :param bool override: 当均分位置存在物品时，是否覆盖该物品，默认为False
#         :param dict|None src_item: 要进行均分的物品信息字典，当该参数不为None时，会用src_item的物品进行均分，而不是用from_cell的物品；默认为None
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(from_cell):
#             return False
#         from_item = src_item or self._get_cell_item(from_cell)
#         if _is_empty_item(from_item):
#             return False
#         from_item = _deepcopy_item_dict(from_item)
#         from_pos = self.GetItemCellPos(from_cell)
#         # 筛选出有效的均分格子
#         to_pos_list = [self.GetItemCellPos(i) for i in to_cell_list]
#         to_pos_list = [
#             p for p in to_pos_list
#             if p and p != from_pos and (override or _is_empty_item(self._get_cell_item(p)))
#         ]
#         if not to_pos_list:
#             return False
#         # 计算均分数量
#         from_count = int(from_item['count'])
#         to_cell_len = len(to_pos_list)
#         to_count = from_count / to_cell_len
#         if to_count <= 0:
#             return False
#         # 遍历设置to_cell物品
#         from_item['count'] = to_count
#         for to_pos in to_pos_list:
#             self._set_cell_ui_item(to_pos, from_item)
#         # 设置from_cell剩余物品
#         remain_count = from_count % to_cell_len
#         from_item['count'] = remain_count
#         self._set_cell_ui_item(from_pos, from_item)
#         self._sync_item_operation(
#             "divide", from_item, from_pos, to_pos_list, override, to_count, remain_count
#         )
#         return True
#
#     def SetItemCellCount(self, cell, count, absolute=0):
#         """
#         | 设置指定方格内的物品的数量。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param int count: 数量
#         :param int absolute: 传0或1，0表示在原数量的基础上增加count（正数表示增加，负数表示减少），1表示将物品数量直接设置为count，默认为0
#
#         :return: 溢出数量，即设置数量后超过最大堆叠数的数量，设置失败时返回-1
#         :rtype: int
#         """
#         if not self._is_cell_exist(cell):
#             return -1
#         item = self._get_cell_item(cell)
#         if _is_empty_item(item):
#             return -1
#         if absolute:
#             item_count = count
#         else:
#             item_count = item['count'] + count
#         overflow_count = 0
#         max_stack = _get_max_stack(item)
#         if item_count > max_stack:
#             overflow_count = item_count - max_stack
#             item_count = max_stack
#         elif item_count < 0:
#             item_count = 0
#         self.SetItemCellCountLabel(cell, item_count)
#         self._sync_item_operation("set_count", self.GetItemCellPos(cell), item_count)
#         return overflow_count
#
#     def GetItemCellCount(self, cell):
#         """
#         | 获取指定方格内的物品的数量。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 物品数量，没有物品时返回0
#         :rtype: int
#         """
#         item = self._get_cell_item(cell)
#         return 0 if _is_empty_item(item) else item.get('count', 1)
#
#     def ReturnItemsToInv(self, keys=None):
#         """
#         | 将所有背包外的物品返还给背包。
#         | 调用该接口后，所有（或指定）的非背包物品网格内的物品会归还给本地玩家的背包。若背包已满，则会丢弃到世界。
#
#         -----
#
#         :param str|tuple[str]|None keys: 网格的key，指定要将哪些网格的物品返还给背包，多个网格可使用元组，传入None时表示所有已初始化网格；默认为None
#
#         :return: 无
#         :rtype: None
#         """
#         keys = self._parse_keys(keys)
#         self._sync_item_operation("ret_items", keys)
#
#     def SpawnItemToItemGrid(self, item_dict, key):
#         """
#         | 生成物品到物品网格。效果与服务端的 ``SpawnItemToPlayerInv`` 接口类似。
#
#         -----
#
#         :param dict item_dict: 生成的物品信息字典，数量可以超过最大堆叠
#         :param str key: 网格的key
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if self._is_grid_inited(key):
#             return False
#         item_dict = _deepcopy_item_dict(item_dict)
#         count = item_dict['count']
#         max_stack = _get_max_stack(item_dict)
#         items = self._get_grid_items(key)
#         # 优先生成到同种物品的位置
#         for i, item in enumerate(items):
#             if _is_same_item(item, item_dict) and item['count'] < max_stack:
#                 count = self.SetItemCellCount((key, i), +count)
#             if count <= 0:
#                 return True
#         # 生成到空格
#         for i, item in enumerate(items):
#             if _is_empty_item(item):
#                 if count > max_stack:
#                     item_dict['count'] = max_stack
#                     count -= max_stack
#                 else:
#                     item_dict['count'] = count
#                     count = 0
#                 self.SetItemCellItem((key, i), item_dict)
#             if count <= 0:
#                 return True
#         # 丢弃剩余物品
#         item_dict['count'] = count
#         self.__lib_sys.NotifyToServer("_ThrowItem", item_dict)
#         return True
#
#     def ThrowItemFromItemGrid(self, cell, count=-1):
#         """
#         | 将指定方格的物品丢弃到世界。
#
#         -----
#
#         :param str|tuple[str,int] cell: 丢弃物品所在的方格路径或方格位置元组
#         :param int count: 丢弃数量，传入-1表示丢弃全部；默认为-1
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         item = self._get_cell_item(cell, True)
#         if _is_empty_item(item):
#             return False
#         self.SetItemCellCount(
#             cell,
#             -count if count >= 0 else 0,
#             0 if count >= 0 else 1,
#         )
#         if count >= 0:
#             item['count'] = count
#         self.__lib_sys.NotifyToServer("_ThrowItem", item)
#         return True
#
#     def SetSelectedItemData(self, cell, selected=True):
#         """
#         | 设置指定物品的选中状态。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param bool selected: 是否选中，默认为True
#
#         :return: 是否成功
#         :rtype: bool
#         """
#         if not self._is_cell_exist(cell):
#             return False
#         default_img = self.GetItemCellUIControl(cell).GetChildByPath(_UI_PATH_DEFAULT).asImage()
#         item_dict = self._get_cell_item(cell, True)
#         path = self.GetItemCellPath(cell)
#         pos = self.GetItemCellPos(cell)
#         args = {
#             'item_dict': item_dict,
#             'cell_path': path,
#             'cell_pos': pos,
#             'cancel': False,
#             'selected': selected,
#         }
#         self.OnItemGridSelectOrUnselectItem(args)
#         if args['cancel']:
#             return False
#         if selected:
#             default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_SELECTED)
#             self._selected_item = {'item_dict': item_dict, 'cell_path': path, 'cell_pos': pos}
#         else:
#             default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
#             self.ClearItemGridState()
#         return True
#
#     def GetSelectedItemData(self):
#         """
#         | 获取当前选中物品的选中数据字典。
#
#         -----
#
#         :return: 选中数据字典，没有选中物品时返回None
#         :rtype: dict[str,dict|str|tuple[str,int]]|None
#         """
#         return self._selected_item.copy() if self._selected_item else None
#
#     def IsCellSelected(self, cell):
#         """
#         | 判断方格是否选中。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#
#         :return: 是否选中
#         :rtype: bool
#         """
#         return self._selected_item and self.GetItemCellPath(cell) == self._selected_item['cell_path']
#
#     def SetItemHeapData(self, cell, count):
#         """
#         | 设置物品分堆数据。
#
#         -----
#
#         :param str|tuple[str,int] cell: 方格路径或方格位置元组
#         :param int count: 分堆数量
#
#         :return: 设置成功时返回分堆数据字典，失败时返回None
#         :rtype: dict[str,dict|int|bool|ProgressBarUIControl|str|tuple[str,int]]|None
#         """
#         if not self._is_cell_exist(cell):
#             return
#         item_dict = self.GetItemCellItem(cell)
#         heap_bar = self.GetItemCellUIControl(cell).GetChildByPath(_UI_PATH_HEAP).asProgressBar()
#         heap_bar.SetVisible(True)
#         heap_bar.SetValue(float(count) / item_dict['count'])
#         self._item_heap_data = {
#             'item_dict': item_dict,
#             'cell_path': self.GetItemCellPath(cell),
#             'cell_pos': self.GetItemCellPos(cell),
#             'selected_count': count,
#             'animating': False,
#             'bar_ctrl': heap_bar,
#         }
#         return self._item_heap_data
#
#     def GetItemHeapData(self):
#         """
#         | 获取物品分堆数据。
#
#         -----
#
#         :return: 分堆数据字典，没有分堆数据时返回None
#         :rtype: dict[str,dict|int|bool|ProgressBarUIControl|str|tuple[str,int]]|None
#         """
#         return self._item_heap_data.copy() if self._item_heap_data else None
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
