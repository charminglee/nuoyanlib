# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from types import GeneratorType
from ..._core._client.comp import CustomUIScreenProxy, ScreenNode
from ..._core import _error
from ..._core._listener import ClientEventProxy
from ..._core._utils import hook_method
from .ui_utils import (
    to_control, get_ui_pos_data, save_ui_pos_data,
    get_children_path_by_level, get_parent_path,
    UiControlType, to_path,
)
from .nyc import *


__all__ = [
    "ScreenNodeExtension",
]


_UI_CONTROL_TYPE_2_NY_CLS = {
    UiControlType.button: NyButton,
    UiControlType.image: NyImage,
    UiControlType.label: NyLabel,
    UiControlType.input_panel: NyInputPanel,
    UiControlType.stack_panel: NyStackPanel,
    UiControlType.edit_box: NyEditBox,
    UiControlType.scroll_view: NyScrollView,
    UiControlType.grid: NyGrid,
    UiControlType.toggle: NyToggle,
    UiControlType.slider: NySlider,
    UiControlType.selection_wheel: NySelectionWheel,

    # UiControlType.panel: NyComboBox,
    # UiControlType.panel: NyProgressBar,
    # UiControlType.custom: NyMiniMap,
    # UiControlType.custom: NyItemRenderer,
}


