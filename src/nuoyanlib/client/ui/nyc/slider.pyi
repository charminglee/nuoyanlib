# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-30
|
| ====================================================
"""


from typing import Optional
from mod.client.ui.controls.sliderUIControl import SliderUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NySlider(NyControl):
    _base_control: SliderUIControl
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        slider_control: SliderUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, val: float) -> None: ...
    GetSliderValue = SliderUIControl.GetSliderValue
    SetSliderValue = SliderUIControl.SetSliderValue
