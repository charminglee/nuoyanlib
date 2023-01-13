# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Email         : 1279735247@qq.com
#   Last Modified : 2023-01-13
#
# ====================================================


import mod.client.extraClientApi as _clientApi


_LEVEL_ID = _clientApi.GetLevelId()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_LevelConfigClientComp = _ClientCompFactory.CreateConfigClient(_LEVEL_ID)


def save_setting(name, dataDict, isGlobal=True):
    # type: (str, dict, bool) -> bool
    """
    保存设置数据。
    -----------------------------------------------------------
    【name: str】 数据名
    【dataDict: dict】 数据
    【isGlobal: bool = True】 是否为全局数据
    -----------------------------------------------------------
    return: bool -> 保存成功返回True，失败返回False
    """
    return _LevelConfigClientComp.SetConfigData(name, dataDict, isGlobal)


def read_setting(name, isGlobal=True):
    # type: (str, bool) -> dict
    """
    读取设置数据。
    -----------------------------------------------------------
    【name: str】 数据名
    【isGlobal: bool = True】 是否为全局数据
    -----------------------------------------------------------
    return: dict -> 数据
    """
    return _LevelConfigClientComp.GetConfigData(name, isGlobal)


# noinspection PyUnresolvedReferences
def check_setting(name, itemList, isGlobal=True):
    # type: (str, list, bool) -> list
    """
    检测本地存储的设置数据是否完整。
    示例：
    data = {'name': "nuoyan", 'qq': "1279735247"}
    save_setting("ny", data)
    checkItem = ["name", "qq", "email", "age"]
    check_setting("ny", checkItem)     # ["email", "age"]
    -----------------------------------------------------------
    【name: str】 数据名
    【itemList: list】 检测项目列表
    【isGlobal: bool = True】 是否为全局数据
    -----------------------------------------------------------
    return: list -> 缺失项目列表
    """
    data = read_setting(name, isGlobal)
    return [k for k in itemList if k not in data]























