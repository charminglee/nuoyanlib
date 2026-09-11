# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


import mod.client.extraClientApi as api
from ...core._utils import get_module
from ...core import _env
from ...core.client.comp import LvComp


if bool(0):
    from mod.client.ui.screenNode import ScreenNode
    from mod.client.system.clientSystem import ClientSystem
    from .nyc import NyControl
    from .screen_node import NyScreenNode, NyScreenProxy


__all__ = [
    "is_top_ui",
    "pop_to_hud",
    "create_ui",
    "push_ui",
    "get_children_path_by_level",
    "get_children_by_level",
    "get_parent_path",
    "get_parent",
]


def is_top_ui(screen_name):
    """
    判断UI界面是否在栈顶。

    示例
    ----

    >>> if nyl.is_top_ui("my_ui.main"):
    ...     nyl.pop_to_hud()

    参见
    ----

    - ``pop_to_hud()`` -- 弹出栈顶UI直到 HUD 界面。

    -----

    :param str screen_name: UI名称；对于原生UI，请使用 UICategory 枚举值；对于自定义UI，格式为 <namespace>.<name>

    :return: 是否在栈顶
    :rtype: bool
    """
    if api.GetTopUI() == screen_name:
        return True
    top_screen = api.GetTopScreen()
    return top_screen and top_screen.full_name == screen_name


def pop_to_hud():
    """
    依次弹出栈顶UI直到 HUD 界面。

    示例
    ----

    >>> if nyl.is_top_ui("my_ui.main"):
    ...     nyl.pop_to_hud()

    参见
    ----

    - ``is_top_ui()`` -- 判断指定UI界面是否在栈顶。
    - ``NyScreenBase.hide()`` -- 隐藏UI界面。

    -----

    :return: 无
    :rtype: None
    """
    top = api.GetTopUI()
    while top and top != "hud_screen":
        api.PopTopUI()
        top = api.GetTopUI()


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
    TOOLTIP_TRIGGER = 23
    COMBOX = 24
    LAYOUT = 25
    STACK_GRID = 26
    JOYSTICK = 27
    RICH_TEXT = 28
    SIXTEEN_NINE_LAYOUT = 29
    MUL_LINES_EDIT = 30
    AMIN_PROCESS_BAR = 31
    UNKNOWN = 32
    NETEASE_PAPER_DOLL = 33 # = CUSTOM
    ITEM_RENDERER = 34      # = CUSTOM
    PROGRESS_BAR = 35       # = PANEL
    COMBO_BOX = 36          # = PANEL
    MINI_MAP = 37           # = CUSTOM


def create_ui(namespace, ui_key, cls_path, screen_def="", param=None, client_system=None):
    """
    [已废弃]

    创建UI界面。

    说明
    ----

    使用此函数创建的UI无需调用 ``RegisterUI()`` 接口进行注册。

    -----

    :param str namespace: 命名空间，建议为 mod 名字
    :param str ui_key: UI唯一标识，一般为 UI json 中 "namespace" 字段的值
    :param str cls_path: UI类路径
    :param str screen_def: UI画布路径，格式为 "<namespace>.<screen_name>"，<namespace> 为 UI json 中 "namespace" 字段的值，<screen_name> 为想要创建的画布名称；默认为 "<ui_key>.main"
    :param dict|None param: UI参数字典；默认为 {'isHud': 1}
    :param ClientSystem|None client_system: 客户端类实例；默认为 None；若指定，可在UI类中通过 param 字典的 '__cs__' 键获取该实例

    :return: UI类实例，创建失败时返回 None
    :rtype: ScreenNode|None
    """
    if not screen_def:
        screen_def = ui_key + ".main"
    if param is None:
        param = {'isHud': 1}
    param['__cs__'] = client_system
    if not _is_ui_registered(namespace, ui_key):
        api.RegisterUI(namespace, ui_key, cls_path, screen_def)
    node = api.CreateUI(namespace, ui_key, param)
    return node


def push_ui(namespace, ui_key, cls_path, screen_def="", param=None, client_system=None):
    """
    [已废弃]

    通过堆栈管理（Push）的方式创建UI界面。

    说明
    ----

    使用此函数创建的UI无需调用 ``RegisterUI()`` 接口进行注册。

    -----

    :param str namespace: 命名空间，建议为 mod 名字
    :param str ui_key: UI唯一标识，一般为 UI json 中 "namespace" 字段的值
    :param str cls_path: UI类路径
    :param str screen_def: UI画布路径，格式为 "<namespace>.<screen_name>"，<namespace> 为 UI json 中 "namespace" 字段的值，<screen_name> 为想要创建的画布名称；默认为 "<ui_key>.main"
    :param dict|None param: UI参数字典；默认为空字典
    :param ClientSystem|None client_system: 客户端类实例；默认为 None；若指定，可在UI类中通过 param 字典的 '__cs__' 键获取该实例

    :return: UI类实例，创建失败时返回 None
    :rtype: ScreenNode|None
    """
    if not screen_def:
        screen_def = ui_key + ".main"
    if param is None:
        param = {}
    param['__cs__'] = client_system
    if not _is_ui_registered(namespace, ui_key):
        api.RegisterUI(namespace, ui_key, cls_path, screen_def)
    node = api.PushScreen(namespace, ui_key, param)
    return node


def _to_path(control):
    return control if isinstance(control, str) else control.GetPath()


