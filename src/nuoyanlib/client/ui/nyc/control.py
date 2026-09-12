# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


if bool(0):
    from typing import Any
    from ..screen_node import NyScreenNode, NyScreenProxy
    from . import *


from ....core import error
from ....core._utils import kwargs_defaults, try_exec, cached_property
from ....core._types._checker import args_type_check
from ..ui_utils import get_children_path_by_level, get_parent_path, is_out_of_screen, _UIControlType


__all__ = [
    "InteractableControl",
    "NyControl",
]


_CONVERSION_FUNC_MAP = {
    _UIControlType.BUTTON               : "asButton",
    _UIControlType.COMBO_BOX            : "asNeteaseComboBox",
    _UIControlType.EDIT_BOX             : "asTextEditBox",
    _UIControlType.GRID                 : "asGrid",
    _UIControlType.IMAGE                : "asImage",
    _UIControlType.INPUT_PANEL          : "asInputPanel",
    _UIControlType.ITEM_RENDERER        : "asItemRenderer",
    _UIControlType.LABEL                : "asLabel",
    _UIControlType.MINI_MAP             : "asMiniMap",
    _UIControlType.NETEASE_PAPER_DOLL   : "asNeteasePaperDoll",
    _UIControlType.PROGRESS_BAR         : "asProgressBar",
    _UIControlType.SCROLL_VIEW          : "asScrollView",
    _UIControlType.SELECTION_WHEEL      : "asSelectionWheel",
    _UIControlType.SLIDER               : "asSlider",
    _UIControlType.STACK_PANEL          : "asStackPanel",
    _UIControlType.TOGGLE               : "asSwitchToggle",
}


class InteractableControl(object):
    def __init__(self, callback_setters):
        self._callbacks = {}
        self._callback_setters = callback_setters

    def __ui_destroy__(self):
        self._callbacks = None
        self._callback_setters = None

    def exec_callbacks(self, cb_type, *args):
        for cb in self._callbacks[cb_type]:
            try_exec(cb, *args)

    def set_callback(self, func, *cb_types):
        for t in cb_types:
            if t not in self._callback_setters:
                raise ValueError("invalid callback type: %s" % t)

            if t not in self._callbacks:
                self._callbacks[t] = []
                setter = self._callback_setters[t]
                if isinstance(setter, tuple):
                    setter[0](*setter[1:])
                else:
                    setter()

            callbacks = self._callbacks[t]
            if func not in callbacks:
                callbacks.append(func)

    def remove_callback(self, func, *cb_types):
        for t in cb_types:
            if t not in self._callback_setters:
                raise ValueError("invalid callback type: %s" % t)
            callbacks = self._callbacks.get(t)
            if callbacks and func in callbacks:
                callbacks.remove(func)


class NyControlMeta(type):
    def __call__(cls, ny_screen_node, path, **kwargs): # noqa
        # NyControl 缓存机制
        cached_nyc = ny_screen_node._nyc_cache_map.get(path)
        if cached_nyc:
            cached_t = type(cached_nyc)
            if cached_t is cls or cached_t is not NyControl:
                return cached_nyc
        inst = type.__call__(cls, ny_screen_node, path, **kwargs)
        ny_screen_node._nyc_cache_map[path] = inst
        return inst


