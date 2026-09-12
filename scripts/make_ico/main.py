# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


from PIL import Image


icon_sizes = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


with Image.open("img/installer_icon.png") as source:
    frames = [
        source.resize(
            size,
            resample=(
                Image.Resampling.NEAREST
                if size[0] <= 128
                else Image.Resampling.LANCZOS
            ),
        )
        for size in icon_sizes
    ]
    frames[-1].save(
        "img/installer_icon.ico",
        format="ICO",
        sizes=icon_sizes,
        append_images=frames[:-1],
    )
