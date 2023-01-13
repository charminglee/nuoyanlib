
# -*- coding: utf-8 -*-
from ..page.basePage import BasePage


class PageGroup(object):

    def GetAddr(self):
        # type: () -> str
        """
            获取该页组的绝对路径
        """
        pass

    def GetPages(self):
        # type: () -> list[BasePage]
        """
            获取该页组的页面数量
        """ 
        pass

    def GetPagesCount(self):
        # type: () -> int
        """
            获取该页组的页面数量
        """  
        pass     

