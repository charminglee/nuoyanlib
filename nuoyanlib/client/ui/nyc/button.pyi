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


from typing import Callable, Optional, Dict, Union, List, Any
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.common.utils.timer import CallLater
from ...._core._types._typing import ArgsDict, FTuple2, UiPathOrControl, ItemDict
from ...._core._types._checker import args_type_check
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....utils.enum import Enum
from ...._core.event._events import ClientEventEnum as Events


class NyButton(NyControl):
    _CALLBACK_API_MAP: Dict[int, str]
    class CommonChildPath(Enum[str]):
        default: str
        hover: str
        pressed: str
        button_label: str
    __vibrate_time: int
    _btn_callbacks: Dict[int, List[Callable]]
    _enabled_double_click: bool
    _double_click_time: float
    _enabled_long_click: bool
    _long_click_timer: Optional[CallLater]
    _movable_controls: List[BaseUIControl]
    _finger_pos: Optional[FTuple2]
    _ui_pos_data_key: str
    base_control: ButtonUIControl
    """
    | 按钮 ``ButtonUIControl`` 实例。
    """
    is_movable: ItemDict
    """
    | 按钮是否可拖动。
    """
    auto_save_pos: bool
    """
    | 是否自动保存按钮位置。
    """
    has_long_clicked: bool
    """
    | 按钮最近一次的按下中是否触发了长按。
    """
    touch_event_params: Optional[Dict[str, Any]]
    """
    | 按钮TouchEvent参数。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        btn_control: ButtonUIControl,
        **kwargs: Any,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def GetEntityByCoordReleaseClientEvent(self, args: ArgsDict) -> None: ...
    def set_default_texture(self, tex_path: str) -> None: ...
    def set_hover_texture(self, tex_path: str) -> None: ...
    def set_pressed_texture(self, tex_path: str) -> None: ...
    def set_text(self, text: str) -> None: ...
    @property
    def vibrate_time(self) -> int: ...
    @vibrate_time.setter
    @args_type_check(int, is_method=True)
    def vibrate_time(self, val: int) -> None: ...
    def set_callback(self, callback_type: int, func: Callable) -> bool: ...
    SetCallback = set_callback
    def remove_callback(self, callback_type: int, func: Callable) -> bool: ...
    RemoveCallback = remove_callback
    def set_movable(
        self,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrControl, List[UiPathOrControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    SetMovable = set_movable
    def set_movable_by_long_click(
        self,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrControl, List[UiPathOrControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    SetMovableByLongClick = set_movable_by_long_click
    def cancel_movable(self) -> None: ...
    CancelMovable = cancel_movable
    def clear_pos_data(self) -> bool: ...
    ClearPosData = clear_pos_data
    def save_pos_data(self) -> bool: ...
    SavePosData = save_pos_data
    def _set_movable_data(
        self,
        movable: bool,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrControl, List[UiPathOrControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    def _exec_callbacks(self, callback_type: int, args: Dict[str, Any]) -> None: ...
    def _on_touch_up_dc(self, args: ArgsDict) -> None: ...
    def _on_touch_down_lc(self, args: ArgsDict) -> None: ...
    def _cancel_long_click(self, args: ArgsDict) -> None: ...
    def _on_move(self, args: ArgsDict) -> None: ...
    def _on_long_click_mov(self, args: ArgsDict) -> None: ...
    def _on_touch_down_mov(self, args: ArgsDict) -> None: ...
    def _vibrate(self) -> None: ...
    def _set_offset(self, control: UiPathOrControl, offset: FTuple2) -> None: ...

    def AddTouchEventParams(self, args: Optional[dict] = None) -> None:
        """
        | 开启按钮回调功能，不调用该函数则按钮无回调。
        | ``args`` 参数说明：
        - ``isSwallow`` - bool，默认为True，按钮是否吞噬事件；为Ture时，点击按钮不会穿透到世界。如破坏方块、镜头转向不会被响应。

        -----

        :param dict|None args: 参数字典，默认为None，详细说明见上方

        :return: 无
        :rtype: None
        """
    def AddHoverEventParams(self) -> None:
        """
        | 开启按钮的悬浮回调功能，不调用该函数则按钮无悬浮回调。
        | 只有PC能生效，且只有 ``PushScreen`` 生成UI时生成的鼠标能产生悬浮回调！

        -----

        :return: 无
        :rtype: None
        """
    def SetButtonTouchDownCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置按钮按下时触发的回调函数。
        | 回调函数参数说明：
        - ``#collection_name`` -- str，按钮所属的集合名称
        - ``#collection_index`` -- int，按钮在集合所属的集合序号
        - ``ButtonState`` -- int，按钮的状态：Up为0，Down为1，默认是-1，建议使用TouchEvent
        - ``TouchEvent`` -- int，按钮的状态新版本：Up为0，Down为1，Cancel为3，Move为4，默认是-1
        - ``PrevButtonDownID`` -- str，上一个被点击Down的按钮的ID，如果没有取值为"-1"
        - ``TouchPosX`` -- float，按钮被点击时手指在屏幕上的坐标X值
        - ``TouchPosY`` -- float，按钮被点击时手指在屏幕上的坐标Y值
        - ``ButtonPath`` -- str，按钮路径
        - ``AddTouchEventParams`` -- dict，调用AddTouchEventParams接口时传入的参数字典
        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonHoverInCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置鼠标进入按钮时触发的悬浮回调函数。
        | 将鼠标移入添加了悬浮回调的控件中会触发该事件，该鼠标指 ``PushScreen`` 生成UI后显示的鼠标，F11生成的鼠标无法生效
        | 回调函数参数说明：
        - ``isHoverIn`` -- int，是否为进入悬浮回调，1为移入，0为移出
        - ``PrevButtonDownID`` -- str，上一个被点击Down的按钮的ID，如果没有取值为"-1"
        - ``TouchPosX`` -- float，鼠标进入按钮时在屏幕上的坐标X值
        - ``TouchPosY`` -- float，鼠标进入按钮时在屏幕上的坐标Y值
        - ``ButtonPath`` -- str，按钮路径
        - ``AddHoverEventParams`` -- dict，调用AddHoverEventParams接口时传入的参数字典

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonHoverOutCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置鼠标退出按钮时触发的悬浮回调函数。
        | 回调函数参数说明详见 ``SetButtonHoverInCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonTouchUpCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置触控在按钮范围内弹起时的回调函数。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonTouchCancelCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置触控在按钮范围外弹起时触发的回调函数。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonTouchMoveCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置按下后触控移动时触发的回调函数。
        | 该事件只在触屏模式下触发。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonTouchMoveInCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置按下按钮后进入控件时触发的回调函数。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonTouchMoveOutCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置按下按钮后退出控件时触发的回调函数。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
    def SetButtonScreenExitCallback(self, callback_func: Callable) -> None:
        """
        | 不推荐，建议使用 ``set_callback()`` 。

        -----

        | 设置按钮所在画布退出时若鼠标仍未抬起时触发回调函数。
        | 回调函数参数说明详见 ``SetButtonTouchDownCallback`` 。

        -----

        :param function callback_func: 回调函数，必须是UI的类函数

        :return: 无
        :rtype: None
        """
