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
#   Last Modified : 2023-11-26
#
# ====================================================


"""

setting
=======

该模块提供了与自定义设置有关的工具。

"""


from comp import LvComp as _LvComp


__all__ = [
    "save_setting",
    "read_setting",
    "check_setting",
]


def save_setting(name, data_dict, is_global=True):
    """
    保存设置数据。
    
    -----
    
    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param dict data_dict: 数据字典
    :param bool is_global: 是否为全局数据，默认为True
    
    :return: 是否保存成功
    :rtype: bool
    """
    return _LvComp.ConfigClient.SetConfigData(name, data_dict, is_global)


def read_setting(name, is_global=True):
    """
    读取设置数据。
    
    -----

    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param bool is_global: 是否为全局数据，默认为True
    
    :return: 数据字典
    :rtype: dict
    """
    return _LvComp.ConfigClient.GetConfigData(name, is_global)


def check_setting(name, item_list, is_global=True):
    """
    检测本地存储的设置数据是否完整。
    
    -----

    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param list item_list: 检测项目列表
    :param bool is_global: 是否为全局数据，默认为True

    :return: 缺失项目列表
    :rtype: list
    """
    data = read_setting(name, is_global)
    return [k for k in item_list if k not in data]























