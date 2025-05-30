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
#   Last Modified : 2025-05-30
#
# ====================================================


from types import MethodType
from typing import Optional, List, overload, Dict
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._types._typing import UiControl
from ..._core._listener import ClientEventProxy
from .button import NyButton


class ScreenNodeExtension(ClientEventProxy):
    ROOT_PANEL_PATH: str
    """
    | 使用基类画布时的根节点路径，所有自定义控件均挂接在该路径下。
    """
    _ui_pos_data_key: str
    _screen_node: Optional[ScreenNode]
    _control_cache: Dict[str, NyButton]
    cs: Optional[ClientSystem]
    """
    | 创建UI的客户端实例。
    """
    ny_buttons: List[NyButton]
    """
    | 通过 ``CreateNyButton`` 创建的NyButton按钮实例的列表。
    """
    root_panel: Optional[BaseUIControl]
    """
    | 当前界面根节点的 ``BaseUIControl`` 实例。
    """
    @overload
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict] = None, /) -> None: ...
    @overload
    def __init__(self: ..., screen_name: str, screen_node: ScreenNode, /) -> None: ...
    def __Create(self): ...
    def __Destroy(self): ...
    def CreateNyButton(self, path: str, touch_event_params: Optional[dict] = None) -> Optional[NyButton]: ...
    def ClearAllPosData(self) -> bool: ...
    def SaveAllPosData(self) -> bool: ...
    def GetAllChildrenPathByLevel(self, control: UiControl, level: int = 1) -> List[str]: ...
    def GetParentPath(self, control: UiControl) -> Optional[str]: ...
    def GetParentControl(self, control: UiControl) -> Optional[BaseUIControl]: ...
    def _method_proxy(self, org_method_name: str, my_method: MethodType) -> MethodType: ...
    def _recover_ui_pos(self) -> None: ...
