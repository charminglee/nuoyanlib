# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Union, Tuple, Callable, TypeVar, Optional, Iterator, Generator, Any, List
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from .control import NyControl
from ...._core._types._typing import ITuple2, ArgsDict
from ...._core._types._checker import args_type_check
from ..screen_node import ScreenNodeExtension
from ...._core._types._events import ClientEventEnum as Events


_T = TypeVar("_T")
__Item = Union[int, slice, Tuple[Union[int, slice], Union[int, slice]]]
__GridUpdateCallback = Callable[[ArgsDict], Any]


class _ElemGroup(Iterator[Optional[NyGrid]]):
    _grid: NyGrid
    _coord_gen: Generator[ITuple2, None, None]
    _len: int
    def __init__(self, grid: NyGrid, item: __Item) -> None: ...
    def __iter__(self: _T) -> _T: ...
    def next(self) -> Optional[NyGrid]: ...
    def __len__(self) -> int: ...
    def _index_to_coord(self, index: int, xl: int) -> ITuple2: ...


class NyGrid(NyControl):
    _update_cbs: List[__GridUpdateCallback]
    base_control: GridUIControl
    """
    | 网格 ``GridUIControl`` 实例。
    """
    is_stack_grid: bool
    """
    | 是否是StackGrid。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        grid_control: GridUIControl,
        *,
        is_stack_grid: bool = False,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3
    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(self, item: __Item) -> _ElemGroup: ...
    def GridComponentSizeChangedClientEvent(self, args: ArgsDict) -> None: ...
    def set_gird_update_callback(self, func: __GridUpdateCallback) -> bool: ...
    def remove_gird_update_callback(self, func: __GridUpdateCallback) -> bool: ...
    @property
    def grid_size(self) -> int: ...
    @property
    def dimension(self) -> ITuple2: ...
    @dimension.setter
    def dimension(self, val: ITuple2) -> None: ...

    def SetGridDimension(self, dimension: ITuple2) -> None:
        """
        | 设置Grid控件的大小。

        -----

        :param tuple[int,int] dimension: 设置网格的横向与纵向大小

        :return: 无
        :rtype: None
        """
    def GetGridItem(self, x: int, y: int) -> BaseUIControl:
        """
        | 根据位置获取网格元素控件。
        | 获取网格子节点需要注意一些细节，详见《开发指南-界面与交互-UI说明文档》中对Grid控件的描述。

        -----

        :param int x: 元素在网格的横坐标
        :param int y: 元素在网格的纵坐标

        :return: 网格的子节点控件
        :rtype: BaseUIControl
        """
