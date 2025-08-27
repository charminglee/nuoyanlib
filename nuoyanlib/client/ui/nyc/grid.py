# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-27
|
| ==============================================
"""


from math import ceil
from types import GeneratorType
from ...._core._utils import get_func, kwargs_setter
from ...._core._types._checker import args_type_check
from ...._core._client.comp import ScreenNode, ViewBinder
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "ElemGroup",
    "NyGrid",
]


def _process_grid_index(index, l):
    if isinstance(index, int):
        if index < 0:
            index += l
        if index < 0 or index >= l:
            raise IndexError("NyGrid index out of range")
        return [index]
    else:
        return range(*index.indices(l))


def _index_to_coord(i, dx):
    return i % dx, i / dx


def _coord_to_index(x, y, dx):
    return x * dx + y


class ElemGroup(object):
    __slots__ = ('grid', 'elem_list', '_len')

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
        'real_visible',
        'name',
        'path',
        'parent_path',
        'parent_control',
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
        'new_child',
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

    def __init__(self, grid, elem_list):
        self.grid = grid
        self.elem_list = elem_list
        self._len = len(elem_list)

    def __iter__(self):
        return iter(self.elem_list)

    def __len__(self):
        return self._len

    @args_type_check((int, slice), is_method=True)
    def __getitem__(self, item):
        return self.elem_list[item]

    def __setattr__(self, key, value):
        if key in ElemGroup.__slots__:
            return object.__setattr__(self, key, value)
        if key not in ElemGroup._ALLOWED_SET_ATTRS:
            raise AttributeError("can't set attribute '%s' to ElemGroup object" % key)
        # 批量设置属性
        for elem in self.elem_list:
            setattr(elem, key, value)

    def __getattr__(self, key):
        if key in ElemGroup._ALLOWED_GET_ATTRS:
            # 批量获取属性
            return [getattr(elem, key) for elem in self.elem_list]
        elif key in ElemGroup._ALLOWED_METHODS:
            # 批量调用方法
            def func(*args, **kwargs):
                res = []
                for elem in self.elem_list:
                    res.append(getattr(elem, key)(*args, **kwargs))
                return res
            return func
        raise AttributeError("can't get attribute '%s' from ElemGroup object" % key)

    def apply(self, func, level=1):
        pass


class NyGrid(NyControl):
    """
    | 创建 ``NyGrid`` 网格实例。

    -----

    | 关于 ``elem_visible_binding`` 与 ``collection_name`` 参数的说明：
    - 该参数用于 ``.elem_count`` 、 ``.dimension`` 等接口，实现动态设置网格元素的数量（多余元素将通过设置 ``visible`` 为 ``False`` 的方式隐藏），不使用该接口可忽略这两个参数。
    - 由于网格控件的特性，设置元素的 ``visible`` 需要使用绑定，请在你的 **网格模板控件** 的json中添加以下绑定，然后将 ``"binding_name"`` 的值设置给 ``elem_visible_binding`` 参数 。
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
    :param str elem_visible_binding: [仅关键字参数] 用于控制网格元素visible的绑定名称，详见上方说明
    :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明
    """

    __get_dim = staticmethod(get_func(
        ScreenNode,
        (103, 117, 105),
        (103, 101, 116, 95, 103, 114, 105, 100, 95, 100, 105, 109, 101, 110, 115, 105, 111, 110)
    ))
    _CONTROL_TYPE = ControlType.GRID

    @kwargs_setter(
        is_stack_grid=False,
        template_name="",
        elem_visible_binding="",
        collection_name="",
    )
    def __init__(self, screen_node_ex, grid_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, grid_control)
        self.is_stack_grid = kwargs['is_stack_grid']
        template_name = kwargs['template_name']
        if template_name and "." in template_name:
            template_name = template_name.split(".")[-1]
        self.__template_name = template_name
        self.elem_visible_binding = kwargs['elem_visible_binding']
        self.collection_name_ = kwargs['collection_name']
        if self.elem_visible_binding and self.collection_name_:
            self.ui_node._build_binding(
                self._return_elem_visible, ViewBinder.BF_BindBool, self.elem_visible_binding, self.collection_name_
            )
        self._update_cbs = []
        self.__elem_count = -1

    def __destroy__(self):
        self._update_cbs = []
        self.ui_node._unbuild_binding(self._return_elem_visible)
        NyControl.__destroy__(self)

    def __grid_update__(self):
        pass

    # region API =======================================================================================================

    @property
    def template_name(self):
        """
        [只读属性]

        | 网格模板控件名称，即 ``"grid_item_template"`` 字段或UI编辑器中的网格“内容”所使用的控件。

        :rtype: str
        """
        if not self.__template_name:
            children_names = self._screen_node.GetChildrenName(self.path)
            if children_names:
                name = children_names[0]
                for i in range(len(name) - 1, -1, -1):
                    if not name[i].isdigit():
                        self.__template_name = name[:i + 1]
                        break
        return self.__template_name

    @property
    def row(self):
        return

    @property
    def column(self):
        return

    def iter_elems(self):
        """
        [迭代器]

        | 获取网格所有元素的 ``NyControl`` 实例。

        -----

        :return: 迭代器
        :rtype: GeneratorType
        """
        for i in range(self.elem_count):
            yield self[i]

    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(self, item):
        """
        | 根据特定规则获取网格单个或多个元素。
        | 获取指定位置的元素：
        - ``grid[i]`` -- 按从左到右从上到下的顺序获取索引为i的元素，支持负数索引。
        - ``grid[x,⠀y]`` -- 获取坐标为 (x, y) 的元素，坐标从0开始，向右为X轴正方向，向下为Y轴正方向（下同）。
        | 利用切片获取多个元素：
        - ``grid[start:stop]`` -- 与列表切片类似，按从左到右从上到下的顺序获取第start到第stop个元素（不包括stop，下同）。
        - ``grid[x,⠀start:stop]`` -- 获取指定x坐标上，y坐标为start到stop的多个元素。
        - ``grid[start:stop,⠀y]`` -- 获取指定y坐标上，x坐标为start到stop的多个元素。
        - ``grid[start1:stop1,⠀start2:stop2]`` -- 获取x坐标为start1到stop1，y坐标为start2到stop2的多个元素。

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
            index_list = [_coord_to_index(x, y, dx) for x in xr for y in yr]

        else:
            size = dx * dy
            index_list = _process_grid_index(item, size)

        if not index_list:
            return
        if len(index_list) == 1:
            return self._get_elem(index_list[0])
        else:
            elem_list = [self._get_elem(i) for i in index_list]
            return ElemGroup(self, elem_list)

    def set_gird_update_callback(self, func):
        """
        设置网格更新时触发的回调函数。

        -----

        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        if func not in self._update_cbs:
            self._update_cbs.append(func)
            return True
        return False

    def remove_gird_update_callback(self, func):
        """
        移除网格更新时触发的回调函数。

        -----

        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        if func in self._update_cbs:
            self._update_cbs.remove(func)
            return True
        return False

    # endregion

    # region Properties ================================================================================================

    @property
    def grid_size(self):
        """
        [只读属性]

        | 网格容量，等价于 ``grid.dimension[0]⠀*⠀grid.dimension[1]`` 。

        :rtype: int
        """
        dim = self.dimension
        return dim[0] * dim[1]

    @property
    def elem_count(self):
        """
        [可读写属性]

        | 网格的元素数量。
        | 对于非StackGrid网格，设置 ``elem_count`` 不会改变网格的列数。例如一个3x3（3行3列）网格，设置 ``elem_count=5`` 后将变成2x3，且第2行最后1个元素会被隐藏。同理，若设置 ``elem_count=13``，则网格变成5x3，第5行最后2个元素会被隐藏。

        :rtype: int
        """
        if self.__elem_count < 0:
            bag = self.property_bag
            return bag.get('#grid_number_size', 0) if bag else 0
        else:
            return self.__elem_count

    @elem_count.setter
    def elem_count(self, val):
        """
        [可读写属性]

        | 网格的元素数量。
        | 对于非StackGrid网格，设置 ``elem_count`` 不会改变网格的列数。例如一个3x3（3行3列）网格，设置 ``elem_count=5`` 后将变成2x3，且第2行最后1个元素会被隐藏。同理，若设置 ``elem_count=13``，则网格变成5x3，第5行最后2个元素会被隐藏。

        :type val: int
        """
        if val == self.elem_count:
            return
        if val < 0:
            raise ValueError("'elem_count' must be greater than 0")
        self.__elem_count = val
        if self.is_stack_grid:
            self._screen_node.SetStackGridCount(self.path, val)
        else:
            dx, dy = self.dimension
            new_dy = int(ceil(float(val) / dx))
            if new_dy != dy:
                self.base_control.SetGridDimension((dx, new_dy))

    @property
    def dimension(self):
        """
        [可读写属性]

        | 获取网格的xy大小。当网格为StackGrid时，y值固定为0。

        :rtype: tuple[int,int]
        """
        return NyGrid.__get_dim(self.base_control.mScreenName, self.base_control.FullPath()) # NOQA

    @dimension.setter
    def dimension(self, val):
        """
        [可读写属性]

        | 设置网格的xy大小。当网格为StackGrid时，忽略传入的y值。

        :type val: tuple[int,int]
        """
        if val == self.dimension:
            return
        if self.is_stack_grid:
            if val[0] < 0:
                raise ValueError("'dimension' value must be greater than 0")
            self._screen_node.SetStackGridCount(self.path, val[0])
            self.__elem_count = val[0]
        else:
            if val[0] < 0 or val[1] < 0:
                raise ValueError("'dimension' value must be greater than 0")
            self.base_control.SetGridDimension(val)
            size = val[0] * val[1]
            if self.__elem_count < 0 or size < self.__elem_count:
                self.__elem_count = size

    # endregion

    # region Internal ==================================================================================================

    def _return_elem_visible(self, index):
        return self.visible and (self.__elem_count < 0 or index < self.__elem_count)

    def _get_elem(self, index):
        elem = self / (self.template_name + str(index + 1))
        return NyControl.from_control(self.ui_node, elem)

    # endregion









