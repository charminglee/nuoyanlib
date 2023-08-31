# -*- coding: utf-8 -*-

from baseUIControl import BaseUIControl

class GridUIControl(BaseUIControl):
    def SetGridDimension(self, dimension):
        # type: (tuple[int,int]) -> None
        """
        设置Grid控件的大小
        """
        pass

    def GetGridItem(self, x, y):
        # type: (int, int) -> BaseUIControl
        """
        根据网格位置获取元素控件
        """
        pass

