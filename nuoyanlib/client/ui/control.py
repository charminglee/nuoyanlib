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
#   Last Modified : 2025-05-28
#
# ====================================================


# todo
class NyControl(object):
    """
    | 创建NyControl通用UI控件实例。
    | 兼容ModSDK ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNode screen_node: 控件所在UI类的实例
    :param BaseUIControl control: 通过GetBaseUIControl()获取的控件实例
    """
    def __init__(self, screen_node, control):
        self.screen_node = screen_node
        self.control = control
        self.path = control.GetPath()

    def __getattr__(self, name):
        # 尝试调用ModSDK方法
        return getattr(self.control, name)

    @property
    def position(self):
        """
        按钮相对于父控件的坐标。
        """
        return self.control.GetPosition()

    @position.setter
    def position(self, val):
        """
        按钮相对于父控件的坐标。
        """
        self.control.SetPosition(val)








