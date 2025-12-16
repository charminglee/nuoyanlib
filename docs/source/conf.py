# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


import sys
import re
import threading
from sphinx.application import Sphinx
from docutils.nodes import document
from bs4 import BeautifulSoup


import nuoyanlib.client as nyl_c
sys.modules['nuoyanlib.client'] = nyl_c
def import_server():
    import nuoyanlib.server as nyl_s
    sys.modules['nuoyanlib.server'] = nyl_s
t = threading.Thread(target=import_server)
t.start()
t.join()


project = "「nuoyanlib」"
copyright = '2025, <a href="https://github.com/charminglee">Nuoyan</a>'
author = "Nuoyan"
language = "zh_CN"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx.ext.duration",
]
exclude_patterns = []


html_theme = "pydata_sphinx_theme"
templates_path = ["_templates"]
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_theme_options = {
    'icon_links': [
        {
            'name': "GitHub",
            'url': "https://github.com/charminglee/nuoyanlib",
            'icon': """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            'type': "svg",
        },
        {
            'name': "Gitee",
            'url': "https://gitee.com/charming-lee/nuoyanLib",
            'icon': """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.982 0 1.778-.796 1.778-1.778v-.296a.593.593 0 0 0-.592-.593h-4.15a.592.592 0 0 1-.592-.592v-1.482a.593.593 0 0 1 .593-.592h6.815c.327 0 .593.265.593.592v3.408a4 4 0 0 1-4 4H5.926a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.445-4.444h8.296Z"></path>
                </svg>
            """,
            'type': "svg",
        }
    ],
    'navbar_end': [
        "theme-switcher",
        "navbar-icon-links",
    ],
    'footer_start': [
        "copyright",
        "sphinx-version",
    ],
    'footer_end': [
        "theme-version",
    ],
    'show_nav_level': 2
}
html_sidebars = {
    '**': ["sidebar-nav-bs", "sidebar-ethical-ads"]
}
html_context = {
    'theme_collapse_navigation': True,
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
autodoc_default_options = {
    'special-members': ""
}
autodoc_docstring_signature = True


a = 0
def builder_inited(app: Sphinx):
    def shorten_name(s):
        if isinstance(s, BeautifulSoup):
            for tag in s.find_all("a", class_="reference internal"):
                tag.string = re.sub(r"nuoyanlib\.(client|server|utils)\.", "", tag.string)
            # global a
            # if a == 0:
            #     print(s)
            #     a += 1
        return s
    app.builder.templates.environment.filters['shorten_name'] = shorten_name


def autodoc_process_docstring(app: Sphinx, what: str, name: str, obj, options, lines: list[str]):
    for i, line in enumerate(lines[:]):
        if line.startswith("| "):
            lines[i] = line[2:]
        if re.match(r"\[.+]", line):
            lines.pop(i)
            lines.pop(i)


def autodoc_skip_member(app: Sphinx, what: str, name: str, obj: object, skip: bool, options):
    if name in ("__init__", "__truediv__", "__bool__"):
        return True
    if what == "class" and name not in obj.__dict__:
        return True
    if name.startswith("_") and (not getattr(obj, '__doc__', "") or "-----" not in obj.__doc__):
        return True
    return skip


b = 0
def html_page_context(app: Sphinx, page_name: str, template_name: str, context: dict[str, ...], doctree: document):
    if 'body' in context:
        context['body'] = re.sub(
            r'<span class=\"sig-prename descclassname\">'
            r'<span class=\"pre\">'
            r'nuoyanlib\.(client|server|utils)\.'
            r'</span></span>',
            "",
            context['body'],
        )
    # global b
    # b += 1
    # if b == 10:
    #     for i in context.items():
    #         print(i)


def setup(app: Sphinx):
    app.connect("builder-inited", builder_inited)
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    app.connect("autodoc-skip-member", autodoc_skip_member)
    app.connect("html-page-context", html_page_context)













