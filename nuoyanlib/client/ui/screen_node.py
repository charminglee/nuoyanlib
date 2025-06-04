# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from ..._core._client import _comp
from ..._core import _listener, _utils, _error
from . import ui_utils as _ui_utils
from .control import NyControl as _NyControl
from .button import NyButton as _NyButton
from .grid import NyGrid as _NyGrid


__all__ = [
    "ScreenNodeExtension",
]


class ScreenNodeExtension(_listener.ClientEventProxy):
    """
    | ScreenNode扩展类，提供更多UI界面功能。
    | 已继承 ``ClientEventProxy`` ，监听事件更便捷。
    """

    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
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

    # noinspection PyUnresolvedReferences
    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._ny_control_cache = {}
        self._ui_pos_data_key = ""
        self._screen_node = None
        if isinstance(self, _comp.CustomUIScreenProxy):
            # 兼容UI代理
            self._screen_node = args[1]
            self.cs = None
            _utils.hook_method(self, "OnCreate", self.__Create)
            _utils.hook_method(self, "OnDestroy", self.__Destroy)
        elif isinstance(self, _comp.ScreenNode):
            self._screen_node = self
            self.cs = args[2].get('__cs__') if len(args) == 3 and isinstance(args[2], dict) else None
            _utils.hook_method(self, "Create", self.__Create)
            _utils.hook_method(self, "Destroy", self.__Destroy)
        else:
            raise _error.ScreenNodeNotFoundError
        self.ny_controls = {}
        self.root_panel = (
            self._screen_node.GetBaseUIControl(ScreenNodeExtension.ROOT_PANEL_PATH)
            or self._screen_node.GetBaseUIControl("")
        )

    # def __setattr__(self, key, value):
    #     # 网易ScreenNode中某些属性被覆盖会导致功能异常且难以排查（如name），因此添加一个限制
    #     if key in ScreenNodeExtension._LIMIT_ATTR and hasattr(self, key):
    #         raise AttributeError("can't set attribute '%s' to '%s'" % (key, self.__class__.__name__))
    #     super(ScreenNodeExtension, self).__setattr__(key, value)

    # System Event Callbacks ===========================================================================================

    def __Create(self):
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (self._screen_node.namespace, self._screen_node.name) # NOQA
        self._recover_ui_pos()

    def __Destroy(self):
        for nyc in self.ny_controls.values():
            nyc.__destroy__()

    # APIs =============================================================================================================

    def CreateNyControl(self, path_or_control):
        """
        | 创建 ``NyControl`` 通用控件实例，可替代 ``GetBaseUIControl()`` 的返回值使用。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyControl控件实例，创建失败返回None
        :rtype: _NyControl|None
        """
        return self._create_nyc(_ui_utils.to_path(path_or_control))

    def CreateNyButton(self, path_or_control, touch_event_params=None):
        """
        | 创建 ``NyButton`` 按钮实例，可替代 ``asButton()`` 的返回值使用。
        | 创建后无需调用 ``AddTouchEventParams()`` 或 ``AddTouchEventParams()`` 接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param dict|None touch_event_params: 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton按钮实例，创建失败返回None
        :rtype: _NyButton|None
        """
        control = self._create_nyc(_ui_utils.to_path(path_or_control), _NyButton)
        if control:
            control.AddTouchEventParams(touch_event_params)
            control.AddHoverEventParams()
            return control

    def CreateNyGrid(self, path_or_control):
        """
        | 创建 ``NyGrid`` 网格实例，可替代 ``asGrid()`` 的返回值使用。
        | 对网格进行操作需要注意一些细节，详见开发指南-界面与交互- `UI说明文档 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/30-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html?key=grid&docindex=4&type=0>`_ 中对Grid控件的描述。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyGrid网格实例，创建失败返回None
        :rtype: _NyGrid|None
        """
        return self._create_nyc(_ui_utils.to_path(path_or_control), _NyGrid)

    def GetAllChildrenPathByLevel(self, path_or_control, level=1):
        """
        | 获取控件的指定层级的所有子控件的路径。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级的所有子控件的路径列表，获取不到时返回空列表
        :rtype: list[str]
        """
        return _ui_utils.get_all_children_path_by_level(path_or_control, self._screen_node, level)

    def GetAllChildrenNyControlByLevel(self, path_or_control, level=1):
        """
        | 获取控件的指定层级的所有子控件的 ``NyControl`` 实例。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级的所有子控件的NyControl实例列表，获取不到时返回空列表
        :rtype: list[_NyControl]
        """
        all_children = _ui_utils.get_all_children_control_by_level(
            path_or_control, self._screen_node, level
        )
        return [self._create_nyc(c.GetPath()) for c in all_children]

    def GetParentPath(self, path_or_control):
        """
        | 获取控件的父控件路径。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件路径，获取不到返回None
        :rtype: str|None
        """
        return _ui_utils.get_parent_path(path_or_control)

    def GetParentNyControl(self, path_or_control):
        """
        | 获取控件的父控件的 ``NyControl`` 实例。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件NyControl实例，获取不到返回None
        :rtype: _NyControl|None
        """
        parent_path = _ui_utils.get_parent_path(path_or_control)
        if parent_path:
            return self._create_nyc(parent_path)

    def ClearAllPosData(self):
        """
        | 删除所有控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        return _ui_utils.save_ui_pos_data(self._ui_pos_data_key, {})

    def SaveAllPosData(self):
        """
        | 保存所有通过 ``set_movable()`` 或 ``set_movable_by_long_click()`` 设置了可拖动的控件的位置数据，下次进入游戏时自动恢复。
        | 为保证安全，超出屏幕边界的按钮不会被保存。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        for control in self.ny_controls.values():
            if isinstance(control, _NyButton) and control.is_movable:
                control.save_pos_data()
        return True

    # Internal =========================================================================================================

    def _create_nyc(self, path, typ=_NyControl, **kwargs):
        control = _ui_utils.to_control(self._screen_node, path, typ._CONTROL_TYPE)
        if not control:
            return
        nyc = typ(self, control, **kwargs)
        self.ny_controls[path] = nyc
        return nyc

    def _recover_ui_pos(self):
        data = _ui_utils.get_ui_pos_data(self._ui_pos_data_key)
        for data_lst in data.values():
            for path, pos in data_lst:
                control = _ui_utils.to_control(self._screen_node, path)
                if control:
                    control.SetPosition(pos)
























