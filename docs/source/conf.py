# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-06
|
| ==============================================
"""


import re


project = "「nuoyanlib」"
copyright = "2025, Nuoyan"
author = "Nuoyan"
language = "zh_CN"


extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]


templates_path = ["_templates"]
exclude_patterns = []


html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_theme_options = {
    'footer_icons': [
        {
            'name': "GitHub",
            'url': "https://github.com/charminglee/nuoyanlib",
            'html': """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            'class': "",
        },
        {
            'name': "Gitee",
            'url': "https://gitee.com/charming-lee/nuoyanLib",
            'html': """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.982 0 1.778-.796 1.778-1.778v-.296a.593.593 0 0 0-.592-.593h-4.15a.592.592 0 0 1-.592-.592v-1.482a.593.593 0 0 1 .593-.592h6.815c.327 0 .593.265.593.592v3.408a4 4 0 0 1-4 4H5.926a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.445-4.444h8.296Z"></path>
                </svg>
            """,
            'class': "",
        },
    ],
}


autosummary_generate = True


autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_mock_imports = [
    # "mod",
    # "mod.client",
    # "mod.server",
    # "mod.common",
]
autodoc_default_options = {}
autodoc_docstring_signature = True


def autodoc_process_docstring(app, what, name, obj, options, lines):
    for i, line in enumerate(lines[:]):
        if line.startswith("| "):
            lines[i] = line[2:]
        if re.match(r"\[.+]", line):
            lines.pop(i)
            lines.pop(i + 1)


def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
    # path = f"src/{obj.__module__.replace('.', '/')}.pyi"
    # with open(path, "r", encoding="utf-8") as f:
    #     pyi = f.read()
    return signature, return_annotation


def autodoc_skip_member(app, what, name, obj, skip, options):
    if name in ("__truediv__", "__bool__"):
        return True
    if what == "class" and name not in obj.__dict__:
        return True
    if name.startswith("_") and name != "__init__" and (not getattr(obj, '__doc__', "") or "-----" not in obj.__doc__):
        return True
    return skip


def setup(app):
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-process-signature", autodoc_process_signature)
    app.connect("autodoc-skip-member", autodoc_skip_member)













