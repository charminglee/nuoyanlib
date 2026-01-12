# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-10
#  ⠀
# =================================================


from typing import Dict, Union, Tuple, Callable, TypeVar, Optional, Any, List, Iterator, overload, Iterable, Generic, ClassVar
from mod.client.ui.controls.gridUIControl import GridUIControl
from ....core._types._typing import Self, ITuple2, STuple, UiPathOrNyControl, T, T2, SlotsType
from ....core._types._checker import args_type_check
from ....core._utils import cached_property
from ....utils.enum import GridCallbackType
from ..screen_node import ScreenNodeExtension
from .control import NyControl


__NyControlT = TypeVar("__NyControlT", covariant=True, bound=NyControl)
__GridCallbackType = Callable[[], Any]


class GridData(list, Generic[T, T2]):
    src: List[T]
    """
    网格数据源。
    """
    op_func: Callable[[int, NyControl, T], Any]
    """
    网格数据操作函数，用于实现数据的操作逻辑。
    
    接受三个参数，分别为网格元素索引、元素的NyControl实例、元素对应的数据。网格刷新时会自动对每个元素调用一次该函数，并传入上述三个参数，实现网格元素与数据的自动管理。
    """
    default: Optional[T2]
    """
    网格元素索引超出数据源范围（越界）时使用的默认数据。
    """
    grid: Optional[NyGrid]
    """
    当前网格数据对象所属的网格的 ``NyGrid`` 实例。
    """
    def __init__(
        self: Self,
        src: List[T],
        op_func: Callable[[int, NyControl, T], Any],
        default: Optional[T2] = None,
    ) -> None: ...
    def bind_grid(self, grid: NyGrid) -> None: ...
    def _get_data(self, index: int) -> T: ...
    def bind(self) -> None: ...


def _process_grid_index(index: Union[int, slice], l: int) -> List[int]: ...
def _index_2_coord(i: int, dx: int) -> ITuple2: ...
def _coord_2_index(x: int, y: int, dx: int) -> int: ...


class ElemGroup(Iterable[__NyControlT]):
    __slots__: SlotsType
    _ALLOWED_SET_ATTRS: ClassVar[STuple]
    _ALLOWED_GET_ATTRS: ClassVar[STuple]
    _ALLOWED_METHODS: ClassVar[STuple]
    grid: NyGrid
    cell_list: List[__NyControlT]
    _len: int
    def __init__(self: Self, grid: NyGrid, cell_list: List[__NyControlT]) -> None: ...
    def __iter__(self) -> Iterator[__NyControlT]: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, item: int) -> __NyControlT: ...
    @overload
    def __getitem__(self, item: slice) -> List[__NyControlT]: ...
    def __setattr__(self, key: str, value: Any) -> None: ...
    def __getattr__(self, key: str) -> Union[List[Any], Callable[[...], List[Any]]]: ...


class NyGrid(NyControl):
    __grid_size: int
    __template_name: str
    _callback_map: Dict[str, List[__GridCallbackType]]
    _loaded: bool
    _base_control: GridUIControl
    is_stack_grid: bool
    """
    是否是StackGrid。
    """
    cell_visible_binding: str
    """
    用于控制网格元素visible的绑定名称。
    """
    collection_name_: str
    """
    网格集合名称。
    """
    gd_obj: Optional[GridData]
    """
    绑定到当前网格的网格数据对象。
    """
    def __init__(
        self: Self,
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
    @cached_property
    def template_name(self) -> str: ...
    @property
    def rows(self) -> List[List[NyControl]]: ...
    @property
    def columns(self) -> List[List[NyControl]]: ...
    @property
    def grid_size(self) -> int: ...
    @grid_size.setter
    def grid_size(self, val: int) -> None: ...
    @property
    def dimension(self) -> ITuple2: ...
    @dimension.setter
    def dimension(self, val: ITuple2) -> None: ...
    @args_type_check((int, slice, tuple), is_method=True)
    def __getitem__(
        self,
        item: Union[int, slice, Tuple[Union[int, slice], Union[int, slice]]]
    ) -> Union[NyControl, ElemGroup, None]: ...
    def get_cell_index(self, cell: UiPathOrNyControl) -> int: ...
    def update_grid_data(self) -> None: ...
    @args_type_check(GridData, is_method=True)
    def bind_data(self, gd: GridData) -> None: ...
    def get_cell(self, index: int) -> Optional[NyControl]: ...
    def get_all_cells(self) -> List[NyControl]: ...
    def set_callback(
        self,
        func: __GridCallbackType,
        cb_type: GridCallbackType = GridCallbackType.UPDATE,
    ) -> bool: ...
    def remove_callback(
        self,
        func: __GridCallbackType,
        cb_type: GridCallbackType = GridCallbackType.UPDATE,
    ) -> bool: ...
    GetCellIndex = get_cell_index
    UpdateGridData = update_grid_data
    BindData = bind_data
    GetCell = get_cell
    GetAllCells = get_all_cells
    SetCallback = set_callback
    RemoveCallback = remove_callback
    def _return_cell_visible(self, index: int) -> bool: ...
    SetGridDimension = GridUIControl.SetGridDimension
    GetGridItem = GridUIControl.GetGridItem
