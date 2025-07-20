# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-11
|
| ==============================================
"""


from typing import Any, Literal, Callable, NoReturn, Dict, Optional, TypeVar, Generator, Type
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ...._core._types._typing import UiPathOrControl, FTuple2, AnchorType, FullSizeDict, FullPositionDict, UiPropertyNames, UiPropertyNamesAll
from ...._core._utils import args_type_check, cached_property
from ..screen_node import ScreenNodeExtension
from . import *


_T = TypeVar("_T")


class NyControl(object):
    _CONTROL_TYPE: str
    _screen_node: ScreenNode
    ui_node: ScreenNodeExtension
    """
    | 控件所在UI类的实例。
    """
    base_control: BaseUIControl
    """
    | 控件 ``BaseUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        control: BaseUIControl,
        **kwargs: Any
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3
    def __destroy__(self) -> None: ...
    def iter_children_control(self, level: int = 1) -> Generator[NyControl, None, None]: ...
    def iter_children_path(self, level: int = 1) -> Generator[str, None, None]: ...
    @classmethod
    def create(
        cls: Type[_T],
        screen_node_ex: ScreenNodeExtension,
        path_or_control: UiPathOrControl,
        **kwargs: Any,
    ) -> Optional[_T]: ...
    @cached_property
    def path(self) -> str: ...
    @cached_property
    def parent_path(self) -> str: ...
    @cached_property
    def parent_control(self) -> Optional[NyControl]: ...
    def destroy(self) -> None: ...
    def to_button(self, touch_event_params: Optional[Dict[str, Any]] = None) -> NyButton: ...
    def to_image(self) -> NyImage: ...
    def to_label(self) -> NyLabel: ...
    def to_input_panel(self) -> NyInputPanel: ...
    def to_stack_panel(self) -> NyStackPanel: ...
    def to_edit_box(self) -> NyEditBox: ...
    def to_netease_paper_doll(self) -> NyPaperDoll: ...
    def to_item_renderer(self) -> NyItemRenderer: ...
    def to_scroll_view(self) -> NyScrollView: ...
    def to_grid(self, is_stack_grid: bool = False) -> NyGrid: ...
    def to_progress_bar(self) -> NyProgressBar: ...
    def to_toggle(self) -> NyToggle: ...
    def to_slider(self) -> NySlider: ...
    def to_selection_wheel(self) -> NySelectionWheel: ...
    def to_combo_box(self) -> NyComboBox: ...
    def to_mini_map(self) -> NyMiniMap: ...
    @property
    def position(self) -> FTuple2: ...
    @position.setter
    def position(self, val: FTuple2) -> None: ...
    @property
    def anchor_from(self) -> AnchorType: ...
    @anchor_from.setter
    def anchor_from(self, val: AnchorType) -> None: ...
    @property
    def anchor_to(self) -> AnchorType: ...
    @anchor_to.setter
    def anchor_to(self, val: AnchorType) -> None: ...
    @property
    def clip_offset(self) -> FTuple2: ...
    @clip_offset.setter
    def clip_offset(self, val: FTuple2) -> None: ...
    @property
    def clip_children(self) -> bool: ...
    @clip_children.setter
    def clip_children(self, val: bool) -> None: ...
    @property
    def full_position_x(self) -> FullPositionDict: ...
    @full_position_x.setter
    def full_position_x(self, val: FullPositionDict) -> None: ...
    @property
    def full_position_y(self) -> FullPositionDict: ...
    @full_position_y.setter
    def full_position_y(self, val: FullPositionDict) -> None: ...
    @property
    def full_size_x(self) -> FullSizeDict: ...
    @full_size_x.setter
    def full_size_x(self, val: FullSizeDict) -> None: ...
    @property
    def full_size_y(self) -> FullSizeDict: ...
    @full_size_y.setter
    def full_size_y(self, val: FullSizeDict) -> None: ...
    @property
    def global_position(self) -> FTuple2: ...
    @global_position.setter
    def global_position(self, val: FTuple2) -> None: ...
    @property
    def max_size(self) -> FTuple2: ...
    @max_size.setter
    def max_size(self, val: FTuple2) -> None: ...
    @property
    def min_size(self) -> FTuple2: ...
    @min_size.setter
    def min_size(self, val: FTuple2) -> None: ...
    @property
    def size(self) -> FTuple2: ...
    @size.setter
    def size(self, val: FTuple2) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, val: bool) -> None: ...
    @property
    def alpha(self) -> NoReturn: ...
    @alpha.setter
    def alpha(self, val: float) -> None: ...
    @property
    def layer(self) -> int: ...
    @layer.setter
    def layer(self, val: int) -> None: ...
    @property
    def touch_enable(self) -> NoReturn: ...
    @touch_enable.setter
    def touch_enable(self, val: bool) -> None: ...

    def SetPosition(self, pos: FTuple2) -> None:
        """
        | 设置控件相对父节点的坐标。

        -----

        :param tuple[float,float] pos: 坐标

        :return: 无
        :rtype: None
        """
    def SetFullSize(self, axis: Literal["x", "y"], param_dict: FullSizeDict) -> bool:
        """
        | 设置控件的大小，支持比例形式以及绝对值。
        | ``param_dict`` 参数：
        - ``fit`` -- bool，是否自适应父控件，默认值为False，可以不写该键值
        - ``followType`` -- str，跟随类型，默认值为"none"，可以不写该键值
        - ``relativeValue`` -- float，相对于跟随控件的比例值，默认值为0，可以不写该键值
        - ``absoluteValue`` -- float，设置的绝对值，默认值为0，可以不写该键值
        | 控件的大小支持复杂的计算来实现自适应布局，形式为 ``absoluteValue`` + ``relativeValue`` * 跟随值。其中跟随值由跟随的控件以及当前设置的属性共同决定。比如当前设置的是控件的宽度，并且跟随控件为父控件，则跟随值为父控件的宽度。 而跟随的控件是特定的，是与控件本身有一定关系的，比如控件的父控件，子控件等，可以通过设置 ``followType`` 的值来指定。
        | ``followType`` 可选的值：
        - ``"none"`` -- 无跟随，实际计算的时候只考虑absoluteValue
        - ``"parent"`` -- 跟随控件为父控件
        - ``"maxChildren"`` -- 跟随控件为最大子控件（设置宽度则为最大宽度，设置高度则为最大高度），relativeValue无论如何设置都为1.0
        - ``"maxSibling"`` -- 跟随控件为最大兄弟控件（设置宽度则为最大宽度，设置高度则为最大高度），relativeValue无论如何设置都为1.0
        - ``"children"`` -- 跟随值等于所有子节点之和
        - ``"x"`` -- 跟随值等于控件本身的宽度，该值仅当 axis == "y" 才生效
        - ``"y"`` -- 跟随值等于控件本身的高度，该值仅当 axis == "x" 才生效
        | ``fit`` 参数用来指定是否自适应父控件，如果是自适应父控件，则 ``absoluteValue`` ， ``followType`` ， ``relativeValue`` 参数均会失效，控件的值直接取自父控件的值。
        | 设置跟随类型的时候请务必小心，不要造成依赖循环，比如父控件宽度依赖子控件的宽度，而子控件的宽度又依赖于父控件这类情况，这样即使设置成功，结果也是未知的。

        -----

        :param str axis: 设置的轴向，可选的值有["x", "y"]，"x"表示设置控件的宽度，"y"表示设置控件的高度
        :param dict param_dict: 设置的参数

        :return: 是否成功
        :rtype: bool
        """
    def GetFullSize(self, axis: Literal["x", "y"]) -> FullSizeDict:
        """
        获取控件的大小，支持百分比以及绝对值。

        -----

        :param str axis: 设置的轴向，可选的值有["x", "y"]，"x"表示设置控件的宽度，"y"表示设置控件的高度

        :return: 控件的大小信息，详见SetFullSize
        :rtype: dict
        """
    def SetFullPosition(self, axis: Literal["x", "y"], param_dict: FullPositionDict) -> bool:
        """
        | 设置控件的锚点坐标（全局坐标），支持比例值以及绝对值。
        | ``param_dict`` 参数：
        - ``followType`` -- str，跟随类型，默认值为"none"，可以不写该键值
        - ``relativeValue`` -- float，相对于跟随控件的比例值，默认值为0，可以不写该键值
        - ``absoluteValue`` -- float，设置的绝对值，默认值为0，可以不写该键值
        | 控件的坐标支持复杂的计算来实现自适应布局，形式为 ``absoluteValue`` + ``relativeValue`` * 跟随值。其中跟随值由跟随的控件以及当前设置的属性共同决定。比如当前设置的是控件的x坐标，并且跟随控件为父控件，则跟随值为父控件的宽度。而跟随的控件是特定的，是与控件本身有一定关系的，比如控件的父控件，子控件等，可以通过设置 ``followType`` 的值来指定。
        | ``followType`` 可选的值：
        - ``"none"`` -- 无跟随，实际计算的时候只考虑absoluteValue
        - ``"parent"`` -- 跟随控件为父控件
        - ``"maxChildren"`` -- 跟随控件为最大子控件（设置x则为最大宽度，设置y则为最大高度），relativeValue无论如何设置都为1.0
        - ``"maxSibling"`` -- 跟随控件为最大兄弟控件（设置x则为最大宽度，设置y则为最大高度），relativeValue无论如何设置都为1.0
        - ``"children"`` -- 跟随值等于所有子节点之和（如果是x则计算的是子节点的宽度之和，如果是y则计算的是子节点的高度之和）
        - ``"x"`` -- 跟随值等于控件本身的宽度，该值仅当 axis == "y" 才生效
        - ``"y"`` -- 跟随值等于控件本身的高度，该值仅当 axis == "x" 才生效
        | 设置跟随类型的时候请务必小心，不要造成依赖循环，比如父控件x坐标依赖子控件的宽度，而子控件的宽度又依赖于父控件这类情况，这样即使设置成功，结果也是未知的。

        -----

        :param str axis: 设置的轴向，可选的值有["x", "y"]，"x"表示设置控件锚点的x坐标，"y"表示设置控件锚点的y坐标
        :param dict param_dict: 设置的参数

        :return: 是否成功
        :rtype: bool
        """
    def GetFullPosition(self, axis: Literal["x", "y"]) -> FullPositionDict:
        """
        | 获取控件的锚点坐标，支持比例值以及绝对值。

        -----

        :param str axis: 设置的轴向，可选的值有["x", "y"]，"x"表示设置控件锚点的x坐标，"y"表示设置控件锚点的y坐标

        :return: 控件的位置信息，详见SetFullPosition
        :rtype: dict
        """
    def SetAnchorFrom(self, ancho_from: AnchorType) -> bool:
        """
        | 设置控件相对于父节点的锚点。
        | ``anchor_from`` 可选的值：
        - ``"top_left"`` -- 相对于父节点的左上角
        - ``"top_middle"`` -- 相对于父节点的上边中间
        - ``"top_right"`` -- 相对于父节点的右上角
        - ``"left_middle"`` -- 相对于父节点的左边中间
        - ``"center"`` -- 相对于父节点的中间
        - ``"right_middle"`` -- 相对于父节点的右边中间
        - ``"bottom_left"`` -- 相对于父节点的底部左边
        - ``"bottom_middle"`` -- 相对于父节点的部中间
        - ``"bottom_right"`` -- 相对于父节点的底部右边

        -----

        :param str ancho_from: 相对于父节点的锚点

        :return: 是否成功
        :rtype: bool
        """
    def GetAnchorFrom(self) -> AnchorType:
        """
        | 判断控件相对于父节点的哪个锚点来计算位置与大小。

        -----

        :return: 控件计算位置大小所依赖的父节点锚点位置信息，详见SetAnchorFrom
        :rtype: str
        """
    def SetAnchorTo(self, anchor_to: AnchorType) -> bool:
        """
        | 设置控件自身锚点位置。

        -----

        :param str anchor_to: 控件自身锚点位置，详见SetAnchorFrom

        :return: 是否成功
        :rtype: bool
        """
    def GetAnchorTo(self) -> AnchorType:
        """
        | 获取控件自身锚点位置信息。

        -----

        :return: 控件自身锚点位置，详见SetAnchorFrom
        :rtype: str
        """
    def SetClipOffset(self, clip_offset: FTuple2) -> bool:
        """
        设置控件的裁剪偏移信息。

        -----

        :param tuple[float,float] clip_offset: 该控件的裁剪偏移信息，第一项为横轴，第二项为纵轴

        :return: 是否成功
        :rtype: bool
        """
    def GetClipOffset(self) -> FTuple2:
        """
        | 获取控件的裁剪偏移信息。

        -----

        :return: 该控件的裁剪偏移信息，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def SetClipsChildren(self, clips_children: bool) -> bool:
        """
        | 设置控件是否开启裁剪内容。

        -----

        :param bool clips_children: True表示开启，False表示关闭

        :return:
        :rtype: bool
        """
    def GetClipsChildren(self) -> bool:
        """
        | 返回某控件是否开启裁剪内容。

        -----

        :return: 该控件是否已开启裁剪内容
        :rtype: bool
        """
    def SetMaxSize(self, max_size: FTuple2) -> bool:
        """
        | 设置控件所允许的最大的大小值。
        | ``maxSize`` 为 ``(0,0)`` 表示无限制。
        -----

        :param tuple[float,float] max_size: 该控件所允许的最大的大小值，第一项为横轴，第二项为纵轴

        :return: 是否成功
        :rtype: bool
        """
    def GetMaxSize(self) -> FTuple2:
        """
        | 获取控件所允许的最大的大小值。

        -----

        :return: 该控件所允许的最大的大小值，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def SetMinSize(self, min_size: FTuple2) -> bool:
        """
        | 设置控件所允许的最小的大小值。
        | ``min_size`` 为 ``(0,0)`` 表示无限制。

        -----

        :param tuple[float,float] min_size: 该控件所允许的最小的大小值，第一项为横轴，第二项为纵轴

        :return: 是否成功
        :rtype: bool
        """
    def GetMinSize(self) -> FTuple2:
        """
        | 获取控件所允许的最小的大小值。

        -----

        :return: 该控件所允许的最小的大小值，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def GetPosition(self) -> FTuple2:
        """
        | 获取控件相对父节点的坐标。

        -----

        :return: 该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def GetGlobalPosition(self) -> FTuple2:
        """
        | 获取控件全局坐标。

        -----

        :return: 该控件全局坐标信息，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def SetSize(self, size: FTuple2, resize_children: bool = False) -> None:
        """
        | 设置控件的大小。

        -----

        :param tuple[float,float] size: 该控件的大小信息，第一项为横轴，第二项为纵轴
        :param bool resize_children: 是否同时调整子控件尺寸，默认为False

        :return: 无
        :rtype: None
        """
    def GetSize(self) -> FTuple2:
        """
        | 获取控件的大小。

        -----

        :return: 该控件的大小信息，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def SetVisible(self, visible: bool, force_update: bool = True) -> None:
        """
        | 根据控件路径选择是否显示某控件，可以通过传入空字符串（""）的方式来调整整个JSON的显示/隐藏。
        | 特殊情况说明：当该接口的调用来自滚动列表内容控件中的按钮回调，且调用目的是隐藏滚动列表控件或其父节点控件时，将 ``force_update`` 参数置 ``True`` 会导致滚动列表数据异常。若没有刷新界面的必要请将 ``force_update`` 参数置 ``False`` ，若有请使用定时器延迟执行手动 ``UpdateScreen`` 接口。
        -----

        :param bool visible: False为隐藏该控件，True为显示该控件
        :param bool force_update: 是否需要强制刷新，默认值为True。置True则按照马上进行刷新，新的visible状态生效。置False，则需要再次调用UpdateScreen使新状态生效。如有大量SetVisible操作且非在同一帧执行，建议设置为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 无
        :rtype: None
        """
    def GetVisible(self) -> bool:
        """
        | 根据控件路径返回某控件是否已显示。

        -----

        :return: 该控件是否已显示
        :rtype: bool
        """
    def SetTouchEnable(self, enable: bool) -> None:
        """
        | 设置控件是否可点击交互。

        -----

        :param bool enable: False为不响应，True为恢复响应

        :return: 无
        :rtype: None
        """
    def SetAlpha(self, alpha: float) -> None:
        """
        | 设置节点的透明度，仅对image和label控件生效。

        -----

        :param float alpha: 透明度，取值0-1之间，0表示完全透明，1表示完全不透明

        :return: 无
        :rtype: None
        """
    def SetLayer(self, layer: int, sync_refresh: bool = True, force_update: bool = True) -> None:
        """
        | 设置控件节点的层级，可以通过传入空字符串（""）的方式来调整整个JSON的基础层级。

        -----

        :param int layer: 设置层级
        :param bool sync_refresh: 是否需要同步刷新，默认值为True。置True为游戏在同一帧根据该控件的层级进行相关计算，置False则在下一帧进行计算。如同一帧有大量SetLayer操作建议置False，操作结束后调用一次ScreenNode.UpdateScreen接口刷新界面及相关控件数据
        :param bool force_update: 是否需要强制刷新，默认值为True。置True则按照sync_refresh逻辑进行同步或者下一帧刷新，置False则当前帧和下一帧均不刷新，需要手动调用UpdateScreen进行刷新。如有大量SetLayer操作且非在同一帧执行，建议设置为False，需要更新时再调用UpdateScreen接口刷新界面及相关控件数据

        :return: 无
        :rtype: None
        """
    def GetPath(self) -> str:
        """
        | 返回当前控件的相对路径，路径从画布节点开始算起。

        -----

        :return: 当前控件的相对路径，路径从画布节点开始算起
        :rtype: str
        """
    def GetChildByName(self, child_name: str) -> BaseUIControl:
        """
        | 根据子控件的名称获取 ``BaseUIControl`` 实例。

        -----

        :param str child_name: 子节点名称

        :return: 子控件的BaseUIControl实例
        :rtype: BaseUIControl
        """
    def GetChildByPath(self, child_path: str) -> BaseUIControl:
        """
        | 根据相对路径获取 ``BaseUIControl`` 实例。

        -----

        :param str child_path: 相对当前BaseUIControl路径的路径

        :return: 子控件的BaseUIControl实例
        :rtype: BaseUIControl
        """
    def resetAnimation(self) -> None:
        """
        | 重置该控件的动画。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :return: 无
        :rtype: None
        """
    def PauseAnimation(self, property_name: UiPropertyNamesAll = "all") -> bool:
        """
        | 暂停动画，暂停后的动画会停在当前的状态。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str property_name: 动画的属性名称，默认值为"all"，表示暂停所有动画，不为"all"的时候表示单个动画的暂停，比如propertyName=="size"时，表示暂停尺寸属性上的动画

        :return: 是否成功
        :rtype: bool
        """
    def PlayAnimation(self, property_name: UiPropertyNamesAll = "all") -> bool:
        """
        | 继续播放动画，从动画当前状态开始播放
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str property_name: 动画的属性名称，默认值为"all"，表示暂停所有动画，不为"all"的时候表示单个动画的暂停，比如propertyName=="size"时，表示暂停尺寸属性上的动画

        :return: 是否成功
        :rtype: bool
        """
    def StopAnimation(self, property_name: UiPropertyNamesAll = "all") -> bool:
        """
        | 停止动画，动画将恢复到第一段动画片段的 ``from`` 状态。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str property_name: 动画的属性名称，默认值为"all"，表示暂停所有动画，不为"all"的时候表示单个动画的暂停，比如propertyName=="size"时，表示暂停尺寸属性上的动画

        :return: 是否成功
        :rtype: bool
        """
    def SetAnimation(
        self,
        property_name: UiPropertyNames,
        namespace: str,
        anim_name: str,
        auto_play: bool = False,
    ) -> bool:
        """
        | 给单一属性设置动画，已有重复的会设置失败，需要先remove。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。
        | 需要注意，设置动画本质上是拷贝动画数据到控件的动画组件里面，所以如果动画数据发生了改变（比如通过接口 ``RegisterUIAnimations`` 修改了动画数据），如果想要控件应用修改需要再次调用 ``SetAnimation`` 进行更新。

        -----

        :param str property_name: 要设置的动画的属性名称，无默认值，值必须为单一属性（不能填"all"）
        :param str namespace: 动画的命名空间，类似于自定义控件，动画也是可以定义到某个命名空间的
        :param str anim_name: 动画的名称
        :param bool auto_play: 动画添加后是否自动播放，默认值为False，表示不进行播放

        :return: 是否成功
        :rtype: bool
        """
    def RemoveAnimation(self, property_name: UiPropertyNames) -> bool:
        """
        | 删除单一属性的动画，删除后的值与当前状态有关，建议删除后重新设置该属性值。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str property_name: 要删除动画的属性名称，无默认值，值必须为单一属性（不能填"all"）

        :return: 是否成功
        :rtype: bool
        """
    def SetAnimEndCallback(self, anim_name: str, func: Callable) -> bool:
        """
        | 设置动画播放结束后的回调，每次设置都会覆盖上一次的设置。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str anim_name: 动画的名称，请不要包含动画的命名空间
        :param function func: 回调，无参数无返回值的函数

        :return: 是否成功
        :rtype: bool
        """
    def RemoveAnimEndCallback(self, anim_name: str) -> bool:
        """
        | 移除动画播放结束后的回调。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str anim_name: 动画的名称，请不要包含动画的命名空间

        :return: 是否成功
        :rtype: bool
        """
    def IsAnimEndCallbackRegistered(self, anim_name: str) -> bool:
        """
        | 控件是否对名称为 ``anim_name`` 的动画进行了注册回调。
        | UI属性动画相关，详见 `属性动画 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/19-%E6%8E%A7%E4%BB%B6%E5%B1%9E%E6%80%A7%E5%8A%A8%E7%94%BB.html>`_ 。

        -----

        :param str anim_name: 动画的名称，请不要包含动画的命名空间

        :return: 是否对名称为anim_name的动画进行了注册回调
        :rtype: bool
        """
    def GetPropertyBag(self) -> Dict[str, Any]:
        """
        | 获取PropertyBag。

        -----

        :return: PropertyBag字典
        :rtype: dict[str,Any]
        """
    def SetPropertyBag(self, params: Dict[str, Any]) -> None:
        """
        | 设置PropertyBag，将使用字典中的每个值来覆盖原本PropertyBag中的值。

        -----

        :param dict[str,Any] params: PropertyBag字典

        :return: 无
        :rtype: None
        """
