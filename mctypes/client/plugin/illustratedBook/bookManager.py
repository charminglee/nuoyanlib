
# -*- coding: utf-8 -*-
from bookConfig import BookConfig
from bookInstance.preset.normalBook import NormalBook

from comp.baseComp import BaseComp
from comp.preset.buttonComp import ButtonComp
from comp.preset.entityComp import EntityComp
from comp.preset.highlightComp import HighlightComp
from comp.preset.imageComp import ImageComp
from comp.preset.textComp import TextComp
from comp.preset.progressBarComp import ProgressBarComp

from page.basePage import BasePage
from page.preset.titlePage import TitlePage

from group.pageGroup import PageGroup
from group.preset.book import Book
from group.preset.category import Category
from group.preset.entry import Entry


class BookManager(object):

    def GetBookInstance(self, bookName):
        # type: (str) -> NormalBook
        """
            根据书本名称获取管理该书本的对象
        """
        pass

    def GetOpeningBookInstance(self):
        # type: () -> NormalBook
        """
            获取当前处于打开状态的书本的管理对象
        """
        pass

    def ShowMsg(self, position, msg):
        # type: (tuple[int, int], str) -> None
        """
            全局显示消息文本
        """   
        pass    

    def HideMsg(self):
        # type: () -> None
        """
            隐藏全局消息文本
        """ 
        pass

    def AddPageType(self, pageName, pageCls):
        # type: (str, type) -> None
        """
            注册自定义页面
        """ 
        pass

    def UpdateScreen(self):
        # type: () -> None
        """
            刷新书本界面
        """
        pass

    def To(self, addr):
        # type: (str) -> None
        """
            注册自定义页面
        """ 
        pass

    def GetBookConfig(self):
        # type: () -> BookConfig
        """
            获取书本配置常量
        """   
        pass      

    def GetBasePageCls(self):
        # type: () -> type[BasePage]
        """
            获取页面类的基类
        """
        pass

    def GetTitlePageCls(self):
        # type: () -> type[TitlePage]
        """
            获取 预设页面 TitlePage 类
        """
        pass

    def GetBaseCompCls(self):
        # type: () -> type[BaseComp]
        """
            获取组件类的基类
        """
        pass

    def GetButtonCompCls(self):
        # type: () -> type[ButtonComp]
        """
            获取 预设组件 ButtonComp 类
        """
        pass

    def GetEntityCompCls(self):
        # type: () -> type[EntityComp]
        """
            获取 预设组件 EntityComp 类
        """
        pass

    def GetHighlightCompCls(self):
        # type: () -> type[HighlightComp]
        """
            获取 预设组件 HighlightComp 类
        """
        pass

    def GetImageCompCls(self):
        # type: () -> type[ImageComp]
        """
            获取 预设组件 ImageComp 类
        """
        pass

    def GetTextCompCls(self):
        # type: () -> type[TextComp]
        """
            获取 预设组件 TextComp 类
        """
        pass

    def GetProgressBarCompCls(self):
        # type: () -> type[ProgressBarComp]
        """
            获取 预设组件 ProgressBarComp 类
        """
        pass

    def GetPageGroupCls(self):
        # type: () -> type[PageGroup]
        """
            获取页组类的基类
        """
        pass

    def GetBookCls(self):
        # type: () -> type[Book]
        """
            获取包含书本首页的页组类 
        """
        pass

    def GetCategoryCls(self):
        # type: () -> type[Category]
        """
            获取包含目录首页的页组类 
        """
        pass

    def GetEntryCls(self):
        # type: () -> type[Entry]
        """
            获取包含章节首页的页组类 
        """
        pass
