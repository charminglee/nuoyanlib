# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-22
#  ⠀
# =================================================


import mod.client.extraClientApi as c_api
from mod.common.minecraftEnum import *
from ..common.mod_config import *
from ..nuoyanlib import client as nyl
from ..nuoyanlib.client import (
    LvComp,
    PlrComp,
    CF,
    PLAYER_ID,
    event,
    ScreenNodeExtension,
)
from ..nuoyanlib.utils.enum import (
    ControlType,
    ButtonCallbackType,
    ComboBoxCallbackType,
)


clientEvent = event(ns=MOD_NAME, sys_name=CLIENT_SYSTEM_NAME)
serverEvent = event(ns=MOD_NAME, sys_name=SERVER_SYSTEM_NAME)


class NuoyanlibTest(nyl.ClientEventProxy, ScreenNodeExtension, nyl.ScreenNode):
    def __init__(self, namespace, name, param):
        super(NuoyanlibTest, self).__init__(namespace, name, param)
        self.grid = None            # type: nyl.NyGrid | None
        self.stack_panel = None     # type: nyl.NyStackPanel | None
        self.scroll_view = None     # type: nyl.NyScrollView | None
        self.label = None           # type: nyl.NyLabel | None
        self.button = None          # type: nyl.NyButton | None
        self.image = None           # type: nyl.NyImage | None
        self.switch_toggle = None   # type: nyl.NyToggle | None
        self.progress_bar = None    # type: nyl.NyProgressBar | None
        self.edit_box = None        # type: nyl.NyEditBox | None
        self.combo_box = None       # type: nyl.NyComboBox | None
        self.a = False
        self.move_parent = False

    def Create(self):
        self.grid = (self.root_panel / "grid").to_grid()
        self.stack_panel = (self.root_panel / "stack_panel").to_stack_panel()
        self.scroll_view = (self.root_panel / "scroll_view").to_scroll_view()
        self.label = (self.stack_panel / "label").to_label()
        self.button = (self.stack_panel / "button").to_button()
        self.image = (self.stack_panel / "image").to_image()
        self.switch_toggle = (self.stack_panel / "switch_toggle").to_toggle()
        self.progress_bar = (self.stack_panel / "progress_bar").to_progress_bar()
        self.edit_box = (self.stack_panel / "edit_box").to_edit_box()
        self.combo_box = (self.root_panel / "combo_box").to_combo_box()

        self.build_binding(self.label_binding, nyl.ViewBinder.BF_BindString)

        self.button.set_callback(self.OnButtonUp, ButtonCallbackType.UP)
        self.button.set_callback(self.OnButtonDown, ButtonCallbackType.DOWN)
        self.button.set_callback(self.OnButtonLongClick, ButtonCallbackType.LONG_CLICK)
        self.button.set_callback(self.OnButtonDoubleClick, ButtonCallbackType.DOUBLE_CLICK)
        (self.button / "toggle").to_toggle().set_callback(self.OnToggleChanged)

        self.switch_toggle.set_callback(self.OnToggleChanged1)

        self.combo_box.set_callback(self.OnComboBoxOpen, ComboBoxCallbackType.OPEN)
        self.combo_box.set_callback(self.OnComboBoxClose, ComboBoxCallbackType.CLOSE)
        self.combo_box.set_callback(self.OnComboBoxSelect, ComboBoxCallbackType.SELECT)
        self.combo_box.bind_data(("选项%d" % i, None, i) for i in range(6))

    def label_binding(self):
        return "动态绑定测试"

    def OnButtonUp(self, args):
        if self.button.has_long_clicked:
            self.button.cancel_movable()
            return
        print("button_up")
        c_api.PopScreen()

    def OnButtonDown(self, args):
        print("button_down")

    def OnButtonLongClick(self, args):
        print("button_long_click")
        self.button.set_movable(self.move_parent, auto_save=True)

    def OnButtonDoubleClick(self, args):
        print("button_double_click")

    def OnToggleChanged(self, args):
        print(1, args)
        self.move_parent = args['state']
        return nyl.ViewRequest.Refresh

    def OnToggleChanged1(self, args):
        print(2, args)
        return nyl.ViewRequest.Refresh

    def OnComboBoxOpen(self):
        print("combo_box_open")

    def OnComboBoxClose(self):
        print("combo_box_close")

    def OnComboBoxSelect(self, index, name, user_data):
        if index == -1:
            return
        print("combo_box_select")
        print(index, name, user_data)
        print(self.combo_box[index])
        del self.combo_box[index]






















