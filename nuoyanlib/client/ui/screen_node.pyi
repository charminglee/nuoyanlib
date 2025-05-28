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


from types import MethodType
from typing import Optional, List, overload
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._typing import UiControl
from ..._core._client._lib_client import NuoyanLibClientSystem
from ..._core._listener import ClientEventProxy
from ..._core._utils import method_cache
from .button import NyButton


class ScreenNodeExtension(ClientEventProxy):
    ROOT_PANEL_PATH: str
    _lib_sys: NuoyanLibClientSystem
    _ui_pos_data_key: str
    _screen_node: Optional[ScreenNode]
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
    @method_cache
    def CreateNyButton(self, path: str) -> Optional[NyButton]: ...
    def ClearAllPosData(self) -> bool: ...
    def SaveAllPosData(self) -> bool: ...
    def GetAllChildrenPathByLevel(self, control: UiControl, level: int = 1) -> List[str]: ...
    def GetParentPath(self, control: UiControl) -> Optional[str]: ...
    def GetParentControl(self, control: UiControl) -> Optional[BaseUIControl]: ...
    def _method_proxy(self, org_method_name: str, my_method: MethodType) -> MethodType: ...
    def _recover_ui_pos(self) -> None: ...
