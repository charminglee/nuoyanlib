# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


if 0:
    from typing import Any, TypeVar
    from ..screen_node import ScreenNodeExtension
    from . import *


from ....core import error
from ....core._utils import kwargs_defaults, try_exec, cached_property, UNIVERSAL_OBJECT
from ....core._types._checker import args_type_check
from ....client.ui.ui_utils import get_children_path_by_level, get_parent_path, to_path
from ....utils.enum import ControlType


__all__ = [
    "InteractableControl",
    "NyControl",
]


class InteractableControl(object):
    CALLBACK_TYPE = UNIVERSAL_OBJECT

    def __init__(self, callback_func_map):
        if not self.CALLBACK_TYPE:
            raise TypeError("unknown CALLBACK_TYPE")
        self.callbacks = {}
        self._callback_flag = []
        self._callback_func_map = callback_func_map

    def __destroy__(self):
        self.callbacks.clear()
        self._callback_flag = []
        self._callback_func_map.clear()

    def _exec_callbacks(self, cb_type, *args):
        for cb in self.callbacks[cb_type]:
            try_exec(cb, *args)

    def set_callback(self, func, cb_type=None):
        if cb_type not in self.CALLBACK_TYPE:
            raise ValueError(
                "invalid callback type: %s, please use enum value of '%s'"
                % (repr(cb_type), self.CALLBACK_TYPE.__name__)
            )

        callback_lst = self.callbacks.setdefault(cb_type, [])
        if func in callback_lst:
            return False
        callback_lst.append(func)

        if cb_type not in self._callback_flag:
            if cb_type in self._callback_func_map:
                api, callback = self._callback_func_map[cb_type]
                api(callback)
            self._callback_flag.append(cb_type)
        return True

    def remove_callback(self, func, cb_type=None):
        if cb_type not in self.CALLBACK_TYPE:
            raise ValueError(
                "invalid callback type: %s, please use enum value of '%s'"
                % (repr(cb_type), self.CALLBACK_TYPE.__name__)
            )

        callback_lst = self.callbacks.get(cb_type)
        if not callback_lst or func not in callback_lst:
            return False
        callback_lst.remove(func)
        return True


