# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


if 0:
    from typing import Any
    from ..screen_node import ScreenNodeExtension


import math
from ....core._utils import get_func, kwargs_setter, try_exec, cached_property
from ....core._types._checker import args_type_check
from ....core.client.comp import ScreenNode, ViewBinder
from ....utils.enum import ControlType, GridCallbackType
from .control import NyControl
from ..ui_utils import to_path


__all__ = [
    "GridData",
    "ElemGroup",
    "NyGrid",
]


class GridData(list):
    """
    网格数据对象，用于实现网格元素与数据的自动管理。

    借助网格数据对象，开发者只需关注数据本身，而无需关心网格的刷新等繁琐细节。
    网格数据对象继承于列表，因此，你可以像操作列表一样操作网格数据对象。

    -----

    :param list src: 网格数据源
    :param function op_func: 网格数据操作函数，用于实现数据的操作逻辑；接受三个参数，分别为网格元素索引、元素的NyControl实例、元素对应的数据；网格刷新时会自动对每个元素调用一次该函数，并传入上述三个参数，实现网格元素与数据的自动管理
    :param Any default: 默认数据；当网格元素索引超出数据源范围（越界）时，将使用默认数据；默认为None
    """

    def __init__(self, src, op_func, default=None):
        list.__init__(self, src)
        self.src = src
        self.op_func = op_func
        self.default = default
        self.grid = None

    def bind_grid(self, grid):
        """
        绑定当前网格数据对象到网格。

        -----

        :param NyGrid grid: 网格NyGrid实例

        :return: 无
        :rtype: None
        """
        self.grid = grid
        grid.gd_obj = self

    def _get_data(self, index):
        return self.src[index] if index < len(self.src) else self.default

    def bind(self):
        """
        立即将数据绑定给各个元素，并刷新显示。

        -----

        :return: 无
        :rtype: None
        """
        for cell in self.grid.get_all_cells():
            index = self.grid.get_cell_index(cell)
            self.op_func(index, cell, self._get_data(index))
        self.grid._screen_node.UpdateScreen()


def _process_grid_index(index, l):
    if isinstance(index, int):
        if index < 0:
            index += l
        if index < 0 or index >= l:
            raise IndexError("NyGrid index out of range")
        return [index]
    else:
        return range(*index.indices(l))


def _index_2_coord(i, dx):
    return i % dx, i / dx


def _coord_2_index(x, y, dx):
    return x * dx + y


class ElemGroup(object):
    __slots__ = ('grid', 'cell_list', '_len')

    _ALLOWED_SET_ATTRS = (
        'position',
        'anchor_from',
        'anchor_to',
        'clip_offset',
        'clip_children',
        'full_position_x',
        'full_position_y',
        'full_size_x',
        'full_size_y',
        'global_position',
        'max_size',
        'min_size',
        'size',
        'visible',
        'alpha',
        'layer',
        'touch_enable',
        'property_bag',
    )
    _ALLOWED_GET_ATTRS = (
        'name',
        'path',
        'parent_path',
        'parent',
        'position',
        'anchor_from',
        'anchor_to',
        'clip_offset',
        'clip_children',
        'full_position_x',
        'full_position_y',
        'full_size_x',
        'full_size_y',
        'global_position',
        'max_size',
        'min_size',
        'size',
        'visible',
        'layer',
        'property_bag',
    )
    _ALLOWED_METHODS = (
        # 'to_button',
        # 'to_image',
        # 'to_label',
        # 'to_input_panel',
        # 'to_stack_panel',
        # 'to_edit_box',
        # 'to_netease_paper_doll',
        # 'to_item_renderer',
        # 'to_scroll_view',
        # 'to_grid',
        # 'to_progress_bar',
        # 'to_toggle',
        # 'to_slider',
        # 'to_selection_wheel',
        # 'to_combo_box',
        # 'to_mini_map',
        'add_child',
        'clone_from',
        'SetPosition',
        'SetFullSize',
        'GetFullSize',
        'SetFullPosition',
        'GetFullPosition',
        'SetAnchorFrom',
        'GetAnchorFrom',
        'SetAnchorTo',
        'GetAnchorTo',
        'SetClipOffset',
        'GetClipOffset',
        'SetClipsChildren',
        'GetClipsChildren',
        'SetMaxSize',
        'GetMaxSize',
        'SetMinSize',
        'GetMinSize',
        'GetPosition',
        'GetGlobalPosition',
        'SetSize',
        'GetSize',
        'SetVisible',
        'GetVisible',
        'SetTouchEnable',
        'SetAlpha',
        'SetLayer',
        'GetPath',
        'GetChildByName',
        'GetChildByPath',
        'resetAnimation',
        'PauseAnimation',
        'PlayAnimation',
        'StopAnimation',
        'SetAnimation',
        'RemoveAnimation',
        'SetAnimEndCallback',
        'RemoveAnimEndCallback',
        'IsAnimEndCallbackRegistered',
        'GetPropertyBag',
        'SetPropertyBag',
    )

    def __init__(self, grid, cell_list):
        self.grid = grid
        self.cell_list = cell_list
        self._len = len(cell_list)

    def __iter__(self):
        return iter(self.cell_list)

    def __len__(self):
        return self._len

    @args_type_check((int, slice), is_method=True)
    def __getitem__(self, item):
        return self.cell_list[item]

    def __setattr__(self, key, value):
        if key in ElemGroup.__slots__:
            return object.__setattr__(self, key, value)
        if key not in ElemGroup._ALLOWED_SET_ATTRS:
            raise AttributeError("can't set attribute '%s' to ElemGroup object" % key)
        # 批量设置属性
        for cell in self.cell_list:
            setattr(cell, key, value)

    def __getattr__(self, key):
        if key in ElemGroup._ALLOWED_GET_ATTRS:
            # 批量获取属性
            return [getattr(cell, key) for cell in self.cell_list]
        elif key in ElemGroup._ALLOWED_METHODS:
            # 批量调用方法
            def func(*args, **kwargs):
                res = []
                for cell in self.cell_list:
                    res.append(getattr(cell, key)(*args, **kwargs))
                return res
            return func
        raise AttributeError("can't get attribute '%s' from ElemGroup object" % key)

    def apply(self, func, level=1):
        pass


