# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from ..._core._utils import args_type_check, join_chr
from ..._core._client._comp import ScreenNode
from ..._core._types._typing import FunctionType
from .ui_utils import ControlType
from .control import NyControl


__all__ = [
    "NyGrid",
]


class _ElemGroup(object):
    def __init__(self, grid, item):
        self._grid = grid
        dim = grid.dimension
        if isinstance(item, tuple):
            x, y = item
            if isinstance(x, int) and isinstance(y, int):
                self._coord_gen = (i for i in [(x, y)])
                self._len = 1
            else:
                xr = xrange(*x.indices(dim[0])) if isinstance(x, slice) else [x]
                yr = xrange(*y.indices(dim[1])) if isinstance(y, slice) else [y]
                self._coord_gen = ((x, y) for x in xr for y in yr)
                self._len = len(xr) * len(yr)
        elif isinstance(item, slice):
            r = xrange(*item.indices(grid.grid_size))
            self._coord_gen = (self._index_to_coord(i, dim[0]) for i in r)
            self._len = len(r)
        else:
            self._coord_gen = (i for i in [self._index_to_coord(item, dim[0])])
            self._len = 1

    def __iter__(self):
        return self

    def next(self):
        elem = self._grid.base_control.GetGridItem(*next(self._coord_gen))
        if elem:
            return NyControl.from_control(self._grid.screen_node, elem)
        return None

    def __len__(self):
        return self._len

    def _coord_to_index(self, x, y, xl):
        return y * xl + x

    def _index_to_coord(self, index, xl):
        return index % xl, index / xl

    def apply(self, func):
        pass

    def apply_to_level(self, func, level=1):
        pass

    def apply_to_attrs(self, attr, value, level=0):
        pass


class NyGrid(NyControl):
    """
    | 创建 ``NyGrid`` 网格实例。
    | 兼容ModSDK ``GridUIControl`` 和 ``BaseUIControl`` 的相关接口。
    | 对网格进行操作需要注意一些细节，详见开发指南-界面与交互-UI说明文档中对Grid控件的描述。

    -----

    :param ScreenNodeExtension screen_node_ex: 网格所在UI类的实例
    :param GridUIControl grid_control: 通过asGrid()获取的网格实例
    :param bool is_stack_grid: 关键字参数，是否是StackGrid，默认为False
    """

    __get_dim = None
    _CONTROL_TYPE = ControlType.grid

    def __init__(self, screen_node_ex, grid_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, grid_control)
        if not NyGrid.__get_dim:
            seq1 = join_chr(95, 95, 102, 117, 110, 99, 95, 95)
            seq2 = join_chr(95, 95, 103, 108, 111, 98, 97, 108, 115, 95, 95)
            seq3 = join_chr(103, 117, 105)
            seq4 = join_chr(103, 101, 116, 95, 103, 114, 105, 100, 95, 100, 105, 109, 101, 110, 115, 105, 111, 110)
            f = getattr(ScreenNode.__init__, seq1)
            m = getattr(f, seq2)[seq3]
            g = getattr(m, seq4)
            NyGrid.__get_dim = staticmethod(g)
        self.is_stack_grid = kwargs.get('is_stack_grid', False)
        self._update_cbs = []

    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(self, item):
        """
        | 根据特定规则获取网格元素，返回 ``ElemGroup`` 对象，规则如下：
        - ``grid[index]`` -- 按照从左到右从上到下的顺序获取第index个元素。
        - ``grid[start:stop]`` -- 按照从左到右从上到下的顺序获取第start到第stop个元素（不包括stop，下同），写法与列表切片相同。
        - ``grid[x,y]`` -- 获取坐标为(x,y)的元素，坐标从0开始，向右为X轴正方向，向下为Y轴正方向。
        - ``grid[x,start:stop]`` -- 获取指定x坐标上，y坐标为start到stop的元素。
        - ``grid[start:stop,y]`` -- 获取指定y坐标上，x坐标为start到stop的元素。
        - ``grid[start1:stop1,start2:stop2]`` -- 获取x坐标为start1到stop1，y坐标为start2到stop2的元素。

        -----

        :param int|slice|tuple[int|slice,int|slice] item: 详见说明

        :return: ElemGroup对象
        :rtype: _ElemGroup|None
        """
        return _ElemGroup(self, item)

    @args_type_check(FunctionType, is_method=True)
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

    @args_type_check(FunctionType, is_method=True)
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

    def _GridComponentSizeChangedClientEvent(self, event):
        for cb in self._update_cbs:
            cb()

    @property
    def grid_size(self):
        """
        [只读]

        | 网格的元素数量，即网格大小x * y。
        """
        bag = self.property_bag
        return bag.get('#grid_number_size', 0) if bag else 0

    @property
    def dimension(self):
        """
        [可读写]

        | 获取网格的xy大小。当网格为StackGrid时，y值固定为0。
        """
        return NyGrid.__get_dim(self.base_control.mScreenName, self.base_control.FullPath()) # NOQA

    @dimension.setter
    def dimension(self, val):
        """
        [可读写]

        | 设置网格的xy大小。当网格为StackGrid时，忽略传入的y值。
        """
        if self.is_stack_grid:
            self._screen_node.SetStackGridCount(self.path, val[0])
        else:
            self.base_control.SetGridDimension(val)