class NyControl(object):
    """
    通用UI控件类。

    说明
    ----

    同一路径重复获取会得到同一个 ``NyControl`` 实例。

    通过 ``NyControl⠀/⠀"child"`` 的方式可以便捷获取子控件实例。

    ``NyControl`` 兼容所有 ModSDK 原生UI控件接口，如 ``NyControl.SetVisible(False)`` ，但建议优先使用 ``NyControl`` 提供的属性和方法。

    示例
    ----

    获取 ``NyControl`` 实例：

    >>> self.panel = nyl.NyControl(self, "/panel")

    获取 ``panel`` 的子控件 ``button`` ， 并转换为 ``NyButton`` 实例：

    >>> self.button = (self.panel / "button").to_button()

    支持多级子控件路径：

    >>> self.button_label = self.panel / "button/button_label"

    获取/设置控件属性：

    >>> if self.button.visible:
    ...     self.button.visible = False

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径

    :raise TypeError: 传入的 ny_screen_node 没有继承 NyScreenNode 或 NyScreenProxy 时抛出
    :raise ControlNotFoundError: 找不到指定路径的控件时抛出
    """

    __metaclass__ = NyControlMeta

    CONTROL_TYPE = _UIControlType.ALL
    ALLOWED_APPLY_ATTRS = (
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

    def __init__(self, ny_screen_node, path, **kwargs):
        from ..screen_node import NyScreenBase
        if not isinstance(ny_screen_node, NyScreenBase):
            raise TypeError(
                "UI screen class %s must inherit NyScreenNode or NyScreenProxy"
                % ny_screen_node.__class__.__name__
            )

        screen_node = ny_screen_node._screen_node
        self._screen_node = screen_node
        self.ny_screen_node = ny_screen_node

        base_control = screen_node.GetBaseUIControl(path)
        if not base_control:
            raise error.ControlNotFoundError(path)
        if self.CONTROL_TYPE != _UIControlType.ALL:
            self._base_control = self._try_convert(base_control)
        else:
            self._base_control = base_control

        self._kwargs = kwargs
        if self.path not in self.ny_screen_node._ui_default_pos_data:
            self.ny_screen_node._set_ui_default_pos_data(self.path, self.position)

    def __getattr__(self, name):
        # 尝试调用ModSDK原生方法
        return getattr(self._base_control, name)

    def __ui_destroy__(self):
        self._screen_node = None
        self._base_control = None
        self.ny_screen_node = None
        self._kwargs = None

    def __repr__(self):
        full_path = self.full_path
        path_parts = full_path.strip("/").split("/")
        if len(path_parts) > 4:
            full_path = "/{0[0]}/{0[1]}/{0[2]}/.../{1}".format(path_parts, path_parts[-1])
        return "<%s '%s' at '%s'>" % (self.__class__.__name__, self.name, full_path)

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
    def full_path(self):
        """
        [只读属性]

        控件完整路径，包含画布名称。

        :rtype: str
        """
        return self._base_control.FullPath()

    @cached_property
    def parent_path(self):
        """
        [只读属性]

        父控件路径，没有父控件时返回 None，若父控件为根画布（main），返回空字符串。

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
        return NyControl(self.ny_screen_node, self.parent_path)

    @property
    def position(self):
        """
        [可读写属性]

        控件相对于父控件的坐标。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetPosition()

    @position.setter
    def position(self, val):
        """
        [可读写属性]

        控件相对于父控件的坐标。

        :type val: tuple[float,float]
        """
        self._base_control.SetPosition(val)

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
        self._base_control.SetClipOffset(val)

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
        self._base_control.SetClipsChildren(val)

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
        self._base_control.SetGlobalPosition(val) # noqa

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
        self._base_control.SetMaxSize(val)

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
        self._base_control.SetMinSize(val)

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
        self._base_control.SetSize(val, True)

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
        self._base_control.SetVisible(val)

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
        self._base_control.SetLayer(val)

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
        self._base_control.SetTouchEnable(val)

    @property
    def property_bag(self):
        """
        [可读写属性]

        获取 PropertyBag。

        :rtype: dict|None
        """
        return self._base_control.GetPropertyBag()

    @property_bag.setter
    def property_bag(self, val):
        """
        [可读写属性]

        设置 PropertyBag，将使用字典中的每个值来覆盖原本 PropertyBag 中的值。

        :type val: dict
        """
        self._base_control.SetPropertyBag(val)

    # endregion

    # region Common ====================================================================================================

    def clear_pos_data(self):
        """
        删除控件位置数据。

        删除后下次创建UI时将不会恢复位置。

        示例
        ----

        >>> self.panel.clear_pos_data()
        True

        参见
        ----

        - ``NyControl.save_pos()`` -- 保存控件当前位置。

        -----

        :return: 是否成功
        :rtype: bool
        """
        self.ny_screen_node._set_ui_pos_data(self.path, None)
        return True

    def save_pos(self):
        """
        保存控件位置数据。

        保存后下次创建UI时将自动恢复位置。

        说明
        ----

        为保证安全，当控件超出屏幕边界时，将取消保存并返回 ``False`` 。

        示例
        ----

        >>> self.panel.save_pos()
        True

        参见
        ----

        - ``NyControl.clear_pos_data()`` -- 删除控件位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if is_out_of_screen(self):
            return False
        pos = self.position
        if pos:
            self.ny_screen_node._set_ui_pos_data(self.path, pos)
            return True
        else:
            return False

    def reset_pos(self):
        """
        将控件恢复到默认位置。

        说明
        ----

        默认位置指的是 UI json 中保存的原始位置。

        示例
        ----

        >>> self.panel.reset_pos()
        True

        参见
        ----

        - ``NyControl.save_pos()`` -- 保存控件当前位置。
        - ``NyControl.clear_pos_data()`` -- 删除控件位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if self.path in self.ny_screen_node._ui_default_pos_data:
            pos = self.ny_screen_node._ui_default_pos_data[self.path]
            self.position = pos
            self.ny_screen_node._set_ui_pos_data(self.path, pos)
            return True
        return False

    @classmethod
    def auto(cls, ny_screen_node, path):
        """
        [类方法]

        自动根据控件类型创建对应的控件实例。

        示例
        ----

        >>> self.button = nyl.NyControl.auto(self, "/panel/button") # 返回NyButton实例
        >>> def on_button_up(args):
        ...     pass
        >>> self.button.set_callback(on_button_up, nyl.NyButton.UP)

        -----

        :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该控件的 NyScreenNode 或 NyScreenProxy 实例
        :param str path: 控件路径

        :return: 控件实例
        :rtype: NyControl

        :raise TypeError: 传入的 ny_screen_node 没有继承 NyScreenNode 或 NyScreenProxy 时抛出
        :raise ControlNotFoundError: 找不到指定路径的控件时抛出
        """
        if cls is not NyControl:
            return cls(ny_screen_node, path)
        # todo

    @args_type_check(str)
    def __truediv__(self, other):
        """
        根据相对路径返回子控件的 ``NyControl`` 实例。

        示例
        ----

        >>> self.button = (self.root_panel / "panel/button").to_button()

        参见
        ----

        - ``NyControl.get_child()`` -- 获取子控件。
        - ``NyControl.children()`` -- 获取指定层次上的所有子控件。
        - ``NyControl.children_path()`` -- 获取指定层次上的所有子控件的路径。

        -----

        :param str other: 相对路径

        :return: 子控件的 NyControl 实例
        :rtype: NyControl
        """
        if not other.startswith("/"):
            other = "/" + other
        return NyControl(self.ny_screen_node, self.path + other)

    __div__ = __truediv__

    def apply_attr(self, attr, value, level=1):
        """
        批量设置指定层次的所有子控件的属性。

        示例
        ----

        隐藏 ``panel`` 的所有子控件：

        >>> self.panel.apply_attr("visible", False)

        -----

        :param str attr: 需要设置的属性名
        :param Any value: 需要设置的值
        :param int level: 子控件所在层次；默认为 1，传入 0 或负值表示所有层次

        :return: 无
        :rtype: None

        :raise AttributeError: attr 不是允许批量设置的属性时抛出
        """
        if attr not in NyControl.ALLOWED_APPLY_ATTRS:
            raise AttributeError("can't apply to attribute '%s'" % attr)
        for c in self.children(level):
            setattr(c, attr, value)

    def has_child(self, path):
        """
        判断子控件是否存在。

        示例
        ----

        >>> if self.panel.has_child("button"):
        ...     self.button = self.panel / "button"

        参见
        ----

        - ``NyControl.get_child()`` -- 获取子控件。
        - ``NyControl.add_child()`` -- 添加新的子控件。

        -----

        :param str path: 相对路径

        :return: 是否存在
        :rtype: bool
        """
        if not path.startswith("/"):
            path = "/" + path
        return self.ny_screen_node.is_control_exist(self.path + path)

    def get_child(self, path):
        """
        获取子控件的 ``NyControl`` 实例。

        示例
        ----

        >>> self.button = self.panel.get_child("button")
        >>> if button:
        ...     button.visible = True

        参见
        ----

        - ``NyControl.has_child()`` -- 判断子控件是否存在。
        - ``NyControl.__div__()`` -- 使用除法运算符获取子控件。

        -----

        :param str path: 相对路径

        :return: 子控件的 ``NyControl`` 实例，不存在时返回 None
        :rtype: NyControl|None
        """
        if not path.startswith("/"):
            path = "/" + path
        child_path = self.path + path
        if self.ny_screen_node.is_control_exist(child_path):
            return NyControl(self.ny_screen_node, child_path)

    def add_child(self, def_name, child_name, force_update=True):
        """
        为当前控件创建一个新的子控件。

        示例
        ----

        >>> self.buttons = []
        >>> for i in range(10):
        ...     button = self.panel.add_child(
        ...         "my_screen.button_template",
        ...         "button%d" % i,
        ...         force_update=False
        ...     )
        ...     button = button
        ...     self.buttons.append(button)
        >>> self.update_screen()

        参见
        ----

        - ``NyControl.get_child()`` -- 获取子控件。
        - ``NyControl.clone_from()`` -- 将指定控件克隆到当前控件下。

        -----

        :param str def_name: 子控件定义名称，格式为 "<namespace>.<control_name>" ； <namespace> 对应 UI json 文件中 "namespace" 字段的值，UI编辑器生成的 UI json 文件该值等于文件名； <control_name> 对应想创建的控件的名称，该控件需要置于 UI json 文件顶层（即与 main 画布同级，不能是任何一个控件的子控件），也可在UI编辑器中将该控件添加至自定义控件库
        :param str child_name: 子控件名称
        :param bool force_update: 是否需要强制刷新；默认为 True；设为 True 则进行同一帧或者下一帧刷新，设为 False 则当前帧和下一帧均不刷新，需要手动调用 .update_screen() 进行刷新；如有大量新建子控件操作且在同一帧执行，建议设为 False，需要更新时再调用 .update_screen() 接口刷新界面及相关控件数据

        :return: 子控件的 NyControl 实例；创建失败时返回 None
        :rtype: NyControl|None

        :raise ControlAlreadyExistsError: 已存在同名子控件时抛出
        """
        path = self.path + "/" + child_name
        if self.ny_screen_node.is_control_exist(path):
            raise error.ControlAlreadyExistsError(path)
        if not self._screen_node.CreateChildControl(def_name, child_name, self._base_control, force_update):
            return
        return NyControl(self.ny_screen_node, path)

    def clone_to(self, parent, name="", sync_refresh=True, force_update=True):
        """
        将当前控件克隆到指定父控件下。

        示例
        ----

        >>> self.button_1 = self.button.clone_to(self.panel, "button_1")

        参见
        ----

        - ``NyControl.clone_from()`` -- 将指定控件克隆到当前控件下。
        - ``NyControl.add_child()`` -- 添加新的子控件。

        -----

        :param str|NyControl parent: 父控件路径或实例
        :param str name: 新控件的名称；默认为当前控件的名称
        :param bool sync_refresh: 是否需要同步刷新；默认为 True；设为 True 时游戏在同一帧计算该控件的 size 等相关数据，设为 False 则在下一帧进行计算；如同一帧有大量 clone 操作建议设为 False，操作结束后调用一次 .update_screen() 接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新；默认为 True；设为 True 则按照 sync_refresh 逻辑进行同一帧或者下一帧刷新，设为 False 则当前帧和下一帧均不刷新，需要手动调用 .update_screen() 进行刷新；如有大量 clone 操作且非在同一帧执行，建议设为 False，需要更新时再调用 .update_screen() 接口刷新界面及相关控件数据

        :return: 新控件实例，类型与当前控件相同；克隆失败时返回 None
        :rtype: NyControl|None

        :raise ControlAlreadyExistsError: 父控件已存在同名子控件时抛出
        """
        parent_path = parent if isinstance(parent, str) else parent.path
        if not name:
            name = self.name
        new_path = parent_path + "/" + name
        if self.ny_screen_node.is_control_exist(new_path):
            raise error.ControlAlreadyExistsError(new_path)
        if self._screen_node.Clone(self.path, parent_path, name, sync_refresh, force_update):
            return self.__class__(self.ny_screen_node, new_path, **self._kwargs)

    def clone_from(self, control, name="", sync_refresh=True, force_update=True):
        """
        将指定控件克隆到当前控件下（当前控件作为父控件）。

        示例
        ----

        >>> self.button_1 = self.panel.clone_from(self.button, "button_1")

        参见
        ----

        - ``NyControl.clone_to()`` -- 将当前控件克隆到指定父控件下。
        - ``NyControl.add_child()`` -- 添加新的子控件。

        -----

        :param str|NyControl control: 被克隆控件的路径或实例
        :param str name: 新控件的名称；默认为被克隆控件的名称
        :param bool sync_refresh: 是否需要同步刷新；默认为 True；设为 True 时游戏在同一帧计算该控件的 size 等相关数据，设为 False 则在下一帧进行计算；如同一帧有大量 clone 操作建议设为 False，操作结束后调用一次 .update_screen() 接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新；默认为 True；设为 True 则按照 sync_refresh 逻辑进行同一帧或者下一帧刷新，设为 False 则当前帧和下一帧均不刷新，需要手动调用 .update_screen() 进行刷新；如有大量 clone 操作且非在同一帧执行，建议设为 False，需要更新时再调用 .update_screen() 接口刷新界面及相关控件数据

        :return: 新控件的 NyControl 实例；克隆失败时返回 None
        :rtype: NyControl|None

        :raise ControlAlreadyExistsError: 父控件已存在同名子控件时抛出
        """
        control_path = control if isinstance(control, str) else control.path
        if not name:
            name = control_path.split("/")[-1]
        new_path = self.path + "/" + name
        if self.ny_screen_node.is_control_exist(new_path):
            raise error.ControlAlreadyExistsError(new_path)
        if self._screen_node.Clone(control_path, self.path, name, sync_refresh, force_update):
            return self.__class__(self.ny_screen_node, new_path, **self._kwargs)

    def children(self, level=1):
        """
        获取指定层次上的所有子控件。

        说明
        ----

        层次指的是从当前控件向下的子控件层数，而不是控件的渲染层级 ``layer`` 。

        示例
        ----

        >>> self.direct_children = self.panel.children()
        >>> self.all_children = self.panel.children(0)

        参见
        ----

        - ``NyControl.children_path()`` -- 获取指定层次上的所有子控件的路径。
        - ``NyControl.get_child()`` -- 获取指定子控件。

        -----

        :param int level: 子控件层次；默认为 1 ，传入 0 或负值表示所有层次

        :return: 指定层次所有子控件的 NyControl 列表
        :rtype: list[NyControl]
        """
        return [NyControl(self.ny_screen_node, p) for p in self.children_path(level)]

    def children_path(self, level=1):
        """
        获取指定层次上的所有子控件的路径。

        说明
        ----

        层次指的是从当前控件向下的子控件层数，而不是控件的渲染层级 ``layer`` 。

        示例
        ----

        >>> paths = self.panel.children_path(0)
        >>> for path in paths:
        ...     print(path)

        参见
        ----

        - ``NyControl.children()`` -- 获取指定层次上的所有子控件。

        -----

        :param int level: 子控件层次；默认为 1 ，传入 0 或负值表示所有层次

        :return: 指定层次所有子控件的路径列表
        :rtype: list[str]
        """
        return get_children_path_by_level(self._base_control, self.ny_screen_node, level)

    def destroy(self):
        """
        销毁控件。

        示例
        ----

        >>> button = self.panel.get_child("button")
        >>> if button:
        ...     button.destroy()

        -----

        :return: 无
        :rtype: None
        """
        self.ny_screen_node._destroy_nyc(self)

    # endregion

    # region Conversion ================================================================================================

    @classmethod
    def auto(cls, ny_screen_node, path):
        """
        [类方法]

        自动根据控件类型创建对应的控件实例。

        示例
        ----

        >>> self.button = nyl.NyControl.auto(self, "/panel/button") # 返回NyButton实例
        >>> def on_button_up(args):
        ...     pass
        >>> self.button.set_callback(on_button_up, nyl.NyButton.UP)

        -----

        :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该控件的 NyScreenNode 或 NyScreenProxy 实例
        :param str path: 控件路径

        :return: 控件实例
        :rtype: NyControl

        :raise TypeError: 传入的 ny_screen_node 没有继承 NyScreenNode 或 NyScreenProxy 时抛出
        :raise ControlNotFoundError: 找不到指定路径的控件时抛出
        """
        if cls is not NyControl:
            return cls(ny_screen_node, path)
        # todo

    def _try_convert(self, base_control):
        conv_func = _CONVERSION_FUNC_MAP[self.CONTROL_TYPE]
        c = getattr(base_control, conv_func)()
        if not c:
            raise error.ControlTypeNotMatchedError(self.CONTROL_TYPE, self.path)
        return c

    @kwargs_defaults(touch_event_params=None)
    def to_button(self, **kwargs):
        """
        转换为 ``NyButton`` 实例。

        示例
        ----

        >>> self.button = (self.panel / "button").to_button(
        ...     touch_event_params={'isSwallow': False}
        ... )

        -----

        :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 `AddTouchEventParams() <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E8%87%AA%E5%AE%9A%E4%B9%89UI/UI%E6%8E%A7%E4%BB%B6.html?key=AddTouchEventParams&docindex=1&type=0>`_

        :return: NyButton 实例
        :rtype: NyButton

        :raise ControlTypeNotMatchedError: 控件非按钮类型时抛出
        """
        from . import NyButton
        if isinstance(self, NyButton):
            return self
        return NyButton(self.ny_screen_node, self.path, **kwargs)

    def to_image(self, **kwargs):
        """
        转换为 ``NyImage`` 实例。

        示例
        ----

        >>> self.image = (self.panel / "image").to_image()

        -----

        :return: NyImage 实例
        :rtype: NyImage

        :raise ControlTypeNotMatchedError: 控件非图片类型时抛出
        """
        from . import NyImage
        if isinstance(self, NyImage):
            return self
        return NyImage(self.ny_screen_node, self.path, **kwargs)

    def to_label(self, **kwargs):
        """
        转换为 ``NyLabel`` 实例。

        示例
        ----

        >>> self.label = (self.panel / "label").to_label()

        -----

        :return: NyLabel 实例
        :rtype: NyLabel

        :raise ControlTypeNotMatchedError: 控件非文本类型时抛出
        """
        from . import NyLabel
        if isinstance(self, NyLabel):
            return self
        return NyLabel(self.ny_screen_node, self.path, **kwargs)

    def to_input_panel(self, **kwargs):
        """
        转换为 ``NyInputPanel`` 实例。

        示例
        ----

        >>> self.input_panel = (self.panel / "input_panel").to_input_panel()

        -----

        :return: NyInputPanel 实例
        :rtype: NyInputPanel

        :raise ControlTypeNotMatchedError: 控件非输入面板类型时抛出
        """
        from . import NyInputPanel
        if isinstance(self, NyInputPanel):
            return self
        return NyInputPanel(self.ny_screen_node, self.path, **kwargs)

    def to_stack_panel(self, **kwargs):
        """
        转换为 ``NyStackPanel`` 实例。

        示例
        ----

        >>> self.stack_panel = (self.panel / "stack_panel").to_stack_panel()

        -----

        :return: NyStackPanel 实例
        :rtype: NyStackPanel

        :raise ControlTypeNotMatchedError: 控件非栈面板类型时抛出
        """
        from . import NyStackPanel
        if isinstance(self, NyStackPanel):
            return self
        return NyStackPanel(self.ny_screen_node, self.path, **kwargs)

    def to_edit_box(self, **kwargs):
        """
        转换为 ``NyEditBox`` 实例。

        示例
        ----

        >>> self.edit_box = (self.panel / "edit_box").to_edit_box()

        -----

        :return: NyEditBox 实例
        :rtype: NyEditBox

        :raise ControlTypeNotMatchedError: 控件非文本编辑框类型时抛出
        """
        from . import NyEditBox
        if isinstance(self, NyEditBox):
            return self
        return NyEditBox(self.ny_screen_node, self.path, **kwargs)

    def to_paper_doll(self, **kwargs):
        """
        转换为 ``NyPaperDoll`` 实例。

        示例
        ----

        >>> self.paper_doll = (self.panel / "paper_doll").to_paper_doll()

        -----

        :return: NyPaperDoll 实例
        :rtype: NyPaperDoll

        :raise ControlTypeNotMatchedError: 控件非纸娃娃类型时抛出
        """
        from . import NyPaperDoll
        if isinstance(self, NyPaperDoll):
            return self
        return NyPaperDoll(self.ny_screen_node, self.path, **kwargs)

    def to_item_renderer(self, **kwargs):
        """
        转换为 ``NyItemRenderer`` 实例。

        示例
        ----

        >>> self.item_renderer = (self.panel / "item_renderer").to_item_renderer()

        -----

        :return: NyItemRenderer 实例
        :rtype: NyItemRenderer

        :raise ControlTypeNotMatchedError: 控件非物品渲染器类型时抛出
        """
        from . import NyItemRenderer
        if isinstance(self, NyItemRenderer):
            return self
        return NyItemRenderer(self.ny_screen_node, self.path, **kwargs)

    def to_scroll_view(self, **kwargs):
        """
        转换为 ``NyScrollView`` 实例。

        示例
        ----

        >>> self.scroll_view = (self.panel / "scroll_view").to_scroll_view()

        -----

        :return: NyScrollView 实例
        :rtype: NyScrollView

        :raise ControlTypeNotMatchedError: 控件非滚动视图类型时抛出
        """
        from . import NyScrollView
        if isinstance(self, NyScrollView):
            return self
        return NyScrollView(self.ny_screen_node, self.path, **kwargs)

    def to_grid(self, **kwargs):
        """
        转换为 ``NyGrid`` 实例。

        说明
        ----

        关于 ``cell_visible_binding`` 与 ``collection_name`` 参数的说明：

        - 该参数用于 ``.grid_size`` 、 ``.dimension`` 等接口，实现动态设置网格元素的数量（多余元素将通过设置 ``visible`` 为 ``False`` 的方式隐藏），不使用该接口可忽略这两个参数。
        - 由于网格控件的特性，设置元素的 ``visible`` 需要使用绑定，请在你的 **网格模板控件** 的 json 中添加以下绑定，然后将 ``"binding_name"`` 的值设置给 ``cell_visible_binding`` 参数 。
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
        - 最后，将 **网格** json 中的 ``"collection_name"`` 字段的值设置给 ``collection_name`` 参数即可。

        示例
        ----

        >>> self.grid = (self.panel / "grid").to_grid()

        -----

        :param bool is_stack_grid: [仅关键字参数] 是否是 StackGrid；默认为 False
        :param str template_name: [仅关键字参数] 网格模板控件名称，即 "grid_item_template" 字段或UI编辑器中的网格“内容”所使用的控件；仅模板控件名称以数字结尾时需要传入该参数
        :param str cell_visible_binding: [仅关键字参数] 用于控制网格元素显隐性的绑定名称，详见上方说明
        :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明

        :return: NyGrid实例
        :rtype: NyGrid

        :raise ControlTypeNotMatchedError: 控件非网格类型时抛出
        """
        from . import NyGrid
        if isinstance(self, NyGrid):
            return self
        return NyGrid(self.ny_screen_node, self.path, **kwargs)

    def to_progress_bar(self, **kwargs):
        """
        转换为 ``NyProgressBar`` 实例。

        示例
        ----

        >>> self.progress_bar = (self.panel / "progress_bar").to_progress_bar()

        -----

        :return: NyProgressBar 实例
        :rtype: NyProgressBar

        :raise ControlTypeNotMatchedError: 控件非进度条类型时抛出
        """
        from . import NyProgressBar
        if isinstance(self, NyProgressBar):
            return self
        return NyProgressBar(self.ny_screen_node, self.path, **kwargs)

    def to_toggle(self, **kwargs):
        """
        转换为 ``NyToggle`` 实例。

        示例
        ----

        >>> self.toggle = (self.panel / "toggle").to_toggle()

        -----

        :return: NyToggle 实例
        :rtype: NyToggle

        :raise ControlTypeNotMatchedError: 控件非开关类型时抛出
        """
        from . import NyToggle
        if isinstance(self, NyToggle):
            return self
        return NyToggle(self.ny_screen_node, self.path, **kwargs)

    def to_slider(self, **kwargs):
        """
        转换为 ``NySlider`` 实例。

        示例
        ----

        >>> self.slider = (self.panel / "slider").to_slider()

        -----

        :return: NySlider 实例
        :rtype: NySlider

        :raise ControlTypeNotMatchedError: 控件非滑动条类型时抛出
        """
        from . import NySlider
        if isinstance(self, NySlider):
            return self
        return NySlider(self.ny_screen_node, self.path, **kwargs)

    def to_selection_wheel(self, **kwargs):
        """
        转换为 ``NySelectionWheel`` 实例。

        示例
        ----

        >>> self.selection_wheel = (self.panel / "selection_wheel").to_selection_wheel()

        -----

        :return: NySelectionWheel 实例
        :rtype: NySelectionWheel

        :raise ControlTypeNotMatchedError: 控件非轮盘类型时抛出
        """
        from . import NySelectionWheel
        if isinstance(self, NySelectionWheel):
            return self
        return NySelectionWheel(self.ny_screen_node, self.path, **kwargs)

    def to_combo_box(self, **kwargs):
        """
        转换为 ``NyComboBox`` 实例。

        示例
        ----

        >>> self.combo_box = (self.panel / "combo_box").to_combo_box()

        -----

        :return: NyComboBox 实例
        :rtype: NyComboBox

        :raise ControlTypeNotMatchedError: 控件非下拉框类型时抛出
        """
        from . import NyComboBox
        if isinstance(self, NyComboBox):
            return self
        return NyComboBox(self.ny_screen_node, self.path, **kwargs)

    def to_mini_map(self, **kwargs):
        """
        转换为 ``NyMiniMap`` 实例。

        示例
        ----

        >>> self.mini_map = (self.panel / "mini_map").to_mini_map()

        -----

        :return: NyMiniMap 实例
        :rtype: NyMiniMap

        :raise ControlTypeNotMatchedError: 控件非小地图类型时抛出
        """
        from . import NyMiniMap
        if isinstance(self, NyMiniMap):
            return self
        return NyMiniMap(self.ny_screen_node, self.path, **kwargs)

    # endregion

    # region Compatibility =============================================================================================

    set_position                    = SetPosition                 = lambda s, *a, **k: s._base_control.SetPosition(*a, **k)
    set_full_size                   = SetFullSize                 = lambda s, *a, **k: s._base_control.SetFullSize(*a, **k)
    get_full_size                   = GetFullSize                 = lambda s, *a, **k: s._base_control.GetFullSize(*a, **k)
    set_full_position               = SetFullPosition             = lambda s, *a, **k: s._base_control.SetFullPosition(*a, **k)
    get_full_position               = GetFullPosition             = lambda s, *a, **k: s._base_control.GetFullPosition(*a, **k)
    set_anchor_from                 = SetAnchorFrom               = lambda s, *a, **k: s._base_control.SetAnchorFrom(*a, **k)
    get_anchor_from                 = GetAnchorFrom               = lambda s, *a, **k: s._base_control.GetAnchorFrom(*a, **k)
    set_anchor_to                   = SetAnchorTo                 = lambda s, *a, **k: s._base_control.SetAnchorTo(*a, **k)
    get_anchor_to                   = GetAnchorTo                 = lambda s, *a, **k: s._base_control.GetAnchorTo(*a, **k)
    set_clip_offset                 = SetClipOffset               = lambda s, *a, **k: s._base_control.SetClipOffset(*a, **k)
    get_clip_offset                 = GetClipOffset               = lambda s, *a, **k: s._base_control.GetClipOffset(*a, **k)
    set_clips_children              = SetClipsChildren            = lambda s, *a, **k: s._base_control.SetClipsChildren(*a, **k)
    get_clips_children              = GetClipsChildren            = lambda s, *a, **k: s._base_control.GetClipsChildren(*a, **k)
    set_max_size                    = SetMaxSize                  = lambda s, *a, **k: s._base_control.SetMaxSize(*a, **k)
    get_max_size                    = GetMaxSize                  = lambda s, *a, **k: s._base_control.GetMaxSize(*a, **k)
    set_min_size                    = SetMinSize                  = lambda s, *a, **k: s._base_control.SetMinSize(*a, **k)
    get_min_size                    = GetMinSize                  = lambda s, *a, **k: s._base_control.GetMinSize(*a, **k)
    get_position                    = GetPosition                 = lambda s, *a, **k: s._base_control.GetPosition(*a, **k)
    get_global_position             = GetGlobalPosition           = lambda s, *a, **k: s._base_control.GetGlobalPosition(*a, **k)
    set_size                        = SetSize                     = lambda s, *a, **k: s._base_control.SetSize(*a, **k)
    get_size                        = GetSize                     = lambda s, *a, **k: s._base_control.GetSize(*a, **k)
    set_visible                     = SetVisible                  = lambda s, *a, **k: s._base_control.SetVisible(*a, **k)
    get_visible                     = GetVisible                  = lambda s, *a, **k: s._base_control.GetVisible(*a, **k)
    set_touch_enable                = SetTouchEnable              = lambda s, *a, **k: s._base_control.SetTouchEnable(*a, **k)
    set_alpha                       = SetAlpha                    = lambda s, *a, **k: s._base_control.SetAlpha(*a, **k)
    set_layer                       = SetLayer                    = lambda s, *a, **k: s._base_control.SetLayer(*a, **k)
    get_path                        = GetPath                     = lambda s, *a, **k: s._base_control.GetPath(*a, **k)
    get_child_by_name               = GetChildByName              = lambda s, *a, **k: s._base_control.GetChildByName(*a, **k)
    get_child_by_path               = GetChildByPath              = lambda s, *a, **k: s._base_control.GetChildByPath(*a, **k)
    reset_animation                 = resetAnimation              = lambda s, *a, **k: s._base_control.resetAnimation(*a, **k)
    pause_animation                 = PauseAnimation              = lambda s, *a, **k: s._base_control.PauseAnimation(*a, **k)
    play_animation                  = PlayAnimation               = lambda s, *a, **k: s._base_control.PlayAnimation(*a, **k)
    stop_animation                  = StopAnimation               = lambda s, *a, **k: s._base_control.StopAnimation(*a, **k)
    set_animation                   = SetAnimation                = lambda s, *a, **k: s._base_control.SetAnimation(*a, **k)
    remove_animation                = RemoveAnimation             = lambda s, *a, **k: s._base_control.RemoveAnimation(*a, **k)
    set_anim_end_callback           = SetAnimEndCallback          = lambda s, *a, **k: s._base_control.SetAnimEndCallback(*a, **k)
    remove_anim_end_callback        = RemoveAnimEndCallback       = lambda s, *a, **k: s._base_control.RemoveAnimEndCallback(*a, **k)
    is_anim_end_callback_registered = IsAnimEndCallbackRegistered = lambda s, *a, **k: s._base_control.IsAnimEndCallbackRegistered(*a, **k)
    get_property_bag                = GetPropertyBag              = lambda s, *a, **k: s._base_control.GetPropertyBag(*a, **k)
    set_property_bag                = SetPropertyBag              = lambda s, *a, **k: s._base_control.SetPropertyBag(*a, **k)
















