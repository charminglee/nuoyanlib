# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-14
|
| ==============================================
"""


from mod.common.minecraftEnum import KeyBoardType


_allowed_keys = {
    i
    for i in KeyBoardType.__dict__.values()
    if isinstance(i, int)
}
_allowed_keys.remove(4)


def bind_key(key, on_up=None, on_down=None, cond=None, multi_binding=False):
    """
    | 绑定按键回调函数。

    -----

    :param int key: 按键类型，请使用 `KeyBoardType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?catalog=1>`_ 枚举值
    :param function|None on_up: 按键抬起时触发的回调函数，默认为None
    :param function|None on_down: 按键按下时触发的回调函数，默认为None
    :param function|None cond: 按键触发条件，该函数需要返回一个bool，为True时才会触发回调函数；默认为None，即无条件
    :param bool multi_binding: 是否允许多次绑定同一按键，默认为False；设为False时，如果要绑定的按键在当前模组中已经绑定了其他回调函数，则本次绑定将会失败

    :return: 是否绑定成功
    :rtype: bool
    """
    if key not in _allowed_keys:
        return False
    return True














