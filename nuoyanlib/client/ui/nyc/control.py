# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-25
|
| ==============================================
"""


from types import GeneratorType
from ...._core import _error
from ...._core._utils import cached_property
from ...._core._types._checker import args_type_check
from ....client.ui.ui_utils import get_children_path_by_level, get_parent_path
from ....utils.enum import ControlType


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

    :raise TypeError: 控件所在的UI类必须继承ScreenNodeExtension，否则抛出该异常
    """

    _CONTROL_TYPE = ControlType.BASE_CONTROL

    def __init__(self, screen_node_ex, control, **kwargs):
        from ..screen_node import ScreenNodeExtension
        if not isinstance(screen_node_ex, ScreenNodeExtension):
            raise TypeError(
                "the UI class where '%s' is located must inherit 'ScreenNodeExtension'"
                % self.__class__.__name__
            )
        self._screen_node = screen_node_ex._screen_node
        self._kwargs = kwargs
        self.ui_node = screen_node_ex
        self.base_control = control

    def __getattr__(self, name):
        # 尝试调用ModSDK方法
        return getattr(self.base_control, name)

    @args_type_check(str, is_method=True)
    def __truediv__(self, other):
        """
        | 根据相对路径返回子控件的 ``NyControl`` 实例。

        -----

        :param str other: 相对路径

        :return: 子控件的NyControl实例
        :rtype: NyControl
        """
        if not other.startswith("/"):
            other = "/" + other
        return NyControl.from_path(self.ui_node, self.path + other)

    __div__ = __truediv__

    def __destroy__(self):
        self._screen_node = None
        self.base_control = None
        self.ui_node = None

    # region APIs ======================================================================================================

    def new_child(self, def_name, child_name, force_update=True):
        """
        | 为当前控件创建一个新的子控件

        -----

        :param str def_name: UI控件路径，格式为"namespace.control_name"；namespace对应UI json文件中"namespace"对应的值，UI编辑器生成的UI json文件该值等于文件名；control_name对应想创建的控件的名称，该控件需要置于UI json文件顶层（即与main画布同级，不能是任何一个控件的子控件），或在UI编辑器中将该控件添加至控件库
        :param str child_name: 子控件名称
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量新建子控件操作且在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 子控件NyControl实例，如果该子控件已经存在则返回已存在的子控件
        :rtype: NyControl
        """
        child = self._screen_node.CreateChildControl(def_name, child_name, self.base_control, force_update)
        if child:
            return NyControl.from_control(self.ui_node, child)

    def clone_to(self, parent, name="", sync_refresh=True, force_update=True):
        """
        | 将当前控件克隆到指定控件下。

        -----

        :param str|BaseUIControl|NyControl parent: 父控件路径或实例
        :param str name: 新控件的名称，默认使用当前控件的名称；若名称已存在，则克隆失败
        :param bool sync_refresh: 是否需要同步刷新，默认为True；设为True时游戏在同一帧计算该控件的size等相关数据，设为False则在下一帧进行计算；如同一帧有大量clone操作建议设为False，操作结束后调用一次UpdateScreen接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则按照sync_refresh逻辑进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量clone操作且非在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 新控件的Ny控件实例，类型与当前控件实例相同，克隆失败时返回None
        :rtype: NyControl|None
        """
        # todo：处理名称重复
        parent_path = parent if isinstance(parent, str) else parent.GetPath()
        if not name:
            name = self.name
        ret = self._screen_node.Clone(self.path, parent_path, name, sync_refresh, force_update)
        if ret:
            new_path = parent_path + "/" + name
            return self.__class__.from_path(self.ui_node, new_path, **self._kwargs)

    def clone_from(self, control, name="", sync_refresh=True, force_update=True):
        """
        | 将指定控件克隆到当前控件下。

        -----

        :param str|BaseUIControl|NyControl control: 控件路径或实例
        :param str name: 新控件的名称，默认使用当前控件的名称；若名称已存在，则克隆失败
        :param bool sync_refresh: 是否需要同步刷新，默认为True；设为True时游戏在同一帧计算该控件的size等相关数据，设为False则在下一帧进行计算；如同一帧有大量clone操作建议设为False，操作结束后调用一次UpdateScreen接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则按照sync_refresh逻辑进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量clone操作且非在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 新控件的NyControl实例，克隆失败时返回None
        :rtype: NyControl|None
        """
        # todo：处理名称重复
        control_path = control if isinstance(control, str) else control.GetPath()
        if not name:
            name = self.name
        ret = self._screen_node.Clone(control_path, self.path, name, sync_refresh, force_update)
        if ret:
            new_path = self.path + "/" + name
            return NyControl.from_path(self.ui_node, new_path)

    def iter_children_control(self, level=1):
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
            yield NyControl.from_path(self.ui_node, p)

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

    @classmethod
    def from_path(cls, screen_node_ex, path, **kwargs):
        """
        | 根据控件路径创建一个类型与调用该方法的类相同的Ny控件实例。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
        :param str path: 控件路径

        :return: Ny控件实例
        :rtype: NyControl
        """
        return screen_node_ex._create_nyc(path, cls, **kwargs)

    @classmethod
    def from_control(cls, screen_node_ex, control, **kwargs):
        """
        | 根据 ``BaseUIControl`` 实例创建一个类型与调用该方法的类相同的Ny控件实例。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
        :param BaseUIControl control: BaseUIControl实例

        :return: Ny控件实例
        :rtype: NyControl
        """
        return screen_node_ex._create_nyc(control.GetPath(), cls, **kwargs)

    def destroy(self):
        """
        | 销毁控件，将控件从画布上移除。

        -----

        :return: 无
        :rtype: None
        """
        self.ui_node._destroy_nyc(self)

    @property
    def real_visible(self):
        """
        [只读属性]

        | 判断控件是否真正可见。
        | 与ModSDK接口 ``.GetVisible()`` 不同的是， ``.GetVisible()`` 获取的是当前控件的 ``visible`` 值。当父控件的 ``visible`` 为 ``False`` ，而当前控件的 ``visible`` 仍为 ``True`` 时，实际上当前控件是不可见的，此时 ``.real_visible`` 将返回 ``False`` 。

        :rtype: bool
        """
        parent = self.parent_control
        while parent:
            if not parent.visible:
                return False
            parent = parent.parent_control
        return self.visible

    @cached_property
    def name(self):
        """
        [只读属性]

        | 控件名称。

        :rtype: str
        """
        return self.path.split("/")[-1]

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

        | 父控件路径，没有父控件时返回None，若父控件为根画布（main），返回空字符串。

        :rtype: str
        """
        return get_parent_path(self.path)

    @cached_property
    def parent_control(self):
        """
        [只读属性]

        | 父控件 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.from_path(self.ui_node, self.parent_path)

    # endregion

    # region Conversion ================================================================================================

    def to_button(self, **kwargs):
        """
        | 转换为 ``NyButton`` 实例。

        -----

        :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton实例
        :rtype: NyButton
        """
        from . import NyButton
        return NyButton.from_path(self.ui_node, self.path, **kwargs)

    def to_image(self, **kwargs):
        """
        | 转换为 ``NyImage`` 实例。

        -----

        :return: NyImage实例
        :rtype: NyImage
        """
        from . import NyImage
        return NyImage.from_path(self.ui_node, self.path, **kwargs)

    def to_label(self, **kwargs):
        """
        | 转换为 ``NyLabel`` 实例。

        -----

        :return: NyLabel实例
        :rtype: NyLabel
        """
        from . import NyLabel
        return NyLabel.from_path(self.ui_node, self.path, **kwargs)

    def to_input_panel(self, **kwargs):
        """
        | 转换为 ``NyInputPanel`` 实例。

        -----

        :return: NyInputPanel实例
        :rtype: NyInputPanel
        """
        from . import NyInputPanel
        return NyInputPanel.from_path(self.ui_node, self.path, **kwargs)

    def to_stack_panel(self, **kwargs):
        """
        | 转换为 ``NyStackPanel`` 实例。

        -----

        :return: NyStackPanel实例
        :rtype: NyStackPanel
        """
        from . import NyStackPanel
        return NyStackPanel.from_path(self.ui_node, self.path, **kwargs)

    def to_edit_box(self, **kwargs):
        """
        | 转换为 ``NyEditBox`` 实例。

        -----

        :return: NyEditBox实例
        :rtype: NyEditBox
        """
        from . import NyEditBox
        return NyEditBox.from_path(self.ui_node, self.path, **kwargs)

    def to_netease_paper_doll(self, **kwargs):
        """
        | 转换为 ``NyPaperDoll`` 实例。

        -----

        :return: NyPaperDoll实例
        :rtype: NyPaperDoll
        """
        from . import NyPaperDoll
        return NyPaperDoll.from_path(self.ui_node, self.path, **kwargs)

    def to_item_renderer(self, **kwargs):
        """
        | 转换为 ``NyItemRenderer`` 实例。

        -----

        :return: NyItemRenderer实例
        :rtype: NyItemRenderer
        """
        from . import NyItemRenderer
        return NyItemRenderer.from_path(self.ui_node, self.path, **kwargs)

    def to_scroll_view(self, **kwargs):
        """
        | 转换为 ``NyScrollView`` 实例。

        -----

        :return: NyScrollView实例
        :rtype: NyScrollView
        """
        from . import NyScrollView
        return NyScrollView.from_path(self.ui_node, self.path, **kwargs)

    def to_grid(self, **kwargs):
        """
        | 转换为 ``NyGrid`` 实例。

        -----

        :param bool is_stack_grid: [仅关键字参数] 是否是StackGrid，默认为False

        :return: NyGrid实例
        :rtype: NyGrid
        """
        from . import NyGrid
        return NyGrid.from_path(self.ui_node, self.path, **kwargs)

    def to_progress_bar(self, **kwargs):
        """
        | 转换为 ``NyProgressBar`` 实例。

        -----

        :return: NyProgressBar实例
        :rtype: NyProgressBar
        """
        from . import NyProgressBar
        return NyProgressBar.from_path(self.ui_node, self.path, **kwargs)

    def to_toggle(self, **kwargs):
        """
        | 转换为 ``NyToggle`` 实例。

        -----

        :return: NyToggle实例
        :rtype: NyToggle
        """
        from . import NyToggle
        return NyToggle.from_path(self.ui_node, self.path, **kwargs)

    def to_slider(self, **kwargs):
        """
        | 转换为 ``NySlider`` 实例。

        -----

        :return: NySlider实例
        :rtype: NySlider
        """
        from . import NySlider
        return NySlider.from_path(self.ui_node, self.path, **kwargs)

    def to_selection_wheel(self, **kwargs):
        """
        | 转换为 ``NySelectionWheel`` 实例。

        -----

        :return: NySelectionWheel实例
        :rtype: NySelectionWheel
        """
        from . import NySelectionWheel
        return NySelectionWheel.from_path(self.ui_node, self.path, **kwargs)

    def to_combo_box(self, **kwargs):
        """
        | 转换为 ``NyComboBox`` 实例。

        -----

        :return: NyComboBox实例
        :rtype: NyComboBox
        """
        from . import NyComboBox
        return NyComboBox.from_path(self.ui_node, self.path, **kwargs)

    def to_mini_map(self, **kwargs):
        """
        | 转换为 ``NyMiniMap`` 实例。

        -----

        :return: NyMiniMap实例
        :rtype: NyMiniMap
        """
        from . import NyMiniMap
        return NyMiniMap.from_path(self.ui_node, self.path, **kwargs)

    # endregion

    # region Properties ================================================================================================

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
        self.base_control.SetPosition(tuple(val))

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
        self.base_control.SetClipOffset(tuple(val))

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
        self.base_control.SetClipsChildren(bool(val))

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
        self.base_control.SetGlobalPosition(tuple(val)) # NOQA

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
        self.base_control.SetMaxSize(tuple(val))

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
        self.base_control.SetMinSize(tuple(val))

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
        self.base_control.SetSize(tuple(val), True)

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
        self.base_control.SetVisible(bool(val))

    @property
    def alpha(self):
        """
        [只写属性]

        | 控件不透明度。

        :rtype: None
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
        self.base_control.SetLayer(int(val))

    @property
    def touch_enable(self):
        """
        [只写属性]

        | 控件是否可点击交互。

        :rtype: None
        """
        raise _error.GetPropertyError("touch_enable")

    @touch_enable.setter
    def touch_enable(self, val):
        """
        [只写属性]

        | 控件是否可点击交互。

        :type val: bool
        """
        self.base_control.SetTouchEnable(bool(val))

    # endregion


def __test__():
    from ..screen_node import ScreenNodeExtension
    from ...._core._client.comp import ScreenNode
    class SN(ScreenNodeExtension, ScreenNode):
        pass
    s = SN("", "")
    c = s.create_ny_control("/control")
    c2 = s.create_ny_control("/control2")
    abc = NyControl.from_path(s, "/abc")
    assert "/abc" in s._nyc_cache
    c = abc / "child"
    assert c.GetPath() == c.path == "/abc/child"
    abc.destroy()
    assert "/abc" not in s._nyc_cache


















