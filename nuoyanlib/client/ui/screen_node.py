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


from types import MethodType as _MethodType
from functools import wraps as _wraps
from ..._core._client import _lib_client, _comp
from ..._core import _listener, _utils
from . import ui_utils as _ui_utils
from .button import NyButton as _NyButton


__all__ = [
    "ScreenNodeExtension",
]


class ScreenNodeExtension(_listener.ClientEventProxy):
    """
    | ScreenNode扩展类，提供更多UI界面功能。
    """

    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

    # noinspection PyUnresolvedReferences
    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._lib_sys = _lib_client.instance()
        self._ui_pos_data_key = ""
        self._screen_node = None
        self.cs = None
        if isinstance(self, _comp.CustomUIScreenProxy):
            # 兼容UI代理
            self._screen_node = args[1]
            self._method_proxy("OnCreate", self.__Create)
            self._method_proxy("OnDestroy", self.__Destroy)
        elif isinstance(self, _comp.ScreenNode):
            self._screen_node = self
            self.cs = args[2].get('__cs__') if len(args) == 3 and isinstance(args[2], dict) else None
            self._method_proxy("Create", self.__Create)
            self._method_proxy("Destroy", self.__Destroy)
        else:
            raise TypeError("cannot find ScreenNode instance")
        self.ny_buttons = []
        self.root_panel = (
            self._screen_node.GetBaseUIControl(ScreenNodeExtension.ROOT_PANEL_PATH)
            or self._screen_node.GetBaseUIControl("")
        )

    # System Event Callbacks ===========================================================================================

    def __Create(self):
        # noinspection PyUnresolvedReferences
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (self._screen_node.namespace, self._screen_node.name)
        self._recover_ui_pos()

    def __Destroy(self):
        for btn in self.ny_buttons:
            btn.Destroy()

    # APIs =============================================================================================================

    @_utils.method_cache
    def CreateNyButton(self, path):
        """
        | 创建NyButton按钮实例。

        -----

        :param str path: 按钮路径

        :return: 按钮实例，创建失败返回None
        :rtype: _NyButton|None
        """
        btn = _ui_utils.to_button(self._screen_node, path)
        if btn:
            btn = _NyButton(self._screen_node, btn)
            self.ny_buttons.append(btn)
            return btn

    def GetAllChildrenPathByLevel(self, control, level=1):
        """
        | 获取控件的指定层级的所有子控件的路径。
        | 例如，某面板panel包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推，则 ``GetAllChildrenPathByLevel(panel,2)`` 将返回这六张图片的路径。

        -----

        :param str|BaseUIControl control: 控件路径或实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级的所有子控件的路径列表，获取不到时返回空列表
        :rtype: list[str]
        """
        return _ui_utils.get_all_children_path_by_level(control, self._screen_node, level)

    def GetParentPath(self, control):
        """
        | 获取控件的父控件路径。

        -----

        :param str|BaseUIControl control: 控件路径或实例

        :return: 父控件路径，获取不到返回None
        :rtype: str|None
        """
        return _ui_utils.get_parent_path(control)

    def GetParentControl(self, control):
        """
        | 获取控件的父控件实例。

        -----

        :param str|BaseUIControl control: 控件路径或实例

        :return: 父控件实例（BaseUIControl），获取不到返回None
        :rtype: BaseUIControl|None
        """
        return _ui_utils.get_parent_control(control, self._screen_node)

    def ClearAllPosData(self):
        """
        | 删除所有控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        return _ui_utils.save_ui_pos_data(self._ui_pos_data_key, {})

    def SaveAllPosData(self):
        """
        | 保存所有通过 ``SetMovable`` 或 ``SetMovableByLongClick`` 设置了可拖动的控件的位置数据，下次进入游戏时自动恢复。
        | 为保证安全，超出屏幕边界的按钮不会被保存。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        for btn in self.ny_buttons:
            if btn.is_movable:
                btn.SavePosData()
        return True

    # Internal =========================================================================================================

    def _method_proxy(self, org_method_name, my_method):
        org_method = getattr(self, org_method_name)
        @_wraps(org_method.__func__)
        def proxy(self, *args, **kwargs):
            my_method(*args, **kwargs)
            org_method(*args, **kwargs)
        proxy_method = _MethodType(proxy, self)
        setattr(self, org_method_name, proxy_method)

    def _recover_ui_pos(self):
        data = _ui_utils.get_ui_pos_data(self._ui_pos_data_key)
        for data_lst in data.values():
            for path, pos in data_lst:
                control = _ui_utils.to_control(self._screen_node, path)
                if control:
                    control.SetPosition(pos)
























