# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-10-4
#  ⠀
#  ================================================


from nuoyanlib.client.ui.nyc.control import NyControl, _AUTO_FUNC_MAP
from nuoyanlib.client.ui.nyc import (
    NyButton,
    NyComboBox,
    NyEditBox,
    NyGrid,
    NyImage,
    NyInputPanel,
    NyItemRenderer,
    NyLabel,
    NyMiniMap,
    NyPaperDoll,
    NyProgressBar,
    NyScrollView,
    NySelectionWheel,
    NySlider,
    NyStackPanel,
    NyToggle,
)
from nuoyanlib.client.ui.screen_node import NyScreenNode
from nuoyanlib.client.ui.ui_utils import _UIControlType


class SN(NyScreenNode):
    pass
sn = SN("", "")


for control_cls, control_type in (
    (NyButton, _UIControlType.BUTTON),
    (NyComboBox, _UIControlType.COMBO_BOX),
    (NyEditBox, _UIControlType.EDIT_BOX),
    (NyGrid, _UIControlType.GRID),
    (NyImage, _UIControlType.IMAGE),
    (NyInputPanel, _UIControlType.INPUT_PANEL),
    (NyItemRenderer, _UIControlType.ITEM_RENDERER),
    (NyLabel, _UIControlType.LABEL),
    (NyMiniMap, _UIControlType.MINI_MAP),
    (NyPaperDoll, _UIControlType.NETEASE_PAPER_DOLL),
    (NyProgressBar, _UIControlType.PROGRESS_BAR),
    (NyScrollView, _UIControlType.SCROLL_VIEW),
    (NySelectionWheel, _UIControlType.SELECTION_WHEEL),
    (NySlider, _UIControlType.SLIDER),
    (NyStackPanel, _UIControlType.STACK_PANEL),
    (NyToggle, _UIControlType.TOGGLE),
):
    assert control_cls.CONTROL_TYPE == control_type


n = [0]
class NC(NyControl):
    def __init__(self, ny_screen_node, path):
        NyControl.__init__(self, ny_screen_node, path)
        n[0] += 1
abc = NC(sn, "/abc")
assert NC(sn, "/abc") is abc
assert NC(sn, "/abc2") is not abc
assert n[0] == 2


print(abc)


class FakeReprControl(object):
    def __init__(self, path):
        self.path = path

    def GetPath(self):
        return self.path

    def FullPath(self):
        return self.path


for path, expected in (
    ("/panel/button", "<NyControl 'button' at '/panel/button'>"),
    (
        "/panel/combo_box/comboBoxContent/contentItem/contentItemContent0",
        "<NyControl 'contentItemContent0' at '/panel/combo_box/comboBoxContent/.../contentItemContent0'>",
    ),
):
    repr_control = NyControl.__new__(NyControl)
    repr_control._base_control = FakeReprControl(path)
    assert repr(repr_control) == expected


assert "/abc" in sn._nyc_cache_map
ch = abc / "child"
assert ch.GetPath() == ch.path == "/abc/child"
abc.destroy()
assert "/abc" not in sn._nyc_cache_map


# NyControl.auto
for method_name in _AUTO_FUNC_MAP.values():
    assert callable(getattr(NyControl, method_name))
assert _AUTO_FUNC_MAP.get(_UIControlType.CUSTOM) is None
assert _AUTO_FUNC_MAP.get(_UIControlType.PANEL) is None

auto_c = NyControl.auto(sn, "/auto")
assert type(auto_c) is NyControl
assert NyControl.auto(sn, "/auto") is auto_c
assert NC.auto(sn, "/auto") is not auto_c
assert n[0] == 3
assert NyControl.auto(sn, "/auto") is not auto_c
