# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


import mod.client.extraClientApi as c_api
from mod.common.minecraftEnum import *
from mod.client.ui.viewRequest import ViewRequest
from mod.client.ui.viewBinder import ViewBinder
from ..common.constant import *
from ..nuoyanlib import client as nyl


@nyl.screen(
    "nuoyanlib_test",
    "screen",
    auto_show=True,
    enabled_deferred_init=True,
    push_to_ui_stack=True,
)
class NuoyanlibTest(nyl.NyScreenNode):
    def __init__(self, namespace, name, param):
        super(NuoyanlibTest, self).__init__(namespace, name, param)
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

        self.build_binding(self.label_binding, ViewBinder.BF_BindString)

        self.button.set_callback(self.on_button_up, nyl.NyButton.UP)
        self.button.set_callback(self.on_button_down, nyl.NyButton.DOWN)
        self.button.set_callback(self.on_button_long_click, nyl.NyButton.LONG_CLICK)
        self.button.set_callback(self.on_button_double_click, nyl.NyButton.DOUBLE_CLICK)
        (self.button / "toggle").to_toggle().set_callback(self.on_toggle_changed)

        self.switch_toggle.set_callback(self.on_toggle_changed_1)

        self.combo_box.set_callback(self.on_combo_box_open, nyl.NyComboBox.OPEN)
        self.combo_box.set_callback(self.on_combo_box_close, nyl.NyComboBox.CLOSE)
        self.combo_box.set_callback(self.on_combo_box_select, nyl.NyComboBox.SELECT)
        self.combo_box.bind_data(("选项%d" % i, None, i) for i in range(6))

        self.move_parent = False

    def __ui_active__(self):
        print("__ui_active__")

    def __ui_deactive__(self):
        print("__ui_deactive__")

    def label_binding(self):
        return "动态绑定测试"

    def on_button_up(self, args):
        if self.button.has_long_clicked:
            self.button.cancel_movable()
            return
        print("on_button_up")
        # self.hide()

    def on_button_down(self, args):
        print("on_button_down")

    def on_button_long_click(self, args):
        print("on_button_long_click")
        self.button.set_movable(self.move_parent, auto_save=True)

    def on_button_double_click(self, args):
        print("on_button_double_click")

    def on_toggle_changed(self, args):
        print(1, args)
        self.move_parent = args['state']
        return ViewRequest.Refresh

    def on_toggle_changed_1(self, args):
        print(2, args)
        return ViewRequest.Refresh

    def on_combo_box_open(self):
        print("on_combo_box_open")

    def on_combo_box_close(self):
        print("on_combo_box_close")

    def on_combo_box_select(self, index, name, user_data):
        if index == -1:
            return
        print("on_combo_box_select")
        print(index, name, user_data)
        print(self.combo_box[index])
        del self.combo_box[index]






















