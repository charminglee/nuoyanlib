# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-11-05
|
| ==============================================
"""


from types import GeneratorType
from functools import wraps
import mod.client.extraClientApi as client_api
from mod.client.system.clientSystem import ClientSystem
from ..._core._client.comp import ScreenNode, LvComp
from ..._core._client import _lib_client
from ..setting import read_setting, save_setting
from ...utils.enum import ControlType


__all__ = [
    "create_ui",
    "to_path",
    "to_control",
    "iter_children_path_by_level",
    "iter_children_by_level",
    "get_parent_path",
    "get_parent",
    "notify_server",
]


def create_ui(namespace, ui_key, cls_path, screen_def="", register=True, param=None, push=False, client_system=None):
    """
    | 创建UI界面。

    -----

    :param str namespace: 命名空间，建议为mod名字
    :param str ui_key: UI唯一标识，建议为UI json中的"namespace"的值
    :param str cls_path: UI类路径
    :param str screen_def: UI画布路径，格式为"<namespace>.<screen_name>"，<namespace>为UI json中"namespace"的值，<screen_name>为想要创建的画布名称；默认为"<ui_key>.main"
    :param bool register: 创建前是否注册UI，默认为True
    :param dict|None param: UI参数字典；不通过堆栈管理的方式创建UI时，该参数默认为{'isHud': 1}
    :param bool push: 是否通过堆栈管理（PushScreen）的方式创建UI，默认为False
    :param ClientSystem|None client_system: 客户端类实例，默认为None；若指定，可在UI类中通过param字典的 '__cs__' 键获取到该实例

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
        client_api.RegisterUI(namespace, ui_key, cls_path, screen_def)
    if push:
        node = client_api.PushScreen(namespace, ui_key, cls_path)
    else:
        node = client_api.CreateUI(namespace, ui_key, param)
    return node


def to_path(control):
    """
    | 获取控件路径，若传入的已经是路径，则返回其本身。

    -----

    :param str|BaseUIControl control: 控件实例

    :return: 控件路径
    :rtype: str
    """
    return control if isinstance(control, str) else control.GetPath()


def to_control(screen_node, path, control_type=ControlType.BASE_CONTROL):
    """
    | 根据路径获取控件实例，若传入的已经是实例，则返回其本身。

    -----

    :param ScreenNode screen_node: 控件所在UI类的实例
    :param str|BaseUIControl path: 控件路径
    :param str control_type: 控件类型，返回该类型对应的实例，请使用ControlType枚举值，默认为ControlType.base_control

    :return: 控件实例，获取不到时返回None
    :rtype: BaseUIControl|None
    """
    control = screen_node.GetBaseUIControl(path) if isinstance(path, str) else path
    if control and control_type not in ControlType._NOT_SPECIAL:
        control = getattr(control, "as" + control_type)()
    return control


def save_ui_pos_data(key, data):
    return save_setting(key, data, False)


def get_ui_pos_data(key):
    data = read_setting(key, False)
    if data:
        for key, data_lst in data.items():
            data_lst = [(str(path), tuple(pos)) for path, pos in data_lst]
            data[key] = data_lst
    return data or {}


def is_ui_out_of_screen(control, screen_node=None):
    """
    | 判断控件是否超出屏幕范围。

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


def iter_children_path_by_level(control, screen_node, level=1):
    """
    [迭代器]

    | 获取控件指定层次的所有子控件的路径，返回迭代器。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层次，默认为1，传入0或负值时，获取所有层次

    :return: 指定层次的所有子控件路径的迭代器，获取不到时返回空迭代器
    :rtype: GeneratorType
    """
    path = to_path(control)
    if level == 1:
        for n in screen_node.GetChildrenName(path):
            yield path + "/" + n
    else:
        control_level = path.count("/")
        if not path.startswith("/"):
            control_level += 1
        target_level = control_level + level
        for p in screen_node.GetAllChildrenPath(path):
            if p.startswith("/safezone_screen_matrix"):
                p = "/variables_button_mappings_and_controls" + p
            if level <= 0 or p.count("/") == target_level:
                yield p


def iter_children_by_level(control, screen_node, level=1):
    """
    [迭代器]

    | 获取控件指定层次的所有子控件的 ``BaseUIControl`` 实例，返回迭代器。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例
    :param int level: 子控件层次，默认为1，传入0或负值时，获取所有层次

    :return: 指定层次的所有子控件实例的迭代器，获取不到时返回空迭代器
    :rtype: GeneratorType
    """
    for p in iter_children_path_by_level(control, screen_node, level):
        yield to_control(screen_node, p)


def get_parent_path(control):
    """
    | 获取控件的父控件路径。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例

    :return: 父控件路径，获取不到返回None
    :rtype: str|None
    """
    path = to_path(control)
    return path[:path.rindex("/")] if path else None


def get_parent(control, screen_node):
    """
    | 获取控件的父控件 ``BaseUIControl`` 实例。

    -----

    :param str|BaseUIControl|NyControl control: 控件路径或实例
    :param ScreenNode screen_node: 控件所在UI类的实例

    :return: 父控件实例，获取不到返回None
    :rtype: BaseUIControl|None
    """
    return screen_node.GetBaseUIControl(get_parent_path(control))


def notify_server(func):
    """
    [装饰器]

    | 用于按钮的回调函数，被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
    | 服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为 ``__id__`` 的key，其value为触发按钮的玩家实体ID。
    | 可通过 args['cancel_notify'] = True 或 return -1 的方式取消触发服务端函数。
    | 若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数字典同样为修改后的字典，可通过该方式向服务端传递更多信息。

    -----

    :return: 返回wrapper函数
    :rtype: function
    """
    @wraps(func)
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