class NyGrid(NyControl):
    """
    网格控件类。

    -----

    关于 ``cell_visible_binding`` 与 ``collection_name`` 参数的说明：

    - 该参数用于 ``.grid_size`` 、 ``.dimension`` 等接口，实现动态设置网格元素的数量（多余元素将通过设置 ``visible`` 为 ``False`` 的方式隐藏），不使用该接口可忽略这两个参数。
    - 由于网格控件的特性，设置元素的 ``visible`` 需要使用绑定，请在你的 **网格模板控件** 的json中添加以下绑定，然后将 ``"binding_name"`` 的值设置给 ``cell_visible_binding`` 参数 。
    ::

        "bindings": [
            {
                "binding_type": "collection",
                "binding_collection_name": "grid_collection_name", //此处需要与网格的"collection_name"字段相同
                "binding_name": "#namespace.binding_name", //可自定义
                "binding_name_override": "#visible",
                "binding_condition": "always"
            }
        ]
    - 最后，将 **网格** json中的 ``"collection_name"`` 字段的值设置给 ``collection_name`` 参数即可。

    -----

    :param ScreenNodeExtension screen_node_ex: 网格所在UI类的实例（需继承ScreenNodeExtension）
    :param GridUIControl grid_control: 通过asGrid()等方式获取的GridUIControl实例
    :param bool is_stack_grid: [仅关键字参数] 是否是StackGrid，默认为False
    :param str template_name: [仅关键字参数] 网格模板控件名称，即"grid_item_template"字段或UI编辑器中的网格“内容”所使用的控件；仅模板控件名称以数字结尾时需要传入该参数
    :param str cell_visible_binding: [仅关键字参数] 用于控制网格元素visible的绑定名称，详见上方说明
    :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明
    """

    CONTROL_TYPE = ControlType.GRID

    @kwargs_setter(
        is_stack_grid=False,
        template_name="",
        cell_visible_binding="",
        collection_name="",
    )
    def __init__(self, screen_node_ex, grid_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, grid_control)
        self.__grid_size = -1
        self._callback_map = {
            GridCallbackType.UPDATE: [],
            GridCallbackType.LOADED: [],
        }
        self._loaded = False
        self.is_stack_grid = kwargs['is_stack_grid']
        template_name = kwargs['template_name']
        if template_name and "." in template_name:
            template_name = template_name.split(".")[-1]
        self.__template_name = template_name
        self.cell_visible_binding = kwargs['cell_visible_binding']
        self.collection_name_ = kwargs['collection_name']
        self.gd_obj = None
        if self.cell_visible_binding and self.collection_name_:
            self.ui_node.build_binding(
                self._return_cell_visible, ViewBinder.BF_BindBool, self.cell_visible_binding, self.collection_name_
            )

    def __destroy__(self):
        self._callback_map.clear()
        self.ui_node.unbuild_binding(self._return_cell_visible)
        NyControl.__destroy__(self)

    def __grid_update__(self):
        if self.gd_obj:
            try_exec(self.gd_obj.bind)
        if not self._loaded:
            self._loaded = True
            for func in self._callback_map[GridCallbackType.LOADED]:
                try_exec(func)
        for func in self._callback_map[GridCallbackType.UPDATE]:
            try_exec(func)

    # region Properties ================================================================================================

    @cached_property
    def template_name(self):
        """
        [只读属性]

        网格模板控件名称。

        即 ``"grid_item_template"`` 字段或UI编辑器中的网格“内容”所使用的控件。

        :rtype: str
        """
        if not self.__template_name:
            children_names = self._screen_node.GetChildrenName(self.path)
            if children_names:
                name = children_names[0]
                for i in name[::-1]:
                    if not i.isdigit():
                        return name[:i + 1]
        else:
            return self.__template_name

    @property
    def rows(self):
        return

    @property
    def columns(self):
        return

    @property
    def grid_size(self):
        """
        [可读写属性]

        网格的容量，即元素数量。

        对于非StackGrid网格，设置 ``grid_size`` 不会改变网格的列数。
        例如一个3x3（3行3列）网格，设置 ``grid_size=5`` 后将变成2x3，且最末尾元素会被隐藏。
        同理，若设置 ``grid_size=13``，则网格变成5x3，末尾2个元素会被隐藏。

        :rtype: int
        """
        if self.__grid_size < 0:
            bag = self.property_bag
            return bag.get('#grid_number_size', 0) if bag else 0
        else:
            return self.__grid_size

    @grid_size.setter
    def grid_size(self, val):
        """
        [可读写属性]

        网格的容量，即元素数量。

        对于非StackGrid网格，设置 ``grid_size`` 不会改变网格的列数。
        例如一个3x3（3行3列）网格，设置 ``grid_size=5`` 后将变成2x3，且最末尾元素会被隐藏。
        同理，若设置 ``grid_size=13``，则网格变成5x3，末尾2个元素会被隐藏。

        :type val: int
        """
        if val == self.grid_size:
            return
        if val < 0:
            raise ValueError("'grid_size' must be >= 0")
        if self.is_stack_grid:
            self._screen_node.SetStackGridCount(self.path, val)
        else:
            dx, dy = self.dimension
            new_dy = int(math.ceil(float(val) / dx))
            if new_dy != dy:
                self._base_control.SetGridDimension((dx, new_dy))
        self.__grid_size = val

    @property
    def dimension(self):
        """
        [可读写属性]

        获取网格的xy大小。

        当网格为StackGrid时，y值固定为0。

        :rtype: tuple[int,int]
        """
        return NyGrid.__get_dim(self._base_control.mScreenName, self._base_control.FullPath())

    @dimension.setter
    def dimension(self, val):
        """
        [可读写属性]

        设置网格的xy大小。

        当网格为StackGrid时，忽略传入的y值。

        :type val: tuple[int,int]
        """
        if val == self.dimension:
            return
        if self.is_stack_grid:
            if val[0] < 0:
                raise ValueError("'dimension' value must be >= 0")
            self._screen_node.SetStackGridCount(self.path, val[0])
            self.__grid_size = val[0]
        else:
            if val[0] < 0 or val[1] < 0:
                raise ValueError("'dimension' value must be >= 0")
            self._base_control.SetGridDimension(val)
            size = val[0] * val[1]
            if self.__grid_size <= 0 or size < self.__grid_size:
                self.__grid_size = size

    # endregion

    # region Common ====================================================================================================

    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(self, item):
        """
        根据特定规则获取网格单个或多个元素。

        获取指定位置的元素：

        - ``grid[i]`` -- 按从左到右从上到下的顺序（下同）获取索引为i的元素，支持负数索引。
        - ``grid[x,⠀y]`` -- 获取坐标为 (x, y) 的元素，坐标从0开始，向右为X轴正方向，向下为Y轴正方向（下同）。

        利用切片获取多个元素：

        - ``grid[start:stop]`` -- 与列表切片类似，获取索引为start到stop的元素（不包括stop，下同）。
        - ``grid[x,⠀start:stop]`` -- 获取指定x坐标上，y坐标为start到stop的元素。
        - ``grid[start:stop,⠀y]`` -- 获取指定y坐标上，x坐标为start到stop的元素。
        - ``grid[start1:stop1,⠀start2:stop2]`` -- 获取x坐标为start1到stop1，y坐标为start2到stop2的元素。

        -----

        :param int|slice|tuple[int|slice,int|slice] item: 详见上方说明

        :return: 获取单个元素时，返回该元素的NyControl实例；获取多个元素时，返回ElemGroup对象；获取不到元素时返回None
        :rtype: NyControl|ElemGroup|None
        """
        dx, dy = self.dimension
        if isinstance(item, tuple):
            x, y = item
            xr = _process_grid_index(x, dx)
            yr = _process_grid_index(y, dy)
            index_list = [_coord_2_index(x, y, dx) for x in xr for y in yr]

        else:
            size = dx * dy
            index_list = _process_grid_index(item, size)

        if not index_list:
            return
        if len(index_list) == 1:
            return self.get_cell(index_list[0])
        else:
            cell_list = [self.get_cell(i) for i in index_list]
            return ElemGroup(self, cell_list)

    def get_cell_index(self, cell):
        """
        获取指定元素在网格中的索引。

        -----

        :param str|BaseUIControl|NyControl cell: 网格元素的路径或实例

        :return: 元素索引
        :rtype: int
        """
        path = to_path(cell)
        return int(path.split(self.template_name)[-1]) - 1

    def update_grid_data(self):
        if not self.gd_obj:
            return

    @args_type_check(GridData, is_method=True)
    def bind_data(self, gd):
        """
        绑定网格数据。

        -----

        :param GridData gd: 网格数据对象

        :return: 无
        :rtype: None
        """
        self.gd_obj = gd
        gd.grid = self

    def get_cell(self, index):
        """
        获取索引为 ``index`` 的元素。

        -----

        :param int index: 索引

        :return: 元素的NyControl实例，获取不到时返回None
        :rtype: NyControl|None
        """
        return self / (self.template_name + str(index + 1))

    def get_all_cells(self):
        """
        获取网格所有元素的 ``NyControl`` 实例。

        -----

        :return: 网格所有元素的NyControl实例列表
        :rtype: list[NyControl]
        """
        return [self.get_cell(i) for i in range(self.grid_size)]

    def set_callback(self, func, cb_type=GridCallbackType.UPDATE):
        """
        设置网格回调函数。

        -----

        :param function func: 回调函数
        :param GridCallbackType cb_type: 回调类型，请使用GridCallbackType枚举值，默认为GridCallbackType.UPDATE

        :return: 是否成功
        :rtype: bool
        """
        if cb_type not in GridCallbackType:
            raise ValueError("invalid callback type: %s, use 'GridCallbackType' instead" % repr(cb_type))
        lst = self._callback_map[cb_type]
        if func in lst:
            return False
        lst.append(func)
        return True

    def remove_callback(self, func, cb_type=GridCallbackType.UPDATE):
        """
        移除网格回调函数。

        -----

        :param function func: 回调函数
        :param GridCallbackType cb_type: 回调类型，请使用GridCallbackType枚举值，默认为GridCallbackType.UPDATE

        :return: 是否成功
        :rtype: bool
        """
        if cb_type not in GridCallbackType:
            raise ValueError("invalid callback type: %s, use 'GridCallbackType' instead" % repr(cb_type))
        lst = self._callback_map[cb_type]
        if func not in lst:
            return False
        lst.remove(func)
        return True

    GetCellIndex = get_cell_index
    UpdateGridData = update_grid_data
    BindData = bind_data
    GetCell = get_cell
    GetAllCells = get_all_cells
    SetCallback = set_callback
    RemoveCallback = remove_callback

    # endregion

    # region Internal ==================================================================================================

    __get_dim = staticmethod(get_func(ScreenNode, (103, 117, 105), (103, 101, 116, 95, 103, 114, 105, 100, 95, 100, 105, 109, 101, 110, 115, 105, 111, 110)))

    def _return_cell_visible(self, index):
        return self.visible and (self.__grid_size < 0 or index < self.__grid_size)

    # endregion









