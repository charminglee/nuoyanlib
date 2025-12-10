# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-09
|
| ====================================================
"""


from ..core.client.comp import LvComp


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
    return LvComp.ConfigClient.SetConfigData(name, data_dict, is_global)


def read_setting(name, is_global=True):
    """
    读取设置数据。
    
    -----

    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param bool is_global: 是否为全局数据，默认为True
    
    :return: 数据字典
    :rtype: dict
    """
    data = LvComp.ConfigClient.GetConfigData(name, is_global)
    if data:
        data = {
            (str(k) if isinstance(k, unicode) else k): v
            for k, v in data.items()
        }
    return data


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























