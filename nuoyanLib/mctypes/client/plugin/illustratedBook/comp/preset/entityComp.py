
# -*- coding: utf-8 -*-
from ...comp.baseComp import BaseComp
from ...bookConfig import BookConfig

class EntityComp(BaseComp):

    def __init__(self):
        # type: () -> EntityComp
        """
            工作台合成表组件初始化
        """
        pass

    def SetDataBeforeShow(self, entityName, molang_dict = {}, entityOffset = (0, 0), backgroundImage = BookConfig.Images.sqrtPanel_light):
        # type: (str, dict, tuple[int, int], str) -> EntityComp
        """
            在显示组件之前，设置组件的数据
        """       
        pass
    


