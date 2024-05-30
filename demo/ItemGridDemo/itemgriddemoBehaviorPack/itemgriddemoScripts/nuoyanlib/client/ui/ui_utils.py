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
#   Last Modified : 2024-05-31
#
# ====================================================


from ..._core._client._comp import ScreenNode as _ScreenNode


__all__ = [
    "get_parent_path",
    "get_direct_children_path",
    "get_parent_control",
]


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






















