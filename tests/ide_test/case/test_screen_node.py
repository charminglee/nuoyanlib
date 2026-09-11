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


from nuoyanlib.client.ui import screen_node as screen_node_module
from nuoyanlib.client.ui.screen_node import NyScreenBase, NyScreenNode, screen
from nuoyanlib.client.ui.nyc.control import NyControl


n = [0]


@screen("", enabled_deferred_init=True)
class SN(NyScreenNode):
    def __init__(self, namespace, name, param):
        super(SN, self).__init__(namespace, name, param)
        n[0] += 1
        assert (namespace, name, param) == args


args = "", "", {'x': 1}
sn = SN(*args)
assert n[0] == 0
sn.Create()
assert n[0] == 1
assert SN.n == 1
assert SN._nyl__instances[0] is sn
sn.Destroy()


args = "a", "b", {'x': 2}
sn = SN(*args)
assert len(SN._nyl__instances) == 1 and SN._nyl__instances[0] is sn
assert n[0] == 1
assert SN.n == 2
sn.Create()
assert n[0] == 2
sn.Destroy()


assert not SN._nyl__instances


class FakeUIControl(object):
    def __init__(self, path, position):
        self.path = path
        self.position = tuple(position)

    def GetPath(self):
        return self.path

    def FullPath(self):
        return "test%s" % self.path

    def GetPosition(self):
        return self.position

    def SetPosition(self, position):
        self.position = tuple(position)

    def GetGlobalPosition(self):
        return self.position

    def GetSize(self):
        return (1, 1)


class FakeScreen(object):
    namespace = "test"
    name = "main"

    def __init__(self):
        self.controls = {
            "": FakeUIControl("", (1, 2)),
            "/panel": FakeUIControl("/panel", (3, 4)),
            "/panel/button": FakeUIControl("/panel/button", (5, 6)),
        }

    def GetBaseUIControl(self, path):
        return self.controls.get(path)

    def GetAllChildrenPath(self, path):
        if path == "":
            return ["/panel", "/panel/button"]
        return []


saved_pos_data = {}
original_read_setting = screen_node_module.read_setting
original_save_setting = screen_node_module.save_setting
original_is_out_of_screen = screen_node_module.is_out_of_screen
screen_node_module.read_setting = lambda *args: dict(saved_pos_data)
screen_node_module.is_out_of_screen = lambda control: False
base = None


def save_pos(key, data, is_global):
    saved_pos_data.clear()
    saved_pos_data.update(data)
    return True


screen_node_module.save_setting = save_pos
try:
    fake_screen = FakeScreen()
    base = NyScreenBase()
    base._screen_node = fake_screen
    base.is_control_exist = lambda path: False
    base._process_button_callback = lambda: None
    base.__ui_create__()

    assert base._ui_default_pos_data == {
        "": (1, 2),
        "/panel": (3, 4),
        "/panel/button": (5, 6),
    }
    fake_screen.controls["/panel/button"].SetPosition((50, 60))
    assert base.reset_all_ui_pos()
    assert fake_screen.controls["/panel/button"].GetPosition() == (5, 6)

    NyControl(base, "/panel/button")
    fake_screen.controls["/panel/button"].SetPosition((7, 8))
    assert base.save_all_pos_data()
    assert base._ui_pos_data["/panel/button"] == (7, 8)
    assert base.clear_all_ui_pos_data()
    assert base._ui_pos_data == {} and not saved_pos_data
finally:
    if base and not base.is_destroyed:
        base.__ui_destroy__()
    screen_node_module.read_setting = original_read_setting
    screen_node_module.save_setting = original_save_setting
    screen_node_module.is_out_of_screen = original_is_out_of_screen
