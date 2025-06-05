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


from ..._core import _error, _utils
from . import ui_utils as _ui_utils


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

    _CONTROL_TYPE = _ui_utils.ControlType.base_control

    def __new__(cls, screen_node_ex, control, **kwargs):
        # 实例缓存
        cache = screen_node_ex._ny_control_cache
        key = control.GetPath()
        if key not in cache:
            cache[key] = object.__new__(cls)
        return cache[key]

    def __init__(self, screen_node_ex, control):
        self._screen_node = screen_node_ex._screen_node
        self.screen_node = screen_node_ex
        self.base_control = control

    def __getattr__(self, name):
        # 尝试调用ModSDK方法
        return getattr(self.base_control, name)

    @_utils.args_type_check(str, is_method=True)
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
        return NyControl.from_path(self.screen_node, self.path + other)

    def __destroy__(self):
        self.base_control = None
        self.screen_node = None

    def iter_children(self, level=1):
        """
        [生成器]

        | 返回当前控件指定层级的子控件的 ``NyControl`` 实例。

        -----

        :param int level: 子控件层级，默认为1，传入0或负值将返回所有层级的子控件
        """
        if level <= 0:
            self._screen_node.GetAllChildrenPath(self.path)
        else:
            all_path = _ui_utils.get_all_children_path_by_level(
                self.base_control, self._screen_node, level
            )

    def iter_path(self, level=1):
        """
        [生成器]

        | 返回当前控件指定层级的子控件的路径。

        -----

        :param int level: 子控件层级，默认为1，传入0或负值将返回所有层级的子控件
        """

    @classmethod
    def from_path(cls, screen_node_ex, path, **kwargs):
        """
        | 根据路径创建一个与调用方类型相同的Ny控件实例。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
        :param str path: 控件路径
        :param Any kwargs: 参数

        :return: Ny控件实例
        :rtype: NyControl
        """
        return screen_node_ex._create_nyc(path, cls, **kwargs)

    @classmethod
    def from_control(cls, screen_node_ex, control, **kwargs):
        """
        | 用 ``BaseUIControl`` 实例创建一个与调用方类型相同的Ny控件实例。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例
        :param BaseUIControl control: 控件BaseUIControl实例
        :param Any kwargs: 参数

        :return: Ny控件实例
        :rtype: NyControl
        """
        return screen_node_ex._create_nyc(control.GetPath(), cls, **kwargs)

    @_utils.cache_property
    def path(self):
        """
        [只读]

        | 控件路径。

        :rtype: str
        """
        return self.base_control.GetPath()

    @_utils.cache_property
    def parent_path(self):
        """
        [只读]

        | 父控件路径。

        :rtype: str
        """
        return _ui_utils.get_parent_path(self.path)

    @_utils.cache_property
    def parent_ny_control(self):
        """
        [只读]

        | 父控件 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.from_path(self.screen_node, self.parent_path)

    def remove(self):
        """
        | 销毁控件，将控件从画布上移除。

        -----

        :return: 无
        :rtype: None
        """
        self.__destroy__()
        self._screen_node.RemoveChildControl(self.base_control)

    @property
    def button(self):
        """
        [只读]

        | 转换为 ``ButtonUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: ButtonUIControl
        """
        return self.base_control.asButton()

    @property
    def image(self):
        """
        [只读]

        | 转换为 ``ImageUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: ImageUIControl
        """
        return self.base_control.asImage()

    @property
    def label(self):
        """
        [只读]

        | 转换为 ``LabelUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: LabelUIControl
        """
        return self.base_control.asLabel()

    @property
    def input_panel(self):
        """
        [只读]

        | 转换为 ``InputPanelUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: InputPanelUIControl
        """
        return self.base_control.asInputPanel()

    @property
    def stack_panel(self):
        """
        [只读]

        | 转换为 ``StackPanelUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: StackPanelUIControl
        """
        return self.base_control.asStackPanel()

    @property
    def edit_box(self):
        """
        [只读]

        | 转换为 ``TextEditBoxUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: TextEditBoxUIControl
        """
        return self.base_control.asTextEditBox()

    @property
    def netease_paper_doll(self):
        """
        [只读]

        | 转换为 ``NeteasePaperDollUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: NeteasePaperDollUIControl
        """
        return self.base_control.asNeteasePaperDoll()

    @property
    def item_renderer(self):
        """
        [只读]

        | 转换为 ``ItemRendererUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: ItemRendererUIControl
        """
        return self.base_control.asItemRenderer()

    @property
    def scroll_view(self):
        """
        [只读]

        | 转换为 ``ScrollViewUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: ScrollViewUIControl
        """
        return self.base_control.asScrollView()

    @property
    def grid(self):
        """
        [只读]

        | 转换为 ``GridUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: GridUIControl
        """
        return self.base_control.asGrid()

    @property
    def progress_bar(self):
        """
        [只读]

        | 转换为 ``ProgressBarUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: ProgressBarUIControl
        """
        return self.base_control.asProgressBar()

    @property
    def toggle(self):
        """
        [只读]

        | 转换为 ``SwitchToggleUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: SwitchToggleUIControl
        """
        return self.base_control.asSwitchToggle()

    @property
    def slider(self):
        """
        [只读]

        | 转换为 ``SliderUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: SliderUIControl
        """
        return self.base_control.asSlider()

    @property
    def selection_wheel(self):
        """
        [只读]

        | 转换为 ``SelectionWheelUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: SelectionWheelUIControl
        """
        return self.base_control.asSelectionWheel()

    @property
    def combo_box(self):
        """
        [只读]

        | 转换为 ``NeteaseComboBoxUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: NeteaseComboBoxUIControl
        """
        return self.base_control.asNeteaseComboBox()

    @property
    def mini_map(self):
        """
        [只读]

        | 转换为 ``MiniMapUIControl`` 实例，用于调用该实例的ModSDK接口。

        :rtype: MiniMapUIControl
        """
        return self.base_control.asMiniMap()

    @property
    def position(self):
        """
        [可读写]

        | 按钮相对于父控件的坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetPosition()

    @position.setter
    def position(self, val):
        """
        [可读写]

        | 按钮相对于父控件的坐标。

        :type val: tuple[float,float]
        """
        self.base_control.SetPosition(val)

    @property
    def anchor_from(self):
        """
        [可读写]

        | 父控件锚点位置。

        :rtype: str
        """
        return self.base_control.GetAnchorFrom()

    @anchor_from.setter
    def anchor_from(self, val):
        """
        [可读写]

        | 父控件锚点位置。

        :type val: str
        """
        self.base_control.SetAnchorFrom(val)

    @property
    def anchor_to(self):
        """
        [可读写]

        | 控件自身锚点位置。

        :rtype: str
        """
        return self.base_control.GetAnchorTo()

    @anchor_to.setter
    def anchor_to(self, val):
        """
        [可读写]

        | 控件自身锚点位置。

        :type val: str
        """
        self.base_control.SetAnchorTo(val)

    @property
    def clip_offset(self):
        """
        [可读写]

        | 控件的裁剪偏移。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetClipOffset()

    @clip_offset.setter
    def clip_offset(self, val):
        """
        [可读写]

        | 控件的裁剪偏移。

        :type val: tuple[float,float]
        """
        self.base_control.SetClipOffset(val)

    @property
    def clip_children(self):
        """
        [可读写]

        | 是否开启裁剪内容。

        :rtype: bool
        """
        return self.base_control.GetClipsChildren()

    @clip_children.setter
    def clip_children(self, val):
        """
        [可读写]

        | 是否开启裁剪内容。

        :type val: bool
        """
        self.base_control.SetClipsChildren(val)

    @property
    def full_position_x(self):
        """
        [可读写]

        | 控件的锚点X坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullPosition("x")

    @full_position_x.setter
    def full_position_x(self, val):
        """
        [可读写]

        | 控件的锚点X坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullPosition("x", val)

    @property
    def full_position_y(self):
        """
        [可读写]

        | 控件的锚点Y坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullPosition("y")

    @full_position_y.setter
    def full_position_y(self, val):
        """
        [可读写]

        | 控件的锚点Y坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullPosition("y", val)

    @property
    def full_size_x(self):
        """
        [可读写]

        | 控件的X轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullSize("x")

    @full_size_x.setter
    def full_size_x(self, val):
        """
        [可读写]

        | 控件的X轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullSize("x", val)

    @property
    def full_size_y(self):
        """
        [可读写]

        | 控件的Y轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self.base_control.GetFullSize("y")

    @full_size_y.setter
    def full_size_y(self, val):
        """
        [可读写]

        | 控件的Y轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self.base_control.SetFullSize("y", val)

    @property
    def global_position(self):
        """
        [可读写]

        | 控件全局坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetGlobalPosition()

    @global_position.setter
    def global_position(self, val):
        """
        [可读写]

        | 控件全局坐标。

        :type val: tuple[float,float]
        """
        self.base_control.SetGlobalPosition(val) # NOQA

    @property
    def max_size(self):
        """
        [可读写]

        | 控件所允许的最大尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetMaxSize()

    @max_size.setter
    def max_size(self, val):
        """
        [可读写]

        | 控件所允许的最大尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetMaxSize(val)

    @property
    def min_size(self):
        """
        [可读写]

        | 控件所允许的最小尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetMinSize()

    @min_size.setter
    def min_size(self, val):
        """
        [可读写]

        | 控件所允许的最小尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetMinSize(val)

    @property
    def size(self):
        """
        [可读写]

        | 控件尺寸。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetSize()

    @size.setter
    def size(self, val):
        """
        [可读写]

        | 控件尺寸。

        :type val: tuple[float,float]
        """
        self.base_control.SetSize(val, True)

    @property
    def visible(self):
        """
        [可读写]

        | 控件是否显示。

        :rtype: bool
        """
        return self.base_control.GetVisible()

    @visible.setter
    def visible(self, val):
        """
        [可读写]

        | 控件是否显示。

        :type val: bool
        """
        self.base_control.SetVisible(val)

    @property
    def alpha(self):
        """
        [只写]

        | 控件不透明度。
        """
        raise _error.GetPropertyError("alpha")

    @alpha.setter
    def alpha(self, val):
        """
        [只写]

        | 控件不透明度。

        :type val: float
        """
        self.base_control.SetAlpha(val)

    @property
    def layer(self):
        """
        [可读写]

        | 控件层级。

        :rtype: int
        """
        return self.base_control.GetLayer() # NOQA

    @layer.setter
    def layer(self, val):
        """
        [可读写]

        | 控件层级。

        :type val: int
        """
        self.base_control.SetLayer(val)

    @property
    def touch_enable(self):
        """
        [只写]

        | 控件是否可点击交互。
        """
        raise _error.GetPropertyError("touch_enable")

    @touch_enable.setter
    def touch_enable(self, val):
        """
        [只写]

        | 控件是否可点击交互。

        :type val: bool
        """
        self.base_control.SetTouchEnable(val)

    @property
    def property_bag(self):
        """
        [可读写]

        | 获取PropertyBag。

        :rtype: dict|None
        """
        return self.base_control.GetPropertyBag()

    @property_bag.setter
    def property_bag(self, val):
        """
        [可读写]

        | 设置PropertyBag，将使用字典中的每个值来覆盖原本PropertyBag中的值。

        :type val: dict
        """
        self.base_control.SetPropertyBag(val)




















