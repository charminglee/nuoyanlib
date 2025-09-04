# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-04
|
| ==============================================
"""


from typing import Dict, Union, Tuple, Callable, TypeVar, Optional, Any, List, Iterator, overload, Iterable, Sized, Generic, ClassVar, Sequence
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from .control import NyControl
from ...._core._types._typing import ITuple2, STuple, UiPathOrNyControl
from ...._core._types._checker import args_type_check
from ...._core._utils import cached_property
from ...._core.event._events import ClientEventEnum as Events
from ....utils.enum import GridCallbackType
from ..screen_node import ScreenNodeExtension


_T = TypeVar("_T")
_T2 = TypeVar("_T2")
_T_co = TypeVar("_T_co", covariant=True, bound=NyControl)
__GridCallbackType = Callable[[], Any]


class GridData(list, Generic[_T, _T2]):
    src: List[_T]
    """
    | 网格数据源。
    """
    op_func: Callable[[int, NyControl, _T], Any]
    """
    | 网格数据操作函数，用于实现数据的操作逻辑。
    | 接受三个参数，分别为网格元素索引、元素的NyControl实例、元素对应的数据。网格刷新时会自动对每个元素调用一次该函数，并传入上述三个参数，实现网格元素与数据的自动管理。
    """
    default: Optional[_T2]
    """
    | 网格元素索引超出数据源范围（越界）时使用的默认数据。
    """
    grid: Optional[NyGrid]
    """
    | 当前网格数据对象所属的网格的 ``NyGrid`` 实例。
    """
    def __init__(
        self: ...,
        src: List[_T],
        op_func: Callable[[int, NyControl, _T], Any],
        default: Optional[_T2] = None,
    ) -> None: ...
    def bind_grid(self, grid: NyGrid) -> None: ...
    def _get_data(self, index: int) -> _T: ...
    def bind(self) -> None: ...


def _process_grid_index(index: Union[int, slice], l: int) -> List[int]: ...
def _index_2_coord(i: int, dx: int) -> ITuple2: ...
def _coord_2_index(x: int, y: int, dx: int) -> int: ...


class ElemGroup(Iterable[_T_co]):
    __slots__: ClassVar[STuple]
    _ALLOWED_SET_ATTRS: ClassVar[STuple]
    _ALLOWED_GET_ATTRS: ClassVar[STuple]
    _ALLOWED_METHODS: ClassVar[STuple]
    grid: NyGrid
    cell_list: List[_T_co]
    _len: int
    def __init__(self: ..., grid: NyGrid, cell_list: List[_T_co]) -> None: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, item: int) -> _T_co: ...
    @overload
    def __getitem__(self, item: slice) -> List[_T_co]: ...
    def __setattr__(self, key: str, value: Any) -> None: ...
    def __getattr__(self, key: str) -> Union[List[Any], Callable[[...], List[Any]]]: ...


class NyGrid(NyControl):
    __grid_size: int
    __template_name: str
    _callback_map: Dict[str, List[__GridCallbackType]]
    _loaded: bool
    base_control: GridUIControl
    """
    | 网格 ``GridUIControl`` 实例。
    """
    is_stack_grid: bool
    """
    | 是否是StackGrid。
    """
    cell_visible_binding: str
    """
    | 用于控制网格元素visible的绑定名称。
    """
    collection_name_: str
    """
    | 网格集合名称。
    """
    gd_obj: Optional[GridData]
    """
    | 绑定到当前网格的网格数据对象。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        grid_control: GridUIControl,
        /,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        cell_visible_binding: str = "",
        collection_name: str = "",
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def __grid_update__(self) -> None: ...
    def get_cell_index(self, cell: UiPathOrNyControl) -> int: ...
    @args_type_check(GridData, is_method=True)
    def bind_data(self, gd: GridData) -> None: ...
    @cached_property
    def template_name(self) -> str: ...
    @property
    def rows(self) -> List[List[NyControl]]: ...
    @property
    def columns(self) -> List[List[NyControl]]: ...
    def get_cell(self, index: int) -> Optional[NyControl]: ...
    def get_all_cells(self) -> List[NyControl]: ...
    def set_callback(self, func: __GridCallbackType, cb_type: str = GridCallbackType.UPDATE) -> bool: ...
    def remove_callback(self, func: __GridCallbackType, cb_type: str = GridCallbackType.UPDATE) -> bool: ...
    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(
        self,
        item: Union[int, slice, Tuple[Union[int, slice], Union[int, slice]]]
    ) -> Union[NyControl, ElemGroup, None]: ...
    @property
    def grid_size(self) -> int: ...
    @grid_size.setter
    def grid_size(self, val: int) -> None: ...
    @property
    def dimension(self) -> ITuple2: ...
    @dimension.setter
    def dimension(self, val: ITuple2) -> None: ...
    def _return_cell_visible(self, index: int) -> bool: ...

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
