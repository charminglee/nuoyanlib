# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-28
#
# ====================================================


from functools import wraps as _wraps
from ..._core._client._comp import (
    ScreenNode as _ScreenNode,
    LvComp as _LvComp,
)
from ...utils import Enum as _Enum
from ..._core._client import _lib_client
from .. import setting as _setting


__all__ = [
    "to_button",
    "to_path",
    "to_control",
    "ButtonCallback",
    "get_parent_path",
    "get_all_children_path_by_level",
    "get_parent_control",
    "notify_server",
]


def to_button(screen_node, control):
    """
    | 获取按钮的 ``ButtonUIControl`` 实例。

    -----

    :param _ScreenNode screen_node: 控件所在UI类的实例
    :param str|BaseUIControl control: 控件路径或实例

    :return: ButtonUIControl实例，获取不到时返回None
    :rtype: ButtonUIControl|None
    """
    control = to_control(screen_node, control)
    return control.asButton() if control else None


def to_path(control):
    """
    | 获取控件路径，若传入的已经是路径，则返回该路径。

    -----

    :param str|BaseUIControl control: 控件实例

    :return: 控件路径
    :rtype: str
    """
    return control if isinstance(control, str) else control.GetPath()


def to_control(screen_node, path):
    """
    | 根据路径获取控件的 ``BaseUIControl`` 实例，若传入的已经是实例，则返回该实例。

    -----

    :param _ScreenNode screen_node: 控件所在UI类的实例
    :param str|BaseUIControl path: 控件路径

    :return: 控件实例，获取不到时返回None
    :rtype: BaseUIControl|None
    """
    return screen_node.GetBaseUIControl(path) if isinstance(path, str) else path


def save_ui_pos_data(key, data):
    return _setting.save_setting(key, data, False)


def get_ui_pos_data(key):
    data = _setting.read_setting(key, False)
    if data:
        for key, data_lst in data.items():
            data_lst = [(str(path), tuple(pos)) for path, pos in data_lst]
            data[key] = data_lst
    return data or {}


class UIControlType:
    All = -1
    Button = 0
    Custom = 1
    CollectionPanel = 2
    Dropdown = 3
    EditBox = 4
    Factory = 5
    Grid = 6
    Image = 7
    InputPanel = 8
    Label = 9
    Panel = 10
    Screen = 11
    ScrollbarBox = 12
    ScrollTrack = 13
    ScrollView = 14
    SelectionWheel = 15
    Slider = 16
    SliderBox = 17
    StackPanel = 18
    Toggle = 19
    ImageCycler = 20
    LabelCycler = 21
    GridPageIndicator = 22
    Combox = 23
    Layout = 24
    StackGrid = 25
    Joystick = 26
    RichText = 27
    SixteenNineLayout = 28
    MulLinesEdit = 29
    AminProcessBar = 30
    Unknown = 31


class ButtonCallback(_Enum[int]):
    """
    按钮回调函数类型枚举。
    """

    touch_up = _Enum.auto()
    """
    触控在按钮范围内抬起。
    """

    touch_down = _Enum.auto()
    """
    按钮按下。
    """

    touch_cancel = _Enum.auto()
    """
    触控在按钮范围外抬起。
    """

    touch_move = _Enum.auto()
    """
    按下后触控移动。
    """

    touch_move_in = _Enum.auto()
    """
    按下按钮后触控进入按钮。
    """

    touch_move_out = _Enum.auto()
    """
    按下按钮后触控退出按钮。
    """

    double_click = _Enum.auto()
    """
    双击按钮。
    """

    long_click = _Enum.auto()
    """
    长按按钮。
    """

    hover_in = _Enum.auto()
    """
    鼠标进入按钮。
    """

    hover_out = _Enum.auto()
    """
    鼠标退出按钮。
    """

    screen_exit = _Enum.auto()
    """
    按钮所在画布退出，且鼠标仍未抬起时触发。
    """


def is_ui_out_of_screen(control, screen_node=None):
    """
    | 判断控件是否超出屏幕范围。

    -----

    :param str|BaseUIControl control: 控件路径或实例
    :param _ScreenNode|None screen_node: 当control参数传入控件路径时，需要指定控件所在UI类的实例；默认为None

    :return: 是否超出屏幕范围
    :rtype: bool
    """
    if isinstance(control, str):
        control = screen_node.GetBaseUIControl(control)
    px, py = control.GetGlobalPosition()
    ctrl_sx, ctrl_sy = control.GetSize()
    scr_sx, scr_sy = _LvComp.Game.GetScreenSize()
    return (
        px < 0
        or py < 0
        or px + ctrl_sx > scr_sx
        or py + ctrl_sy > scr_sy
    )


def _get_path(control):
    return control if isinstance(control, str) else control.GetPath()


def get_all_children_path_by_level(control, screen_node, level=1):
    """
    | 获取控件的指定层级的所有子控件的路径。
    | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

    -----

    :param str|BaseUIControl control: 控件路径或实例
    :param _ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层级，默认为1

    :return: 控件指定层级的所有子控件的路径列表，获取不到时返回空列表
    :rtype: list[str]
    """
    path = _get_path(control)
    control_level = path.count("/")
    if not path.startswith("/"):
        control_level += 1
    target_level = control_level + level
    res = []
    for p in screen_node.GetAllChildrenPath(path):
        if p.startswith("/safezone_screen_matrix"):
            p = "/variables_button_mappings_and_controls" + p
        if p.count("/") == target_level:
            res.append(p)
    return res


def get_parent_path(control):
    """
    | 获取控件的父控件路径。

    -----

    :param str|BaseUIControl control: 控件路径或实例

    :return: 父控件路径，获取不到返回None
    :rtype: str|None
    """
    path = _get_path(control)
    return path[:path.rindex("/")] if path else None


def get_parent_control(control, screen_node):
    """
    | 获取控件的父控件实例。

    -----

    :param str|BaseUIControl control: 控件路径或实例
    :param _ScreenNode screen_node: 控件所在UI类的实例

    :return: 父控件实例（BaseUIControl），获取不到返回None
    :rtype: BaseUIControl|None
    """
    return screen_node.GetBaseUIControl(get_parent_path(control))


def notify_server(func):
    """
    【已废弃】

    | 函数装饰器，用于按钮的回调函数。
    | 被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
    | 服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为 ``__id__`` 的key，其value为触发按钮的玩家实体ID。
    | 可通过 args['cancel_notify'] = True 或 return -1 的方式取消触发服务端函数。
    | 若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数字典同样为修改后的字典，可通过该方式向服务端传递更多信息。
    """
    @_wraps(func)
    def wrapper(self, args):
        args['cancel_notify'] = False
        ret = func(self, args)
        if args['cancel_notify'] or ret == -1:
            return ret
        del args['cancel_notify']
        _lib_client.instance().NotifyToServer(
            "_ButtonCallbackTrigger",
            {'name': func.__name__, 'args': args}
        )
        return ret
    return wrapper

















