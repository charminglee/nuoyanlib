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


from typing import Union, Tuple, Callable, TypeVar, Optional, Any, List, Iterator, overload, Iterable, Sized, Generator, DefaultDict
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from .control import NyControl
from ...._core._types._typing import ITuple2, STuple
from ...._core._types._checker import args_type_check
from ...._core.event._events import ClientEventEnum as Events
from ..screen_node import ScreenNodeExtension


_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True, bound=NyControl)
__GridUpdateCallback = Callable[[], Any]


def _process_grid_index(index: Union[int, slice], l: int) -> List[int]: ...
def _index_to_coord(i: int, dx: int) -> ITuple2: ...
def _coord_to_index(x: int, y: int, dx: int) -> int: ...


class ElemGroup(Iterable[_T_co], Sized):
    __slots__: STuple
    _ALLOWED_SET_ATTRS: STuple
    _ALLOWED_GET_ATTRS: STuple
    _ALLOWED_METHODS: STuple
    grid: NyGrid
    elem_list: List[_T_co]
    _len: int
    def __init__(self, grid: NyGrid, elem_list: List[_T_co]) -> None: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, item: int) -> _T_co: ...
    @overload
    def __getitem__(self, item: slice) -> List[_T_co]: ...
    def __setattr__(self, key: str, value: Any) -> None: ...
    def __getattr__(self, key: str) -> Union[List[Any], Callable[[...], List[Any]]]: ...


class NyGrid(NyControl):
    __elem_count: int
    __template_name: str
    _update_cbs: List[__GridUpdateCallback]
    base_control: GridUIControl
    """
    | 网格 ``GridUIControl`` 实例。
    """
    is_stack_grid: bool
    """
    | 是否是StackGrid。
    """
    elem_visible_binding: str
    """
    | 用于控制网格元素visible的绑定名称。
    """
    collection_name_: str
    """
    | 网格集合名称。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        grid_control: GridUIControl,
        /,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        elem_visible_binding: str = "",
        collection_name: str = "",
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def __grid_update__(self) -> None: ...
    @property
    def template_name(self) -> str: ...
    @property
    def row(self) -> List[NyControl]: ...
    @property
    def column(self) -> List[NyControl]: ...
    def iter_elems(self) -> Generator[NyControl]: ...
    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(
        self,
        item: Union[int, slice, Tuple[Union[int, slice], Union[int, slice]]]
    ) -> Union[NyControl, ElemGroup, None]: ...
    def set_gird_update_callback(self, func: __GridUpdateCallback) -> bool: ...
    def remove_gird_update_callback(self, func: __GridUpdateCallback) -> bool: ...
    @property
    def grid_size(self) -> int: ...
    @property
    def elem_count(self) -> int: ...
    @elem_count.setter
    def elem_count(self, val: int) -> None: ...
    @property
    def dimension(self) -> ITuple2: ...
    @dimension.setter
    def dimension(self, val: ITuple2) -> None: ...
    def _return_elem_visible(self, index: int) -> bool: ...
    def _get_elem(self, index: int) -> Optional[NyControl]: ...

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
