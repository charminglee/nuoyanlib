# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-26
|
| ==============================================
"""


from typing import Optional, Callable, Any, Dict, Union
from types import MethodType
from mod.client.ui.controls.neteaseComboBoxUIControl import NeteaseComboBoxUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


__ComboBoxCallbackType = Callable[[Any], Any]


class NyComboBox(NyControl):
    _callback_map: Dict[str, MethodType]
    base_control: NeteaseComboBoxUIControl
    """
    | 下拉框 ``NeteaseComboBoxUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        combo_box_control: NeteaseComboBoxUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def _item_to_index(self, item: Union[int, str]) -> int: ...
    @args_type_check((int, str), is_method=True)
    def __getitem__(self, item: Union[int, str]) -> NyControl: ...
    @args_type_check((int, str), is_method=True)
    def __delitem__(self, item: Union[int, str]) -> None: ...
    def set_callback(self, callback_type: str, func: __ComboBoxCallbackType) -> None: ...
    @property
    def opt_count(self) -> int: ...
    @property
    def selected_opt_index(self) -> int: ...
    @selected_opt_index.setter
    def selected_opt_index(self, val: int) -> None: ...
    @property
    def selected_opt_name(self) -> Optional[str]: ...
    @selected_opt_name.setter
    def selected_opt_name(self, val: Optional[str]) -> None: ...

    def AddOption(self, show_name: str, icon: Optional[str] = None, user_data: Optional[Any] = None) -> bool:
        """
        | 添加下拉框项，若添加成功则返回 ``True`` ，否则返回 ``False`` 。

        -----

        :param str show_name: 显示文本
        :param str|None icon: 贴图路径，若填写则在下拉框项前端会显示该icon，默认为None
        :param Any|None user_data: 自定义数据，在选中该下拉框项时会跟随回调函数传回，默认为None

        :return: 是否成功
        :rtype: bool
        """
    def ClearOptions(self) -> None:
        """
        | 清空下拉框。

        -----

        :return: 无
        :rtype: None
        """
    def ClearSelection(self) -> None:
        """
        | 清除当前选中，使下拉框恢复未选中内容状态。

        -----

        :return: 无
        :rtype: None
        """
    def GetOptionIndexByShowName(self, show_name: str) -> int:
        """
        | 根据显示文本查找对应下拉框项的索引位置，若找不到返回 ``-1`` 。

        -----

        :param str show_name: 显示文本

        :return: 索引位置
        :rtype: int
        """
    def GetOptionShowNameByIndex(self, index: int) -> str:
        """
        | 根据索引位置查找显示文本，若找不到返回 ``None`` 。

        -----

        :param int index: 索引位置

        :return: 显示文本
        :rtype: str
        """
    def GetOptionCount(self) -> int:
        """
        | 获得选项数量。

        -----

        :return: 选项数量
        :rtype: int
        """
    def GetSelectOptionIndex(self) -> int:
        """
        | 获得当前选中项的索引，若无选中项则返回 ``-1`` 。

        -----

        :return: 当前选中项的索引
        :rtype: int
        """
    def GetSelectOptionShowName(self) -> Optional[str]:
        """
        | 获得当前选中项的显示文本，所无选中项则返回 ``None`` 。

        -----

        :return: 当前选中项的显示文本
        :rtype: str|None
        """
    def RemoveOptionByShowName(self, show_name: str) -> bool:
        """
        | 根据提供的显示文本移除对应下拉框项，移除成功则返回 ``True`` ，否则返回 ``False`` 。

        -----

        :param str show_name: 显示文本

        :return: 是否成功
        :rtype: bool
        """
    def RemoveOptionByIndex(self, index: int) -> bool:
        """
        | 根据提供的索引移除对应下拉框项，移除成功则返回 ``True`` ，否则返回 ``False`` 。

        -----

        :param int index: 索引位置

        :return: 是否成功
        :rtype: bool
        """
    def SetSelectOptionByIndex(self, index: int) -> None:
        """
        | 根据提供的索引选中对应下拉框项。

        -----

        :param int index: 索引位置

        :return: 无
        :rtype: None
        """
    def SetSelectOptionByShowName(self, show_name: str) -> None:
        """
        | 根据提供的显示文本选中对应下拉框项。

        -----

        :param str show_name: 显示文本

        :return: 无
        :rtype: None
        """
    def RegisterOpenComboBoxCallback(self, callback: __ComboBoxCallbackType) -> None:
        """
        | 注册展开下拉框事件回调。

        -----

        :param function callback: 回调函数

        :return: 无
        :rtype: None
        """
    def RegisterCloseComboBoxCallback(self, callback: __ComboBoxCallbackType) -> None:
        """
        | 注册关闭下拉框事件回调。

        -----

        :param function callback: 回调函数

        :return: 无
        :rtype: None
        """
    def RegisterSelectItemCallback(self, callback: __ComboBoxCallbackType) -> None:
        """
        | 注册选中下拉框内容事件回调。

        -----

        :param function callback: 回调函数

        :return: 无
        :rtype: None
        """
