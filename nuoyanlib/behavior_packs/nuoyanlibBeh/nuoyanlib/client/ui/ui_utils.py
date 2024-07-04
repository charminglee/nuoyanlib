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
#   Last Modified : 2024-07-03
#
# ====================================================


from behavior_packs.nuoyanlibBeh.nuoyanlibScripts._core._client import (
    get_lib_system as _get_lib_system,
)


__all__ = [
    "register_item_grid",
    "get_parent_path",
    "get_direct_children_path",
    "get_parent_control",
]


def register_item_grid(key, ui_cls_path, grid_path, grid_size=1, is_single=False):
    """
    | 注册物品网格或注册单个方格按钮。如果注册的是单个方格按钮，则该方格按钮将被视为只有一个元素的网格。
    | 注册后还需要在网格显示在屏幕上时调用 ``ItemGridManager`` 的 ``InitItemGrids`` 接口才能正常使用。
    | 当网格的key以“_shortcut”、“_inv27”或“_inv36”结尾时（如“my_item_grid_inv36”），将获得以下特殊功能：
    * 该网格将与本地玩家的背包进行绑定，"_shortcut"表示快捷栏，"_inv27"表示除快捷栏以外的物品栏，"_inv36"表示整个物品栏。
    * 该网格会自动获取本地玩家背包物品数据，并显示物品。
    * 在该网格进行的任何物品操作会自动与本地玩家的背包进行同步。
    | key以“_shortcut”、“_inv27”或“_inv36”结尾的网格的方格数量分别为9、27、36时才能注册成功。

    -----

    :param str key: 网格的key，请保证key唯一，不能与其他网格相同，建议格式为“模组名+网格名称”
    :param str ui_cls_path: 网格所在UI类的路径（该UI类需要继承ItemGridManager）
    :param str grid_path: 网格的UI路径
    :param int grid_size: 网格的方格数量，默认为1
    :param bool is_single: 是否是单个方格按钮，默认为False

    :return: 是否注册成功
    :rtype: bool
    """
    lib_sys = _get_lib_system()
    if not lib_sys:
        return False
    return lib_sys.register_item_grid(key, ui_cls_path, grid_path, grid_size, is_single)


def _get_path(control):
    return control if isinstance(control, str) else control.GetPath()


def get_direct_children_path(control, ui_ins):
    """
    | 获取控件的所有直接子控件的路径。
    | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的直接子控件，图片为面板的间接子控件。

    -----

    :param str|BaseUIControl control: 控件路径或控件实例
    :param _ScreenNode ui_ins: 控件所在的UI类实例

    :return: 控件所有直接子控件的路径的列表，获取不到返回空列表
    :rtype: list[str]
    """
    path = _get_path(control)
    if not path.startswith("/"):
        path = "/" + path
    path_level = path.count("/")
    path_first = path if path_level == 1 else path[:path.index("/", 1)]
    all_children = []
    for p in ui_ins.GetAllChildrenPath(path):
        p_first = p[:p.index("/", 1)]
        if p_first != path_first:
            p = path_first + p
        p_level = p.count("/")
        if p_level == path_level + 1:
            all_children.append(p)
    return all_children


def get_parent_path(control):
    """
    | 获取控件的父控件路径。

    -----

    :param str|BaseUIControl control: 控件路径或控件实例

    :return: 父控件路径，获取不到返回None
    :rtype: str|None
    """
    path = _get_path(control)
    return path[:path.rindex("/")] if path else None


def get_parent_control(control, ui_ins):
    """
    | 获取控件的父控件实例。

    -----

    :param str|BaseUIControl control: 控件路径或控件实例
    :param _ScreenNode ui_ins: 控件所在的UI类实例

    :return: 父控件实例（BaseUIControl），获取不到返回None
    :rtype: BaseUIControl|None
    """
    path = get_parent_path(control)
    return ui_ins.GetBaseUIControl(path) if path else None






