class ScreenNodeExtension(ClientEventProxy):
    """
    | ScreenNode扩展类，提供更多UI界面功能。
    | 已继承 ``ClientEventProxy`` ，监听事件更便捷。
    """

    _LIMIT_ATTR = [
        "namespace",
        "name",
        "full_name",
        "screen_name",
        "component_path",
        "parent",
        "children",
        "visible",
        "enable",
        "removed",
        "def_key",
        "org_key",
        "input_mode",
        "is_push_screen",
        "touch_with_mouse",
        "dirty",
        "fresh_async",
    ]
    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._nyc_cache = {}
        self._ui_pos_data_key = ""
        self._screen_node = None
        self.cs = None
        if isinstance(self, CustomUIScreenProxy):
            # 兼容UI代理
            self._screen_node = args[1]
            hook_method(self, "OnCreate", self.__create__) # NOQA
            hook_method(self, "OnDestroy", self.__destroy__) # NOQA
        elif isinstance(self, ScreenNode):
            self._screen_node = self
            if len(args) == 3 and args[2]:
                self.cs = args[2].get('__cs__')
            hook_method(self, "Create", self.__create__) # NOQA
            hook_method(self, "Destroy", self.__destroy__) # NOQA
        else:
            raise _error.ScreenNodeNotFoundError
        self.root_panel = (
            self._screen_node.GetBaseUIControl(ScreenNodeExtension.ROOT_PANEL_PATH) # NOQA
            or self._screen_node.GetBaseUIControl("") # NOQA
        )

    # def __setattr__(self, key, value):
    #     # 网易ScreenNode中某些属性被覆盖会导致功能异常且难以排查（如name），因此添加一个限制
    #     if key in ScreenNodeExtension._LIMIT_ATTR and hasattr(self, key):
    #         raise AttributeError("can't set attribute '%s' to '%s'" % (key, self.__class__.__name__))
    #     super(ScreenNodeExtension, self).__setattr__(key, value)

    def __create__(self):
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (self._screen_node.namespace, self._screen_node.name) # NOQA
        self._recover_ui_pos()

    def __destroy__(self):
        for nyc in self._nyc_cache.values():
            nyc.__destroy__()
        self._nyc_cache.clear()
        self._screen_node = None
        self.cs = None
        self.root_panel = None

    # region API ===================================================================================

    def create_ny_control(self, path_or_control):
        """
        | 创建 ``NyControl`` 通用控件实例，可替代 ``.GetBaseUIControl()`` 的返回值使用。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyControl控件实例，创建失败返回None
        :rtype: NyControl|None
        """
        return self._create_nyc(path_or_control, NyControl)

    def create_ny_button(self, path_or_control, touch_event_params=None):
        """
        | 创建 ``NyButton`` 按钮实例，可替代 ``.asButton()`` 的返回值使用。
        | 创建后无需调用 ``.AddTouchEventParams()`` 或 ``.AddTouchEventParams()`` 接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param dict|None touch_event_params: 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton按钮实例，创建失败返回None
        :rtype: NyButton|None
        """
        return self._create_nyc(path_or_control, NyButton, touch_event_params=touch_event_params)

    def create_ny_grid(self, path_or_control, is_stack_grid=False):
        """
        | 创建 ``NyGrid`` 网格实例，可替代 ``.asGrid()`` 的返回值使用。
        | 对网格进行操作需要注意一些细节，详见开发指南-界面与交互- `UI说明文档 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/30-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html?key=grid&docindex=4&type=0>`_ 中对Grid控件的描述。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param bool is_stack_grid: 是否是StackGrid，默认为False

        :return: NyGrid网格实例，创建失败返回None
        :rtype: NyGrid|None
        """
        return self._create_nyc(path_or_control, NyGrid, is_stack_grid=is_stack_grid)

    def get_children_path_by_level(self, path_or_control, level=1):
        """
        [迭代器]

        | 获取控件的指定层级的所有子控件的路径，返回迭代器。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级所有子控件路径的迭代器，获取不到时返回空迭代器
        :rtype: GeneratorType
        """
        return get_children_path_by_level(path_or_control, self._screen_node, level)

    def get_children_ny_control_by_level(self, path_or_control, level=1):
        """
        [迭代器]

        | 获取控件的指定层级的所有子控件的 ``NyControl`` 实例，返回迭代器。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级所有子控件的NyControl实例的迭代器，获取不到时返回空迭代器
        :rtype: GeneratorType
        """
        all_path = get_children_path_by_level(path_or_control, self._screen_node, level)
        for p in all_path:
            yield self._create_nyc(p, NyControl)

    def get_parent_path(self, path_or_control):
        """
        | 获取控件的父控件路径。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件路径，获取不到返回None
        :rtype: str|None
        """
        return get_parent_path(path_or_control)

    def get_parent_ny_control(self, path_or_control):
        """
        | 获取控件的父控件 ``NyControl`` 实例。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件的NyControl实例，获取不到返回None
        :rtype: NyControl|None
        """
        parent_path = get_parent_path(path_or_control)
        if parent_path:
            return self._create_nyc(parent_path, NyControl)

    def clear_all_pos_data(self):
        """
        | 删除所有控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        return save_ui_pos_data(self._ui_pos_data_key, {})

    def save_all_pos_data(self):
        """
        | 保存所有通过 ``.set_movable()`` 或 ``.set_movable_by_long_click()`` 设置了可拖动的控件的位置数据，下次进入游戏时自动恢复。
        | 为保证安全，超出屏幕边界的按钮不会被保存。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        for nyc in self._nyc_cache.values():
            if isinstance(nyc, NyButton) and nyc.is_movable:
                nyc.save_pos_data()
        return True

    CreateNyControl = create_ny_control
    CreateNyButton = create_ny_button
    CreateNyGrid = create_ny_grid
    GetChildrenPathByLevel = get_children_path_by_level
    GetChildrenNyControlByLevel = get_children_ny_control_by_level
    GetParentPath = get_parent_path
    GetParentNyControl = get_parent_ny_control
    ClearAllPosData = clear_all_pos_data
    SaveAllPosData = save_all_pos_data

    # endregion

    # region Internal ===================================================================================

    def _create_nyc(self, path_or_control, typ, **kwargs):
        path = to_path(path_or_control)
        if path in self._nyc_cache:
            return self._nyc_cache[path]
        control = to_control(self._screen_node, path_or_control, typ._CONTROL_TYPE)
        if control:
            nyc = typ(self, control, **kwargs)
            self._nyc_cache[path] = nyc
            return nyc

    def _destroy_nyc(self, nyc):
        nyc.__destroy__()
        self._nyc_cache.pop(nyc.path, None)
        self._screen_node.RemoveChildControl(nyc.base_control)

    def _recover_ui_pos(self):
        data = get_ui_pos_data(self._ui_pos_data_key)
        for data_lst in data.values():
            for path, pos in data_lst:
                control = to_control(self._screen_node, path)
                if control:
                    control.SetPosition(pos)

    # endregion


def __test__():
    class SN(ScreenNodeExtension, ScreenNode):
        def __init__(self, namespace, name, param):
            super(SN, self).__init__(namespace, name, param)
    sn = SN("abc", "ui", {})
    c1 = sn.create_ny_control("/path/to/control1")
    c2 = sn.create_ny_button("/path/to/control2")
    c3 = sn.create_ny_grid("/path/to/control3")


















