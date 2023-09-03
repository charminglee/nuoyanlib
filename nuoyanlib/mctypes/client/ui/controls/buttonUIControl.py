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
#   Last Modified : 2023-08-31
#
# ====================================================


from baseUIControl import BaseUIControl


class ButtonUIControl(BaseUIControl):
    def AddTouchEventParams(self, args=None):
        # type: (dict) -> None
        """
        开启按钮回调功能，不调用该函数则按钮无回调
        """
        pass

    def AddHoverEventParams(self):
        # type: () -> None
        """
        开启按钮的悬浮回调功能，不调用该函数则按钮无悬浮回调
        """
        pass

    def SetButtonTouchDownCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置按钮按下时触发的回调函数
        """
        pass

    def SetButtonHoverInCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置鼠标进入按钮时触发的悬浮回调函数
        """
        pass

    def SetButtonHoverOutCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置鼠标退出按钮时触发的悬浮回调函数
        """
        pass

    def SetButtonTouchUpCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置触控在按钮范围内弹起时的回调函数
        """
        pass

    def SetButtonTouchCancelCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置触控在按钮范围外弹起时触发的回调函数
        """
        pass

    def SetButtonTouchMoveCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置按下后触控移动时触发的回调函数
        """
        pass

    def SetButtonTouchMoveInCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置按下按钮后进入控件时触发的回调函数
        """
        pass

    def SetButtonTouchMoveOutCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置按下按钮后退出控件时触发的回调函数
        """
        pass

    def SetButtonScreenExitCallback(self, callbackFunc):
        # type: (function) -> None
        """
        设置按钮所在画布退出时若鼠标仍未抬起时触发回调函数
        """
        pass

