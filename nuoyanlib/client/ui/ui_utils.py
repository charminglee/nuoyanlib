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
#   Last Modified : 2024-04-28
#
# ====================================================


from ..comp import ScreenNode as _ScreenNode


__all__ = [
    "get_parent_path",
    "get_direct_children_path",
]


def get_direct_children_path(path, ui_self):
    """
    | 获取网格的所有直接子控件的路径。例如，一个网格包含两个按钮，而每个按钮又包含三张图片，则按钮为网格的直接子控件，图片为网格的间接子控件。

    -----

    :param str path: 网格路径
    :param _ScreenNode ui_self: UI类实例，在UI类里调用该函数直接传self即可

    :return: 网格的所有直接子控件的路径，获取不到返回空列表
    :rtype: list[str]
    """
    if not path.startswith("/"):
        path = "/" + path
    gp_level = path.count("/")
    all_children = []
    for p in ui_self.GetAllChildrenPath(path):
        if p.startswith("/safezone_screen_matrix"):
            p = "/variables_button_mappings_and_controls" + p
        if p.count("/") == gp_level + 1:
            all_children.append(p)
    return all_children


def get_parent_path(path):
    """
    | 根据控件路径获取父控件路径。

    -----

    :param str path: 控件路径

    :return: 父控件路径
    :rtype: str
    """
    return "/".join(path.split("/")[:-1])






















