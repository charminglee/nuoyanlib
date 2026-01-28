# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from typing import Optional
from mod.client.ui.controls.sliderUIControl import SliderUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self


class NySlider(NyControl):
    _base_control: SliderUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        slider_control: SliderUIControl,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, val: float) -> None: ...
    GetSliderValue = SliderUIControl.GetSliderValue
    SetSliderValue = SliderUIControl.SetSliderValue