def is_out_of_screen(control, ny_screen_node=None):
    """
    判断控件是否超出屏幕范围。

    示例
    ----

    >>> if nyl.is_out_of_screen(button):
    ...     button.visible = False

    -----

    :param str|NyControl control: 控件路径或实例
    :param NyScreenNode|NyScreenProxy|None ny_screen_node: 当 control 参数传入控件路径时，需要指定控件所在UI类的实例；默认为 None

    :return: 是否超出屏幕范围
    :rtype: bool
    """
    if isinstance(control, str):
        if ny_screen_node is None:
            raise ValueError("parameter 'ny_screen_node' not specified")
        from .nyc import NyControl
        control = NyControl(ny_screen_node, control)
    px, py = control.global_position
    ctrl_sx, ctrl_sy = control.size
    scr_sx, scr_sy = LvComp.Game.GetScreenSize()
    return (
        px < 0
        or py < 0
        or px + ctrl_sx > scr_sx
        or py + ctrl_sy > scr_sy
    )


def get_children_path_by_level(control, ny_screen_node, level=1):
    """
    获取控件指定层次上的子控件的路径。

    说明
    ----

    此处的“层次”指的是子控件层次，而非渲染层级（layer），详见示例。

    示例
    ----

    假设有以下控件结构：
    ::

        panel
        ├─ button1
        │  ├─ default
        │  ├─ pressed
        │  ├─ hover
        │  └─ button_label
        └─ button2
           ├─ default
           ├─ pressed
           ├─ hover
           └─ button_label

    >>> nyl.get_children_path_by_level("/panel", ny_screen_node, 1)
    ['/panel/button1', '/panel/button2']

    >>> nyl.get_children_path_by_level("/panel", ny_screen_node, 2)
    ['/panel/button1/default', '/panel/button1/pressed', '/panel/button1/hover', '/panel/button1/button_label',
     '/panel/button2/default', '/panel/button2/pressed', '/panel/button2/hover', '/panel/button2/button_label']

    >>> nyl.get_children_path_by_level("/panel/button1", ny_screen_node, 1)
    ['/panel/button1/default', '/panel/button1/pressed', '/panel/button1/hover', '/panel/button1/button_label']

    参见
    ----

    - ``get_children_by_level()`` -- 获取指定层次上的子控件实例。

    -----

    :param str|NyControl control: 控件路径或实例
    :param NyScreenNode|NyScreenProxy ny_screen_node: 控件所在UI类的实例
    :param int level: 子控件层次；默认为 1，传入 0 或负值时，获取所有层次的子控件

    :return: 指定层次的所有子控件路径的列表，获取不到时返回空列表
    :rtype: list[str]
    """
    path = _to_path(control)
    screen_node = ny_screen_node._screen_node
    if level == 1:
        return [
            path + "/" + n
            for n in screen_node.GetChildrenName(path)
        ]
    elif level <= 0:
        return screen_node.GetAllChildrenPath(path) or []
    else:
        res = []
        control_level = path.count("/")
        if not path.startswith("/"):
            control_level += 1
        target_level = control_level + level
        for p in screen_node.GetAllChildrenPath(path):
            if p.startswith("/safezone_screen_matrix"):
                # 在base_screen中，接口获取的子控件路径会错误地丢失/variables_button_mappings_and_controls
                p = "/variables_button_mappings_and_controls" + p
            this_level = p.count("/")
            if this_level == target_level:
                res.append(p)
        return res


def get_children_by_level(control, ny_screen_node, level=1):
    """
    获取控件指定层次上的子控件的 ``NyControl`` 实例。

    说明
    ----

    此处的“层次”指的是子控件层次，而非渲染层级（layer），详见 ``get_children_path_by_level()`` 。

    示例
    ----

    >>> buttons = nyl.get_children_by_level("/panel", ny_screen_node, 1)
    >>> for button in buttons:
    ...     button.visible = True

    参见
    ----

    - ``get_children_path_by_level()`` -- 获取指定层次上的子控件路径。

    -----

    :param str|NyControl control: 控件路径或实例
    :param NyScreenNode|NyScreenProxy ny_screen_node: 控件所在UI类的实例
    :param int level: 子控件层次；默认为 1，传入 0 或负值时，获取所有层次

    :return: 指定层次上的子控件实例的列表，获取不到时返回空列表
    :rtype: list[NyControl]
    """
    from .nyc import NyControl
    return [
        NyControl(ny_screen_node, p)
        for p in get_children_path_by_level(control, ny_screen_node, level)
    ]


def get_parent_path(control):
    """
    获取父控件路径。

    示例
    ----

    >>> nyl.get_parent_path("/panel/button")
    '/panel'

    参见
    ----

    - ``get_parent()`` -- 获取父控件实例。

    -----

    :param str|NyControl control: 控件路径或实例

    :return: 父控件路径，获取不到返回 None
    :rtype: str|None
    """
    path = _to_path(control)
    return path[:path.rindex("/")] if path else None


def get_parent(control, ny_screen_node):
    """
    获取父控件的 ``NyControl`` 实例。

    示例
    ----

    >>> panel = nyl.get_parent(button, ny_screen_node)
    >>> panel.visible = True

    参见
    ----

    - ``get_parent_path()`` -- 获取父控件路径。

    -----

    :param str|NyControl control: 控件路径或实例
    :param NyScreenNode|NyScreenProxy ny_screen_node: 控件所在UI类的实例

    :return: 父控件实例，获取不到返回 None
    :rtype: NyControl|None
    """
    from .nyc import NyControl
    parent_path = get_parent_path(control)
    if parent_path is None:
        return
    return NyControl(ny_screen_node, parent_path)


def _is_ui_registered(ui_key):
    mgr = get_module(99, 108, 105, 101, 110, 116, 46, 117, 105, 46, 117, 105, 77, 97, 110, 97, 103, 101, 114)
    if not mgr:
        return False
    key = _env.MOD_NAME + ":" + ui_key
    try:
        return key in mgr.instance().screen_def
    except (TypeError, AttributeError):
        return False
