
# -*- coding: utf-8 -*-
from ...group.pageGroup import PageGroup


class Book(PageGroup):

    def GetSons(self):
        # type: () -> list[Category]
        """
            获取子页组（其子页组就是Category对象）
        """
        pass

    def GetProgressValue(self):
        # type: () -> float
        """
            获取子页组解锁的进度，常用于进度条显示
        """ 
        pass

