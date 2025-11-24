# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


import os
import shutil
from sphinx.application import Sphinx


SOURCE_DIR = "docs/source"
BUILD_DIR = "docs/build"
DOCTREES_DIR = "docs/build/.doctrees"
BUILDER = "html"


if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)


app = Sphinx(
    srcdir=SOURCE_DIR,
    confdir=SOURCE_DIR,
    outdir=BUILD_DIR,
    doctreedir=DOCTREES_DIR,
    buildername=BUILDER,
    parallel=4,
)
app.build()

