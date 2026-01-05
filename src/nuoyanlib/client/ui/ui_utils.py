# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-4
#  ⠀
# =================================================


if 0:
    from mod.client.ui.screenNode import ScreenNode
    from mod.client.system.clientSystem import ClientSystem
    from .nyc import NyControl


import mod.client.extraClientApi as c_api
from ...core.client.comp import LvComp
from ...utils.enum import ControlType


__all__ = [
    "pop_to_hud",
    "create_ui",
    "to_path",
    "to_control",
    "get_children_path_by_level",
    "get_children_by_level",
    "get_parent_path",
    "get_parent",
]


def pop_to_hud():
    """
    依次弹出栈顶UI直到HUD界面。

    -----

    :return: 无
    :rtype: None
    """
    while not c_api.GetTopUI() != "hud_screen":
        c_api.PopTopUI()


class _UIControlType:
    ALL = -1
    BUTTON = 0
    CUSTOM = 1
    COLLECTION_PANEL = 2
    DROPDOWN = 3
    EDIT_BOX = 4
    FACTORY = 5
    GRID = 6
    IMAGE = 7
    INPUT_PANEL = 8
    LABEL = 9
    PANEL = 10
    SCREEN = 11
    SCROLLBAR_BOX = 12
    SCROLL_TRACK = 13
    SCROLL_VIEW = 14
    SELECTION_WHEEL = 15
    SLIDER = 16
    SLIDER_BOX = 17
    STACK_PANEL = 18
    TOGGLE = 19
    IMAGE_CYCLER = 20
    LABEL_CYCLER = 21
    GRID_PAGE_INDICATOR = 22
    COMBOX = 23
    LAYOUT = 24
    STACK_GRID = 25
    JOYSTICK = 26
    RICH_TEXT = 27
    SIXTEEN_NINE_LAYOUT = 28
    MUL_LINES_EDIT = 29
    AMIN_PROCESS_BAR = 30
    UNKNOWN = 31


def create_ui(namespace, ui_key, cls_path, screen_def="", register=True, param=None, push=False, client_system=None):
    """
    创建UI界面。

    -----

    :param str namespace: 命名空间，建议为mod名字
    :param str ui_key: UI唯一标识，建议为UI json中的"namespace"的值
    :param str cls_path: UI类路径
    :param str screen_def: UI画布路径，格式为"<namespace>.<screen_name>"，<namespace>为UI json中"namespace"的值，<screen_name>为想要创建的画布名称；默认为"<ui_key>.main"
    :param bool register: 创建前是否注册UI；默认为True
    :param dict|None param: UI参数字典；不通过堆栈管理的方式创建UI时，该参数默认为{'isHud': 1}
    :param bool push: 是否通过堆栈管理（PushScreen）的方式创建UI；默认为False
    :param ClientSystem|None client_system: 客户端类实例；默认为None；若指定，可在UI类中通过param字典的 '__cs__' 键获取到该实例

    :return: UI类实例，创建失败时返回None
    :rtype: ScreenNode|None
    """
    if not screen_def:
        screen_def = ui_key + ".main"
    if param is None:
        param = {}
    if not push and 'isHud' not in param:
        param['isHud'] = 1
    param['__cs__'] = client_system
    if register:
        c_api.RegisterUI(namespace, ui_key, cls_path, screen_def)
    if push:
        node = c_api.PushScreen(namespace, ui_key, param)
    else:
        node = c_api.CreateUI(namespace, ui_key, param)
    return node


def to_path(control):
    """
    获取控件路径。

    若传入的已经是路径，则返回其本身。

    -----

    :param str|BaseUIControl control: 控件实例

    :return: 控件路径
    :rtype: str
    """
    return control if isinstance(control, str) else control.GetPath()


def to_control(screen_node, path, control_type=ControlType.BASE_CONTROL):
    """
    根据路径获取控件实例。

    若传入的已经是实例，则返回其本身。

    -----

    :param ScreenNode screen_node: 控件所在UI类的实例
    :param str|BaseUIControl path: 控件路径
    :param ControlType control_type: 控件类型，返回该类型对应的实例，请使用ControlType枚举值；默认为ControlType.BASE_CONTROL

    :return: 控件实例，获取不到时返回None
    :rtype: BaseUIControl|None
    """
    control = screen_node.GetBaseUIControl(path) if isinstance(path, str) else path
    if control and control_type not in ControlType._AS_BASE:
        control = getattr(control, "as" + control_type)()
    return control


def is_out_of_screen(control, screen_node=None):
    """
    判断控件是否超出屏幕范围。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode|None screen_node: 当control参数传入控件路径时，需要指定控件所在UI类的实例；默认为None

    :return: 是否超出屏幕范围
    :rtype: bool
    """
    if isinstance(control, str):
        control = screen_node.GetBaseUIControl(control)
    px, py = control.GetGlobalPosition()
    ctrl_sx, ctrl_sy = control.GetSize()
    scr_sx, scr_sy = LvComp.Game.GetScreenSize()
    return (
        px < 0
        or py < 0
        or px + ctrl_sx > scr_sx
        or py + ctrl_sy > scr_sy
    )


def get_children_path_by_level(control, screen_node, level=1):
    """
    获取控件指定层次的所有子控件的路径。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层次；默认为1，传入0或负值时，获取所有层次

    :return: 指定层次的所有子控件路径的列表，获取不到时返回空列表
    :rtype: list[str]
    """
    path = to_path(control)
    if level == 1:
        return [
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
            if level <= 0 or p.count("/") == target_level:
                res.append(p)
        return res


def get_children_by_level(control, screen_node, level=1):
    """
    获取控件指定层次的所有子控件的 ``BaseUIControl`` 实例。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层次；默认为1，传入0或负值时，获取所有层次

    :return: 指定层次的所有子控件实例的列表，获取不到时返回空列表
    :rtype: list[BaseUIControl]
    """
    return [
        to_control(screen_node, p)
        for p in get_children_path_by_level(control, screen_node, level)
    ]


def get_parent_path(control):
    """
    获取父控件路径。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例

    :return: 父控件路径，获取不到返回None
    :rtype: str|None
    """
    path = to_path(control)
    return path[:path.rindex("/")] if path else None


def get_parent(control, screen_node):
    """
    获取父控件的 ``BaseUIControl`` 实例。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例

    :return: 父控件实例，获取不到返回None
    :rtype: BaseUIControl|None
    """
    return screen_node.GetBaseUIControl(get_parent_path(control))
