# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


from typing import List, Tuple, ClassVar, Optional, Any, Dict, Generator, Callable, Union, Type
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.CustomUIScreenProxy import CustomUIScreenProxy
from ...core._types._typing import FTuple3, FTuple2, Args, Kwargs, NyControlTypes, F, TypeT, NyScreenBaseT
from .nyc import NyControl, NyImage
from ...core._utils import dualmethod


def screen(
    namespace: str,
    name: str = "main",
    *,
    is_hud: bool = False,
    bind_entity_id: Optional[str] = None,
    bind_offset: FTuple3 = (0, 1, 0),
    bind_world_position: Optional[Tuple[int, FTuple3]] = None,
    auto_scale: bool = True,
    mini_map_root_path: str = "",
    auto_show: bool = True,
    push_to_ui_stack: bool = False,
    enabled_deferred_init: bool = False,
) -> Callable[[TypeT], TypeT]: ...
def screen_proxy(
    namespace: str,
    name: str,
    *,
    enabled_deferred_init: bool = False,
) -> Callable[[TypeT], TypeT]: ...


class NyScreenBase(object):
    ROOT_PANEL_PATH: ClassVar[str]
    """ 基类画布的根面板（root_screen_panel）路径。 """
    AUTO_SAVE_INTERVAL: ClassVar[int]
    """ 自动保存间隔，单位为 tick 。 """
    namespace: ClassVar[str]
    """ UI命名空间，对应 UI json 中 ``"namespace"`` 字段的值。 """
    name: ClassVar[str]
    """ UI画布名称，对应 UI json 中想要创建的画布的名称。 """
    full_name: ClassVar[str]
    """ UI完整名称，格式为 ``<namespace>.<name>`` 。 """
    is_hud: ClassVar[bool]
    """ 是否为 HUD 界面的UI。 """
    bind_entity_id: ClassVar[Optional[str]]
    """ 绑定的实体ID。 """
    bind_offset: ClassVar[FTuple3]
    """ 与绑定实体的偏移量。 """
    bind_world_position: ClassVar[Optional[Tuple[int, FTuple3]]]
    """ 第一个元素为绑定的维度，第二个为世界坐标。 """
    auto_scale: ClassVar[bool]
    """ 绑定实体或世界坐标时是否会自动根据目标与本地玩家的距离动态缩放UI大小。 """
    mini_map_root_path: ClassVar[str]
    """ 小地图控件根路径。 """
    auto_show: ClassVar[bool]
    """ 是否在 ``UiInitFinished`` 事件触发后自动创建并显示UI。 """
    push_to_ui_stack: ClassVar[bool]
    """ 是否使用堆栈管理的方式（Push）创建UI。 """
    enabled_deferred_init: ClassVar[bool]
    """
    是否启用延迟初始化。
    
    启用时UI类的 ``__init__()`` 方法将推迟到UI创建完毕后触发，此时可以在 ``__init__()`` 方法内正常执行各种UI控件接口，从而不必写在 ``Create()`` 或 ``OnCreate()`` 方法里。
    """
    _screen_node: ScreenNode
    _nyc_cache_map: Dict[str, NyControlTypes]
    _ui_pos_data_key: str
    _ui_pos_data: Dict[str, FTuple2]
    _ui_default_pos_data: Dict[str, FTuple2]
    _frame_anim_data: Dict[str, Dict[str, Any]]
    _binging_data: Dict[Union[Callable, Tuple[Callable, object]], Tuple[Callable, bool]]
    _tick: int
    _is_dirty: bool
    root_panel: NyControl
    """
    当前界面根面板的 ``NyControl`` 实例。
    
    当界面继承基类画布时，根面板为 ``root_screen_panel`` ，路径为 ``"/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"`` 。
    否则根面板为画布本身，路径为空字符串 ``""`` 。
    """
    has_created: bool
    """
    UI界面是否已创建完成。
    
    若 ``has_created`` 为True，则此时UI界面的 ``.Create()`` 或 ``.OnCreate()`` 方法已执行完毕。
    """
    is_base_screen: bool
    """ 当前界面是否是基类画布。 """
    is_destroyed: bool
    def __init__(self) -> None: ...
    def __ui_create__(self) -> None: ...
    def __ui_destroy__(self) -> None: ...
    def __ui_update__(self) -> None: ...
    def __ui_deactive__(self) -> None: ...
    def __ui_active__(self) -> None: ...
    @property
    def is_on_top(self) -> bool: ...
    @classmethod
    def instance(cls: Type[NyScreenBaseT]) -> Optional[NyScreenBaseT]: ...
    @classmethod
    def all_instances(cls: Type[NyScreenBaseT]) -> List[NyScreenBaseT]: ...
    @dualmethod
    def show(self: Union[NyScreenBaseT, Type[NyScreenBaseT]]) -> Optional[NyScreenBaseT]: ...
    @dualmethod
    def hide(self: Union[NyScreenBase, Type[NyScreenBase]]) -> bool: ...
    @classmethod
    def create_new(cls: Type[NyScreenBaseT], param: Optional[dict] = None) -> Optional[NyScreenBaseT]: ...
    @dualmethod
    def destroy(self: Union[NyScreenBase, Type[NyScreenBase]]) -> bool: ...
    def build_binding(self, func: Callable, flag: int, binding_name: str = "", collection_name: str = "") -> bool: ...
    def unbuild_binding(self, func: Callable) -> bool: ...
    def _create_binding_proxy(
        self,
        func: Callable,
        flag: int,
        binding_name: str = "",
        collection_name: str = "",
    ) -> Callable: ...
    def _destroy_nyc(self, nyc: NyControl) -> None: ...
    @staticmethod
    def button_callback(
        btn_path: str,
        *callback_types: int,
        touch_event_params: Optional[dict] = None,
    ) -> Callable[[F], F]: ...
    def _process_button_callback(self) -> None: ...
    def _expend_path(self, path: str) -> Generator[str]: ...
    def _get_all_ui_paths(self) -> List[str]: ...
    def reset_all_ui_pos(self) -> bool: ...
    def clear_all_ui_pos_data(self) -> bool: ...
    def _set_ui_pos_data(self, path: str, pos: Optional[FTuple2]) -> bool: ...
    def _set_ui_default_pos_data(self, path: str, pos: FTuple2) -> bool: ...
    def _save_all_ui_pos_data(self) -> bool: ...
    def _get_all_ui_pos_data(self) -> Dict[str, FTuple2]: ...
    def _update_all_ui_pos(self) -> None: ...
    def _play_frame_anim(
        self,
        ny_image: NyImage,
        tex_path: str,
        frame_count: int,
        frame_rate: int,
        stop_frame: int = -1,
        loop: bool = False,
        callback: Optional[Callable] = None,
        args: Optional[Args] = None,
        kwargs: Optional[Kwargs] = None,
    ) -> None: ...
    def _pause_frame_anim(self, ny_image: NyImage) -> None: ...
    def _stop_frame_anim(self, ny_image: NyImage) -> None: ...
    def is_control_exist(self, path: str) -> bool: ...
    set_bind_world_position = ScreenNode.SetBindWorldPosition
    set_screen_visible = ScreenNode.SetScreenVisible
    change_bind_entity_id = ScreenNode.ChangeBindEntityId
    bind_virtual_world_model = ScreenNode.BindVirtualWorldModel
    change_bind_offset = ScreenNode.ChangeBindOffset
    change_bind_auto_scale = ScreenNode.ChangeBindAutoScale
    get_bind_entity_id = ScreenNode.GetBindEntityId
    get_bind_world_position = ScreenNode.GetBindWorldPosition
    get_bind_offset = ScreenNode.GetBindOffset
    get_bind_auto_scale = ScreenNode.GetBindAutoScale
    clone = ScreenNode.Clone
    get_children_name = ScreenNode.GetChildrenName
    get_all_children_path = ScreenNode.GetAllChildrenPath
    remove_component = ScreenNode.RemoveComponent
    set_remove = ScreenNode.SetRemove
    create_child_control = ScreenNode.CreateChildControl
    remove_child_control = ScreenNode.RemoveChildControl
    set_ui_model = ScreenNode.SetUiModel
    set_ui_entity = ScreenNode.SetUiEntity
    set_ui_model_scale = ScreenNode.SetUiModelScale
    update_screen = ScreenNode.UpdateScreen
    set_stack_grid_count = ScreenNode.SetStackGridCount
    set_select_control = ScreenNode.SetSelectControl
    get_rich_text_item = ScreenNode.GetRichTextItem
    set_is_hud = ScreenNode.SetIsHud
    get_is_hud = ScreenNode.GetIsHud
    get_screen_name = ScreenNode.GetScreenName
    get_self = ScreenNode.GetSelf
    get_base_uicontrol = ScreenNode.GetBaseUIControl


class NyScreenNode(NyScreenBase, ScreenNode):
    __user_init: ClassVar[Optional[Callable[[NyScreenNode, str, str, Optional[dict]], None]]]
    __user_init_args: ClassVar[Optional[Tuple[str, str, Optional[dict]]]]
    __inited: bool
    def __new__(cls, namespace: str, name: str, param: Optional[dict] = None) -> NyScreenNode: ...
    def __init__(self, namespace: str, name: str, param: Optional[dict] = None) -> None: ...
    def __ui_create__(self) -> None: ...


class NyScreenProxy(NyScreenBase, CustomUIScreenProxy):
    __user_init: ClassVar[Optional[Callable[[NyScreenProxy, str, ScreenNode], None]]]
    __user_init_args: ClassVar[Optional[Tuple[str, ScreenNode]]]
    __inited: bool
    def __new__(cls, screen_name: str, screen_node: ScreenNode) -> NyScreenProxy: ...
    def __init__(self, screen_name: str, screen_node: ScreenNode) -> None: ...
    def __ui_create__(self) -> None: ...
    @classmethod
    def register_proxy(cls) -> bool: ...
    get_screen_node = CustomUIScreenProxy.GetScreenNode
    get_screen_name = CustomUIScreenProxy.GetScreenName
