# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-13
|
| ==============================================
"""


from weakref import proxy
from types import GeneratorType
from ...._core import _error
from ...._core._utils import args_type_check, cached_property
from ....client.ui.ui_utils import ControlType, get_children_path_by_level, get_parent_path


__all__ = [
    "NyControl",
]


class NyControl(object):
    """
    | 创建 ``NyControl`` 通用UI控件实例。
    | 兼容ModSDK ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
    :param BaseUIControl control: 通过GetBaseUIControl()获取的控件实例
    """

    _CONTROL_TYPE = ControlType.base_control

    def __init__(self, screen_node_ex, control, **kwargs):
        from ..screen_node import ScreenNodeExtension
        if not isinstance(screen_node_ex, ScreenNodeExtension):
            raise TypeError(
                "the UI class where '%s' is located must inherit 'ScreenNodeExtension'"
                % self.__class__.__name__
            )
        self._screen_node = proxy(screen_node_ex._screen_node)
        self.ui_node = proxy(screen_node_ex)
        self.base_control = control

    def __getattr__(self, name):
        # 尝试调用ModSDK方法
        return getattr(self.base_control, name)

    @args_type_check(str, is_method=True)
    def __div__(self, other):
        """
        | 根据相对路径返回子控件的 ``NyControl`` 实例。

        -----

        :param str other: 相对路径

        :return: 子控件的NyControl实例
        :rtype: NyControl
        """
        if not other.startswith("/"):
            other = "/" + other
        return NyControl.create(self.ui_node, self.path + other)

    def __destroy__(self):
        self._screen_node = None
        self.base_control = None
        self.ui_node = None

    # region API ===================================================================================

    def iter_children_ny_control(self, level=1):
        """
        [迭代器]

        | 返回当前控件指定层级子控件的 ``NyControl`` 实例的迭代器。

        -----

        :param int level: 子控件层级，默认为1，传入0或负值时获取所有层级

        :return: 迭代器
        :rtype: GeneratorType
        """
        all_path = get_children_path_by_level(self.base_control, self._screen_node, level)
        for p in all_path:
            yield NyControl.create(self.ui_node, p)

    def iter_children_path(self, level=1):
        """
        [迭代器]

        | 返回当前控件指定层级子控件的路径的迭代器。

        -----

        :param int level: 子控件层级，默认为1，传入0或负值时获取所有层级

        :return: 迭代器
        :rtype: GeneratorType
        """
        return get_children_path_by_level(self.base_control, self._screen_node, level)

    @cached_property
    def path(self):
        """
        [只读属性]

        | 控件路径。

        :rtype: str
        """
        return self.base_control.GetPath()

    @cached_property
    def parent_path(self):
        """
        [只读属性]

        | 父控件路径。

        :rtype: str
        """
        return get_parent_path(self.path)

    @cached_property
    def parent_ny_control(self):
        """
        [只读属性]

        | 父控件 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.create(self.ui_node, self.parent_path)

    @classmethod
    def create(cls, screen_node_ex, path_or_control, **kwargs):
        """
        | 创建一个类型与调用该方法的类相同的Ny控件实例。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
        :param str path_or_control: 控件路径或BaseUIControl实例
        :param Any kwargs: 参数

        :return: Ny控件实例
        :rtype: NyControl
        """
        return screen_node_ex._create_nyc(path_or_control, cls, **kwargs)

    def destroy(self):
        """
        | 销毁控件，将控件从画布上移除。

        -----

        :return: 无
        :rtype: None
        """
        self.ui_node._destroy_nyc(self)

    # endregion

    # region conversion ===================================================================================

    def to_button(self, touch_event_params=None):
        """
        | 转换为 ``NyButton`` 实例。

        -----

        :param dict[str,Any]|None touch_event_params: 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton实例
        :rtype: NyButton
        """
        from . import NyButton
        return NyButton.create(self.ui_node, self.path, touch_event_params=touch_event_params)

    def to_image(self):
        """
        [只读属性]

        | 转换为 ``NyImage`` 实例。

        :rtype: NyImage
        """
        from . import NyImage
        return NyImage.create(self.ui_node, self.path)

    def to_label(self):
        """
        [只读属性]

        | 转换为 ``NyLabel`` 实例。

        :rtype: NyLabel
        """
        from . import NyLabel
        return NyLabel.create(self.ui_node, self.path)

    def to_input_panel(self):
        """
        [只读属性]

        | 转换为 ``NyInputPanel`` 实例。

        :rtype: NyInputPanel
        """
        from . import NyInputPanel
        return NyInputPanel.create(self.ui_node, self.path)

    def to_stack_panel(self):
        """
        [只读属性]

        | 转换为 ``NyStackPanel`` 实例。

        :rtype: NyStackPanel
        """
        from . import NyStackPanel
        return NyStackPanel.create(self.ui_node, self.path)

    def to_edit_box(self):
        """
        [只读属性]

        | 转换为 ``NyEditBox`` 实例。

        :rtype: NyEditBox
        """
        from . import NyEditBox
        return NyEditBox.create(self.ui_node, self.path)

    def to_netease_paper_doll(self):
        """
        [只读属性]

        | 转换为 ``NyPaperDoll`` 实例。

        :rtype: NyPaperDoll
        """
        from . import NyPaperDoll
        return NyPaperDoll.create(self.ui_node, self.path)

    def to_item_renderer(self):
        """
        [只读属性]

        | 转换为 ``NyItemRenderer`` 实例。

        :rtype: NyItemRenderer
        """
        from . import NyItemRenderer
        return NyItemRenderer.create(self.ui_node, self.path)

    def to_scroll_view(self):
        """
        [只读属性]

        | 转换为 ``NyScrollView`` 实例。

        :rtype: NyScrollView
        """
        from . import NyScrollView
        return NyScrollView.create(self.ui_node, self.path)

    def to_grid(self):
        """
        [只读属性]

        | 转换为 ``NyGrid`` 实例。

        :rtype: NyGrid
        """
        from . import NyGrid
        return NyGrid.create(self.ui_node, self.path)

    def to_progress_bar(self):
        """
        [只读属性]

        | 转换为 ``NyProgressBar`` 实例。

        :rtype: NyProgressBar
        """
        from . import NyProgressBar
        return NyProgressBar.create(self.ui_node, self.path)

    def to_toggle(self):
        """
        [只读属性]

        | 转换为 ``NyToggle`` 实例。

        :rtype: NyToggle
        """
        from . import NyToggle
        return NyToggle.create(self.ui_node, self.path)

    def to_slider(self):
        """
        [只读属性]

        | 转换为 ``NySlider`` 实例。

        :rtype: NySlider
        """
        from . import NySlider
        return NySlider.create(self.ui_node, self.path)

    def to_selection_wheel(self):
        """
        [只读属性]

        | 转换为 ``NySelectionWheel`` 实例。

        :rtype: NySelectionWheel
        """
        from . import NySelectionWheel
        return NySelectionWheel.create(self.ui_node, self.path)

    def to_combo_box(self):
        """
        [只读属性]

        | 转换为 ``NyComboBox`` 实例。

        :rtype: NyComboBox
        """
        from . import NyComboBox
        return NyComboBox.create(self.ui_node, self.path)

    def to_mini_map(self):
        """
        [只读属性]

        | 转换为 ``NyMiniMap`` 实例。

        :rtype: NyMiniMap
        """
        from . import NyMiniMap
        return NyMiniMap.create(self.ui_node, self.path)

    # endregion

    # region property proxy ===================================================================================

    @property
    def position(self):
        """
        [可读写属性]

        | 按钮相对于父控件的坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetPosition()

    @position.setter
    def position(self, val):
        """
        [可读写属性]

        | 按钮相对于父控件的坐标。

        :type val: tuple[float,float]
        """
        self.base_control.SetPosition(val)

    @property
    def anchor_from(self):
        """
        [可读写属性]

        | 父控件锚点位置。

        :rtype: str
        """
        return self.base_control.GetAnchorFrom()

    @anchor_from.setter
    def anchor_from(self, val):
        """
        [可读写属性]

        | 父控件锚点位置。

        :type val: str
        """
        self.base_control.SetAnchorFrom(val)

    @property
    def anchor_to(self):
        """
        [可读写属性]

        | 控件自身锚点位置。

        :rtype: str
        """
        return self.base_control.GetAnchorTo()

    @anchor_to.setter
    def anchor_to(self, val):
        """
        [可读写属性]

        | 控件自身锚点位置。

        :type val: str
        """
        self.base_control.SetAnchorTo(val)

    @property
    def clip_offset(self):
        """
        [可读写属性]

        | 控件的裁剪偏移。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetClipOffset()

    @clip_offset.setter
    def clip_offset(self, val):
        """
        [可读写属性]

        | 控件的裁剪偏移。

        :type val: tuple[float,float]
        """
        self.base_control.SetClipOffset(val)

    @property
    def clip_children(self):
        """
        [可读写属性]

        | 是否开启裁剪内容。

        :rtype: bool
        """
        return self.base_control.GetClipsChildren()

    @clip_children.setter
    def clip_children(self, val):
        """
        [可读写属性]

        | 是否开启裁剪内容。

        :type val: bool
        """
        self.base_control.SetClipsChildren(val)

    @property
    def full_position_x(self):
        """
        [可读写属性]

        | 控件的锚点X坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullPosition("x")

    @full_position_x.setter
    def full_position_x(self, val):
        """
        [可读写属性]

        | 控件的锚点X坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullPosition("x", val)

    @property
    def full_position_y(self):
        """
        [可读写属性]

        | 控件的锚点Y坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullPosition("y")

    @full_position_y.setter
    def full_position_y(self, val):
        """
        [可读写属性]

        | 控件的锚点Y坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullPosition("y", val)

    @property
    def full_size_x(self):
        """
        [可读写属性]

        | 控件的X轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullSize("x")

    @full_size_x.setter
    def full_size_x(self, val):
        """
        [可读写属性]

        | 控件的X轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullSize("x", val)

    @property
    def full_size_y(self):
        """
        [可读写属性]

        | 控件的Y轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullSize("y")

    @full_size_y.setter
    def full_size_y(self, val):
        """
        [可读写属性]

        | 控件的Y轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullSize("y", val)

    @property
    def global_position(self):
        """
        [可读写属性]

        | 控件全局坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetGlobalPosition()

    @global_position.setter
    def global_position(self, val):
        """
        [可读写属性]

        | 控件全局坐标。

        :type val: tuple[float,float]
        """
        self.base_control.SetGlobalPosition(val) # NOQA

    @property
    def max_size(self):
        """
        [可读写属性]

        | 控件所允许的最大尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetMaxSize()

    @max_size.setter
    def max_size(self, val):
        """
        [可读写属性]

        | 控件所允许的最大尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetMaxSize(val)

    @property
    def min_size(self):
        """
        [可读写属性]

        | 控件所允许的最小尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetMinSize()

    @min_size.setter
    def min_size(self, val):
        """
        [可读写属性]

        | 控件所允许的最小尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetMinSize(val)

    @property
    def size(self):
        """
        [可读写属性]

        | 控件尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetSize()

    @size.setter
    def size(self, val):
        """
        [可读写属性]

        | 控件尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetSize(val, True)

    @property
    def visible(self):
        """
        [可读写属性]

        | 控件是否显示。

        :rtype: bool
        """
        return self.base_control.GetVisible()

    @visible.setter
    def visible(self, val):
        """
        [可读写属性]

        | 控件是否显示。

        :type val: bool
        """
        self.base_control.SetVisible(val)

    @property
    def alpha(self):
        """
        [只写属性]

        | 控件不透明度。
        """
        raise _error.GetPropertyError("alpha")

    @alpha.setter
    def alpha(self, val):
        """
        [只写属性]

        | 控件不透明度。

        :type val: float
        """
        self.base_control.SetAlpha(val)

    @property
    def layer(self):
        """
        [可读写属性]

        | 控件层级。

        :rtype: int
        """
        return self.base_control.GetLayer() # NOQA

    @layer.setter
    def layer(self, val):
        """
        [可读写属性]

        | 控件层级。

        :type val: int
        """
        self.base_control.SetLayer(val)

    @property
    def touch_enable(self):
        """
        [只写属性]

        | 控件是否可点击交互。
        """
        raise _error.GetPropertyError("touch_enable")

    @touch_enable.setter
    def touch_enable(self, val):
        """
        [只写属性]

        | 控件是否可点击交互。

        :type val: bool
        """
        self.base_control.SetTouchEnable(val)

    # endregion


def __test__():
    from ..screen_node import ScreenNodeExtension
    from ...._core._client.comp import ScreenNode
    class SN(ScreenNodeExtension, ScreenNode):
        pass
    s = SN("", "")
    c = s.create_ny_control("/control")
    c2 = s.create_ny_control("/control2")
    abc = NyControl.create(s, "/abc")
    assert "/abc" in s._nyc_cache
    c = abc / "child"
    assert c.GetPath() == c.path == "/abc/child"
    abc.destroy()
    assert "/abc" not in s._nyc_cache


















