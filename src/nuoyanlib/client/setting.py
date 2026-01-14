# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


from ..core.client.comp import LvComp


if 0:
    from typing import Any


__all__ = [
    "save_setting",
    "read_setting",
]


def save_setting(name, data, is_global=True):
    """
    保存设置数据。
    
    -----
    
    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param Any data: 数据
    :param bool is_global: 是否为全局数据；默认为 True
    
    :return: 是否保存成功
    :rtype: bool
    """
    if isinstance(data, dict):
        data_dict = data
    else:
        data_dict = {'__nyl_setting_data__': data}
    return LvComp.ConfigClient.SetConfigData(name, data_dict, is_global)


def read_setting(name, default=None, is_global=True):
    """
    读取设置数据。
    
    -----

    :param str name: 数据名，只能包含字母、数字和下划线字符
    :param Any|None default: 数据默认值；默认为 None
    :param bool is_global: 是否为全局数据；默认为 True
    
    :return: 数据字典
    :rtype: dict
    """
    data_dict = LvComp.ConfigClient.GetConfigData(name, is_global)
    if not data_dict:
        return default
    data = data_dict.get('__nyl_setting_data__', data_dict)
    if isinstance(data, dict):
        data = {
            (str(k) if isinstance(k, unicode) else k): v
            for k, v in data.items()
        }
    return data