class NyControl(object):
    """
    通用UI控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例（需继承ScreenNodeExtension）
    :param BaseUIControl control: 通过GetBaseUIControl()等方式获取的BaseUIControl实例

    :raise TypeError: 控件所在的UI类必须继承ScreenNodeExtension，否则抛出该异常
    """

    CONTROL_TYPE = ControlType.BASE_CONTROL
    _ALLOWED_APPLY_ATTRS = (
        'position',
        'anchor_from',
        'anchor_to',
        'clip_offset',
        'clip_children',
        'full_position_x',
        'full_position_y',
        'full_size_x',
        'full_size_y',
        'global_position',
        'max_size',
        'min_size',
        'size',
        'visible',
        'alpha',
        'layer',
        'touch_enable',
        'property_bag',
    )

    def __init__(self, screen_node_ex, control, **kwargs):
        from ..screen_node import ScreenNodeExtension
        if not isinstance(screen_node_ex, ScreenNodeExtension):
            raise TypeError(
                "UI class '%s' must inherit 'ScreenNodeExtension'"
                % screen_node_ex.__class__.__name__
            )
        self._screen_node = screen_node_ex._screen_node
        self.ui_node = screen_node_ex
        self._base_control = control
        self._kwargs = kwargs

    def __getattr__(self, name):
        # 尝试调用ModSDK方法
        return getattr(self._base_control, name)

    def __destroy__(self):
        self._screen_node = None
        self._base_control = None
        self.ui_node = None

    def __repr__(self):
        return "<%s object at '%s'>" % (self.__class__.__name__, self._base_control.FullPath())

    # region Properties ================================================================================================

    @cached_property
    def name(self):
        """
        [只读属性]

        控件名称。

        :rtype: str
        """
        return self.path.split("/")[-1]

    @cached_property
    def path(self):
        """
        [只读属性]

        控件路径。

        :rtype: str
        """
        return self._base_control.GetPath()

    @cached_property
    def parent_path(self):
        """
        [只读属性]

        父控件路径，没有父控件时返回None，若父控件为根画布（main），返回空字符串。

        :rtype: str
        """
        return get_parent_path(self.path)

    @cached_property
    def parent(self):
        """
        [只读属性]

        父控件 ``NyControl`` 实例。

        :rtype: NyControl
        """
        return NyControl.from_path(self.ui_node, self.parent_path)
    @property
    def position(self):
        """
        [可读写属性]

        按钮相对于父控件的坐标。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetPosition()

    @position.setter
    def position(self, val):
        """
        [可读写属性]

        按钮相对于父控件的坐标。

        :type val: tuple[float,float]
        """
        self._base_control.SetPosition(tuple(val))

    @property
    def anchor_from(self):
        """
        [可读写属性]

        父控件锚点位置。

        :rtype: str
        """
        return self._base_control.GetAnchorFrom()

    @anchor_from.setter
    def anchor_from(self, val):
        """
        [可读写属性]

        父控件锚点位置。

        :type val: str
        """
        self._base_control.SetAnchorFrom(val)

    @property
    def anchor_to(self):
        """
        [可读写属性]

        控件自身锚点位置。

        :rtype: str
        """
        return self._base_control.GetAnchorTo()

    @anchor_to.setter
    def anchor_to(self, val):
        """
        [可读写属性]

        控件自身锚点位置。

        :type val: str
        """
        self._base_control.SetAnchorTo(val)

    @property
    def clip_offset(self):
        """
        [可读写属性]

        控件的裁剪偏移。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetClipOffset()

    @clip_offset.setter
    def clip_offset(self, val):
        """
        [可读写属性]

        控件的裁剪偏移。

        :type val: tuple[float,float]
        """
        self._base_control.SetClipOffset(tuple(val))

    @property
    def clip_children(self):
        """
        [可读写属性]

        是否开启裁剪内容。

        :rtype: bool
        """
        return self._base_control.GetClipsChildren()

    @clip_children.setter
    def clip_children(self, val):
        """
        [可读写属性]

        是否开启裁剪内容。

        :type val: bool
        """
        self._base_control.SetClipsChildren(bool(val))

    @property
    def full_position_x(self):
        """
        [可读写属性]

        控件的锚点X坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self._base_control.GetFullPosition("x")

    @full_position_x.setter
    def full_position_x(self, val):
        """
        [可读写属性]

        控件的锚点X坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self._base_control.SetFullPosition("x", val)

    @property
    def full_position_y(self):
        """
        [可读写属性]

        控件的锚点Y坐标，支持百分比以及绝对值。

        :rtype: dict
        """
        return self._base_control.GetFullPosition("y")

    @full_position_y.setter
    def full_position_y(self, val):
        """
        [可读写属性]

        控件的锚点Y坐标，支持百分比以及绝对值。

        :type val: dict
        """
        self._base_control.SetFullPosition("y", val)

    @property
    def full_size_x(self):
        """
        [可读写属性]

        控件的X轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self._base_control.GetFullSize("x")

    @full_size_x.setter
    def full_size_x(self, val):
        """
        [可读写属性]

        控件的X轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self._base_control.SetFullSize("x", val)

    @property
    def full_size_y(self):
        """
        [可读写属性]

        控件的Y轴大小，支持百分比以及绝对值。

        :rtype: dict
        """
        return self._base_control.GetFullSize("y")

    @full_size_y.setter
    def full_size_y(self, val):
        """
        [可读写属性]

        控件的Y轴大小，支持百分比以及绝对值。

        :type val: dict
        """
        self._base_control.SetFullSize("y", val)

    @property
    def global_position(self):
        """
        [可读写属性]

        控件全局坐标。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetGlobalPosition()

    @global_position.setter
    def global_position(self, val):
        """
        [可读写属性]

        控件全局坐标。

        :type val: tuple[float,float]
        """
        self._base_control.SetGlobalPosition(tuple(val)) # noqa

    @property
    def max_size(self):
        """
        [可读写属性]

        控件所允许的最大尺寸。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetMaxSize()

    @max_size.setter
    def max_size(self, val):
        """
        [可读写属性]

        控件所允许的最大尺寸。

        :type val: tuple[float,float]
        """
        self._base_control.SetMaxSize(tuple(val))

    @property
    def min_size(self):
        """
        [可读写属性]

        控件所允许的最小尺寸。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetMinSize()

    @min_size.setter
    def min_size(self, val):
        """
        [可读写属性]

        控件所允许的最小尺寸。

        :type val: tuple[float,float]
        """
        self._base_control.SetMinSize(tuple(val))

    @property
    def size(self):
        """
        [可读写属性]

        控件尺寸。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetSize()

    @size.setter
    def size(self, val):
        """
        [可读写属性]

        控件尺寸。

        :type val: tuple[float,float]
        """
        self._base_control.SetSize(tuple(val), True)

    @property
    def visible(self):
        """
        [可读写属性]

        控件是否显示。

        :rtype: bool
        """
        return self._base_control.GetVisible()

    @visible.setter
    def visible(self, val):
        """
        [可读写属性]

        控件是否显示。

        :type val: bool
        """
        self._base_control.SetVisible(bool(val))

    @property
    def alpha(self):
        """
        [只写属性]

        控件不透明度。

        :rtype: None
        """
        raise error.GetPropertyError("alpha")

    @alpha.setter
    def alpha(self, val):
        """
        [只写属性]

        控件不透明度。

        :type val: float
        """
        self._base_control.SetAlpha(val)

    @property
    def layer(self):
        """
        [可读写属性]

        控件渲染层级。

        :rtype: int
        """
        return self._base_control.GetLayer()

    @layer.setter
    def layer(self, val):
        """
        [可读写属性]

        控件渲染层级。

        :type val: int
        """
        self._base_control.SetLayer(int(val))

    @property
    def touch_enable(self):
        """
        [只写属性]

        控件是否可点击交互。

        :rtype: None
        """
        raise error.GetPropertyError("touch_enable")

    @touch_enable.setter
    def touch_enable(self, val):
        """
        [只写属性]

        控件是否可点击交互。

        :type val: bool
        """
        self._base_control.SetTouchEnable(bool(val))

    @property
    def property_bag(self):
        """
        [可读写属性]

        获取PropertyBag。

        :rtype: dict|None
        """
        return self._base_control.GetPropertyBag()

    @property_bag.setter
    def property_bag(self, val):
        """
        [可读写属性]

        设置PropertyBag，将使用字典中的每个值来覆盖原本PropertyBag中的值。

        :type val: dict
        """
        self._base_control.SetPropertyBag(val)

    # endregion

    # region Common ====================================================================================================

    @args_type_check(str, is_method=True)
    def __truediv__(self, other):
        """
        根据相对路径返回子控件的 ``NyControl`` 实例。

        -----

        :param str other: 相对路径

        :return: 子控件的NyControl实例
        :rtype: NyControl
        """
        if not other.startswith("/"):
            other = "/" + other
        return NyControl.from_path(self.ui_node, self.path + other)

    __div__ = __truediv__

    def apply_attr(self, attr, value, level=1):
        """
        批量设置指定层次的所有子控件的属性。

        -----

        :param str attr: 需要设置的属性名
        :param Any value: 需要设置的值
        :param int level: 子控件所在层次，默认为1，传入0或负值表示所有层次

        :return: 无
        :rtype: None
        """
        if attr not in NyControl._ALLOWED_APPLY_ATTRS:
            raise AttributeError("can't apply to attribute '%s'" % attr)
        for c in self.children(level):
            setattr(c, attr, value)

    def add_child(self, def_name, child_name, force_update=True):
        """
        为当前控件创建一个新的子控件。

        -----

        :param str def_name: 控件定义名称，格式为"<namespace>.<control_name>"；<namespace>对应UI json文件中"namespace"对应的值，UI编辑器生成的UI json文件该值等于文件名；<control_name>对应想创建的控件的名称，该控件需要置于UI json文件顶层（即与main画布同级，不能是任何一个控件的子控件），或在UI编辑器中将该控件添加至自定义控件库
        :param str child_name: 控件名称
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量新建子控件操作且在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 新控件的NyControl实例；若当前控件已存在同名子控件，则返回其NyControl实例；创建失败时返回None
        :rtype: NyControl|None
        """
        path = self.path + "/" + child_name
        if self.ui_node._is_control_exist(path):
            return NyControl.from_path(self.ui_node, path)
        control = self._screen_node.CreateChildControl(def_name, child_name, self._base_control, force_update)
        if control:
            return NyControl.from_control(self.ui_node, control)

    def clone_to(self, parent, name="", sync_refresh=True, force_update=True):
        """
        将当前控件克隆到指定父控件下。

        -----

        :param str|BaseUIControl|NyControl parent: 父控件路径或实例
        :param str name: 新控件的名称，默认为当前控件的名称
        :param bool sync_refresh: 是否需要同步刷新，默认为True；设为True时游戏在同一帧计算该控件的size等相关数据，设为False则在下一帧进行计算；如同一帧有大量clone操作建议设为False，操作结束后调用一次UpdateScreen接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则按照sync_refresh逻辑进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量clone操作且非在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 新控件的Ny控件实例，类型与当前控件相同；若父控件已存在同名子控件，则返回其NyControl实例；克隆失败时返回None
        :rtype: NyControl|None
        """
        parent_path = to_path(parent)
        if not name:
            name = self.name
        new_path = parent_path + "/" + name
        if self.ui_node._is_control_exist(new_path):
            return NyControl.from_path(self.ui_node, new_path)
        if self._screen_node.Clone(self.path, parent_path, name, sync_refresh, force_update):
            return self.__class__.from_path(self.ui_node, new_path, **self._kwargs)

    def clone_from(self, control, name="", sync_refresh=True, force_update=True):
        """
        将指定控件克隆到当前控件下（当前控件作为父控件）。

        -----

        :param str|BaseUIControl|NyControl control: 被克隆控件的路径或实例
        :param str name: 新控件的名称，默认为被克隆控件的名称
        :param bool sync_refresh: 是否需要同步刷新，默认为True；设为True时游戏在同一帧计算该控件的size等相关数据，设为False则在下一帧进行计算；如同一帧有大量clone操作建议设为False，操作结束后调用一次UpdateScreen接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新，默认为True；设为True则按照sync_refresh逻辑进行同一帧或者下一帧刷新，设为False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新；如有大量clone操作且非在同一帧执行，建议设为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 新控件的NyControl实例；若当前控件已存在同名子控件，则返回其NyControl实例；克隆失败时返回None
        :rtype: NyControl|None
        """
        control_path = to_path(control)
        if not name:
            name = control_path.split("/")[-1]
        new_path = self.path + "/" + name
        if self.ui_node._is_control_exist(new_path):
            return NyControl.from_path(self.ui_node, new_path)
        if self._screen_node.Clone(control_path, self.path, name, sync_refresh, force_update):
            return NyControl.from_path(self.ui_node, new_path)

    def children(self, level=1):
        """
        获取指定层次上的所有子控件。

        -----

        :param int level: 子控件层次，默认为1，传入0或负值表示所有层次

        :return: 指定层次所有子控件的NyControl列表
        :rtype: list[NyControl]
        """
        return [
            NyControl.from_path(self.ui_node, p)
            for p in self.children_path(level)
        ]

    def children_path(self, level=1):
        """
        获取指定层次上的所有子控件的路径。

        -----

        :param int level: 子控件层次，默认为1，传入0或负值表示所有层次

        :return: 指定层次所有子控件的路径列表
        :rtype: list[str]
        """
        return get_children_path_by_level(self._base_control, self._screen_node, level)

    @classmethod
    def from_path(cls, screen_node_ex, path, **kwargs):
        """
        [类方法]

        根据控件路径创建Ny控件实例，类型与当前类相同。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例（需继承ScreenNodeExtension）
        :param str path: 控件路径

        :return: Ny控件实例
        :rtype: NyControl|None
        """
        return screen_node_ex._create_nyc(path, cls, **kwargs)

    @classmethod
    def from_control(cls, screen_node_ex, control, **kwargs):
        """
        [类方法]

        根据 ``BaseUIControl`` 实例创建Ny控件实例，类型与当前类相同。

        -----

        :param ScreenNodeExtension screen_node_ex: 控件所在UI类的实例（需继承ScreenNodeExtension）
        :param BaseUIControl control: BaseUIControl实例

        :return: Ny控件实例
        :rtype: NyControl|None
        """
        if control:
            return screen_node_ex._create_nyc(control.GetPath(), cls, **kwargs)

    def destroy(self):
        """
        销毁控件。

        -----

        :return: 是否成功
        :rtype: bool
        """
        return self.ui_node._destroy_nyc(self)

    ApplyAttr = apply_attr
    AddChild = add_child
    CloneTo = clone_to
    CloneFrom = clone_from
    Children = children
    ChildrenPath = children_path
    FromPath = from_path
    FromControl = from_control
    Destroy = destroy

    # endregion

    # region Conversion ================================================================================================

    @kwargs_defaults(touch_event_params=None)
    def to_button(self, **kwargs):
        """
        转换为 ``NyButton`` 实例。

        -----

        :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton实例
        :rtype: NyButton|None
        """
        from . import NyButton
        if isinstance(self, NyButton):
            return self
        return NyButton.from_path(self.ui_node, self.path, **kwargs)

    def to_image(self, **kwargs):
        """
        转换为 ``NyImage`` 实例。

        -----

        :return: NyImage实例
        :rtype: NyImage|None
        """
        from . import NyImage
        if isinstance(self, NyImage):
            return self
        return NyImage.from_path(self.ui_node, self.path, **kwargs)

    def to_label(self, **kwargs):
        """
        转换为 ``NyLabel`` 实例。

        -----

        :return: NyLabel实例
        :rtype: NyLabel|None
        """
        from . import NyLabel
        if isinstance(self, NyLabel):
            return self
        return NyLabel.from_path(self.ui_node, self.path, **kwargs)

    def to_input_panel(self, **kwargs):
        """
        转换为 ``NyInputPanel`` 实例。

        -----

        :return: NyInputPanel实例
        :rtype: NyInputPanel|None
        """
        from . import NyInputPanel
        if isinstance(self, NyInputPanel):
            return self
        return NyInputPanel.from_path(self.ui_node, self.path, **kwargs)

    def to_stack_panel(self, **kwargs):
        """
        转换为 ``NyStackPanel`` 实例。

        -----

        :return: NyStackPanel实例
        :rtype: NyStackPanel|None
        """
        from . import NyStackPanel
        if isinstance(self, NyStackPanel):
            return self
        return NyStackPanel.from_path(self.ui_node, self.path, **kwargs)

    def to_edit_box(self, **kwargs):
        """
        转换为 ``NyEditBox`` 实例。

        -----

        :return: NyEditBox实例
        :rtype: NyEditBox|None
        """
        from . import NyEditBox
        if isinstance(self, NyEditBox):
            return self
        return NyEditBox.from_path(self.ui_node, self.path, **kwargs)

    def to_paper_doll(self, **kwargs):
        """
        转换为 ``NyPaperDoll`` 实例。

        -----

        :return: NyPaperDoll实例
        :rtype: NyPaperDoll|None
        """
        from . import NyPaperDoll
        if isinstance(self, NyPaperDoll):
            return self
        return NyPaperDoll.from_path(self.ui_node, self.path, **kwargs)

    def to_item_renderer(self, **kwargs):
        """
        转换为 ``NyItemRenderer`` 实例。

        -----

        :return: NyItemRenderer实例
        :rtype: NyItemRenderer|None
        """
        from . import NyItemRenderer
        if isinstance(self, NyItemRenderer):
            return self
        return NyItemRenderer.from_path(self.ui_node, self.path, **kwargs)

    def to_scroll_view(self, **kwargs):
        """
        转换为 ``NyScrollView`` 实例。

        -----

        :return: NyScrollView实例
        :rtype: NyScrollView|None
        """
        from . import NyScrollView
        if isinstance(self, NyScrollView):
            return self
        return NyScrollView.from_path(self.ui_node, self.path, **kwargs)

    def to_grid(self, **kwargs):
        """
        转换为 ``NyGrid`` 实例。

        -----

        关于 ``cell_visible_binding`` 与 ``collection_name`` 参数的说明：

        - 该参数用于 ``.grid_size`` 、 ``.dimension`` 等接口，实现动态设置网格元素的数量（多余元素将通过设置 ``visible`` 为 ``False`` 的方式隐藏），不使用该接口可忽略这两个参数。
        - 由于网格控件的特性，设置元素的 ``visible`` 需要使用绑定，请在你的 **网格模板控件** 的json中添加以下绑定，然后将 ``"binding_name"`` 的值设置给 ``cell_visible_binding`` 参数 。
        ::

            "bindings": [
                {
                    "binding_type": "collection",
                    "binding_collection_name": "grid_collection_name", //此处需要与网格的"collection_name"字段相同
                    "binding_name": "#namespace.binding_name", //可自定义
                    "binding_name_override": "#visible",
                    "binding_condition": "always"
                }
            ]
        - 最后，将 **网格** json中的 ``"collection_name"`` 字段的值设置给 ``collection_name`` 参数即可。

        -----

        :param bool is_stack_grid: [仅关键字参数] 是否是StackGrid，默认为False
        :param str template_name: [仅关键字参数] 网格模板控件名称，即"grid_item_template"字段或UI编辑器中的网格“内容”所使用的控件；仅模板控件名称以数字结尾时需要传入该参数
        :param str cell_visible_binding: [仅关键字参数] 用于控制网格元素显隐性的绑定名称，详见上方说明
        :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明

        :return: NyGrid实例
        :rtype: NyGrid|None
        """
        from . import NyGrid
        if isinstance(self, NyGrid):
            return self
        return NyGrid.from_path(self.ui_node, self.path, **kwargs)

    def to_progress_bar(self, **kwargs):
        """
        转换为 ``NyProgressBar`` 实例。

        -----

        :return: NyProgressBar实例
        :rtype: NyProgressBar|None
        """
        from . import NyProgressBar
        if isinstance(self, NyProgressBar):
            return self
        return NyProgressBar.from_path(self.ui_node, self.path, **kwargs)

    def to_toggle(self, **kwargs):
        """
        转换为 ``NyToggle`` 实例。

        -----

        :return: NyToggle实例
        :rtype: NyToggle|None
        """
        from . import NyToggle
        if isinstance(self, NyToggle):
            return self
        return NyToggle.from_path(self.ui_node, self.path, **kwargs)

    def to_slider(self, **kwargs):
        """
        转换为 ``NySlider`` 实例。

        -----

        :return: NySlider实例
        :rtype: NySlider|None
        """
        from . import NySlider
        if isinstance(self, NySlider):
            return self
        return NySlider.from_path(self.ui_node, self.path, **kwargs)

    def to_selection_wheel(self, **kwargs):
        """
        转换为 ``NySelectionWheel`` 实例。

        -----

        :return: NySelectionWheel实例
        :rtype: NySelectionWheel|None
        """
        from . import NySelectionWheel
        if isinstance(self, NySelectionWheel):
            return self
        return NySelectionWheel.from_path(self.ui_node, self.path, **kwargs)

    def to_combo_box(self, **kwargs):
        """
        转换为 ``NyComboBox`` 实例。

        -----

        :return: NyComboBox实例
        :rtype: NyComboBox|None
        """
        from . import NyComboBox
        if isinstance(self, NyComboBox):
            return self
        return NyComboBox.from_path(self.ui_node, self.path, **kwargs)

    def to_mini_map(self, **kwargs):
        """
        转换为 ``NyMiniMap`` 实例。

        -----

        :return: NyMiniMap实例
        :rtype: NyMiniMap|None
        """
        from . import NyMiniMap
        if isinstance(self, NyMiniMap):
            return self
        return NyMiniMap.from_path(self.ui_node, self.path, **kwargs)

    ToButton = to_button
    ToImage = to_image
    ToLabel = to_label
    ToInputPanel = to_input_panel
    ToStackPanel = to_stack_panel
    ToEditBox = to_edit_box
    ToPaperDoll = to_paper_doll
    ToItemRenderer = to_item_renderer
    ToScrollView = to_scroll_view
    ToGrid = to_grid
    ToProgressBar = to_progress_bar
    ToToggle = to_toggle
    ToSlider = to_slider
    ToSelectionWheel = to_selection_wheel
    ToComboBox = to_combo_box
    ToMiniMap = to_mini_map

    # endregion


def __test__():
    from ..screen_node import ScreenNodeExtension
    from ....core.client.comp import ScreenNode
    class SN(ScreenNodeExtension, ScreenNode):
        pass
    s = SN("", "")
    c = s.create_ny_control("/control")
    c2 = s.create_ny_control("/control2")
    abc = NyControl.from_path(s, "/abc")
    assert "/abc" in s._nyc_cache_map
    ch = abc / "child"
    assert ch.GetPath() == ch.path == "/abc/child"
    abc.destroy()
    assert "/abc" not in s._nyc_cache_map


















