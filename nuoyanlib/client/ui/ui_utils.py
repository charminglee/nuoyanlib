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


from functools import wraps as _wraps
from ..._core._client._comp import (
    ScreenNode as _ScreenNode,
    LvComp as _LvComp,
)
from ...utils import Enum as _Enum
from ..._core._client import _lib_client
from .. import setting as _setting


__all__ = [
    "ControlType",
    "to_path",
    "to_control",
    "ButtonCallback",
    "get_parent_path",
    "get_all_children_path_by_level",
    "get_all_children_control_by_level",
    "get_parent_control",
    "notify_server",
]


class ControlType(_Enum[str]):
    """
    | UI控件类型枚举。
    """

    base_control = "BaseControl"
    """
    | 通用控件。
    """

    button = "Button"
    """
    | 按钮。
    """

    image = "Image"
    """
    | 图片。
    """

    label = "Label"
    """
    | 文本。
    """

    panel = "Panel"
    """
    | 面板。
    """

    input_panel = "InputPanel"
    """
    | 输入面板。
    """

    stack_panel = "StackPanel"
    """
    | 栈面板。
    """

    edit_box = "TextEditBox"
    """
    | 文本编辑框。
    """

    paper_doll = "PaperDoll"
    """
    | 纸娃娃。
    """

    netease_paper_doll = "NeteasePaperDoll"
    """
    | 网易纸娃娃。
    """

    item_renderer = "ItemRenderer"
    """
    | 物品渲染器。
    """

    gradient_renderer = "GradientRenderer"
    """
    | 渐变渲染器。
    """

    scroll_view = "ScrollView"
    """
    | 滚动视图。
    """

    grid = "Grid"
    """
    | 网格。
    """

    progress_bar = "ProgressBar"
    """
    | 进度条。
    """

    toggle = "SwitchToggle"
    """
    | 开关。
    """

    slider = "Slider"
    """
    | 滑动条。
    """

    selection_wheel = "SelectionWheel"
    """
    | 轮盘。
    """

    combo_box = "NeteaseComboBox"
    """
    | 下拉框。
    """

    mini_map = "MiniMap"
    """
    | 小地图。
    """

    _not_special = (base_control, panel, paper_doll, gradient_renderer)


def to_path(control):
    """
    | 获取控件路径，若传入的已经是路径，则返回其本身。

    -----

    :param str|BaseUIControl control: 控件实例

    :return: 控件路径
    :rtype: str
    """
    return control if isinstance(control, str) else control.GetPath()


def to_control(screen_node, path, control_type=ControlType.base_control):
    """
    | 根据路径获取控件实例，若传入的已经是实例，则返回其本身。

    -----

    :param _ScreenNode screen_node: 控件所在UI类的实例
    :param str|BaseUIControl path: 控件路径
    :param str control_type: 控件类型，请使用ControlType枚举值，默认为ControlType.base_control

    :return: 控件实例，获取不到时返回None
    :rtype: BaseUIControl|None
    """
    control = screen_node.GetBaseUIControl(path) if isinstance(path, str) else path
    if control and control_type not in ControlType._not_special:
        control = getattr(control, "as" + control_type)()
    return control


def save_ui_pos_data(key, data):
    return _setting.save_setting(key, data, False)


def get_ui_pos_data(key):
    data = _setting.read_setting(key, False)
    if data:
        for key, data_lst in data.items():
            data_lst = [(str(path), tuple(pos)) for path, pos in data_lst]
            data[key] = data_lst
    return data or {}


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
    path = to_path(control)
    if level == 1:
        res = [
            path + "/" + n
            for n in screen_node.GetChildrenName(path)
        ]
    else:
        res = []
        control_level = path.count("/")
        if not path.startswith("/"):
            control_level += 1
        target_level = control_level + level
        for p in screen_node.GetAllChildrenPath(path):
            if p.startswith("/safezone_screen_matrix"):
                p = "/variables_button_mappings_and_controls" + p
            if p.count("/") == target_level:
                res.append(p)
    return res


def get_all_children_control_by_level(control, screen_node, level=1):
    """
    | 获取控件的指定层级的所有子控件的实例。
    | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

    -----

    :param str|BaseUIControl control: 控件路径或实例
    :param _ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层级，默认为1

    :return: 控件指定层级的所有子控件的实例列表，获取不到时返回空列表
    :rtype: list[BaseUIControl]
    """
    return [
        to_control(screen_node, p)
        for p in get_all_children_path_by_level(control, screen_node, level)
    ]


def get_parent_path(control):
    """
    | 获取控件的父控件路径。

    -----

    :param str|BaseUIControl control: 控件路径或实例

    :return: 父控件路径，获取不到返回None
    :rtype: str|None
    """
    path = to_path(control)
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
    [已废弃] [装饰器]

    | 用于按钮的回调函数，被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
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

















