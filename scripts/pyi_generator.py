# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-26
|
| ==============================================
"""


import os
import datetime


py_path = input("file: ")
pyi_path = py_path + "i"
py_content = ""
pyi_content = ""


if os.path.exists(pyi_path):
    with open(pyi_path, encoding="utf-8") as f:
        pyi_content = f.read()


if not pyi_content:
    today = datetime.date.today()
    pyi_content = (
        "# -*- coding: utf-8 -*-\n"
        "\"\"\"\n"
        "| ==============================================\n"
        "|\n"
        "|   Copyright (c) 2025 Nuoyan\n"
        "|\n"
        "|   Author: Nuoyan\n"
        "|   Email : 1279735247@qq.com\n"
        "|   Gitee : https://gitee.com/charming-lee\n"
        "|   Date  : %s\n"
        "|\n"
        "| ==============================================\n"
        "\"\"\"\n"
        % today.strftime("%Y-%m-%d")
    )


def add_typing(typ):
    global pyi_content
    if "typing" not in pyi_content:
        idx = pyi_content.index('"""', 30)
        pyi_content = pyi_content[:idx + 6] + "from typing import {}\n".format(typ) + pyi_content[idx + 6:]
    else:
        start = pyi_content.index("typing")
        end = pyi_content.index("\n", start)
        if typ not in pyi_content[start: end]:
            pyi_content = pyi_content[:end] + ", {}".format(typ) + pyi_content[end:]


in_class = False
in_func = False
with open(py_path, encoding="utf-8") as f:
    while line := f.readline():
        if line.startswith("def __test__():"):
            continue
        if (
                line.startswith("class")
                or line.startswith("@")
                or line.startswith("    @")
        ):
            pyi_content += line
        elif (
                line.startswith("def")
                or line.startswith("    def")
        ):
            pyi_content += line[:-1] + " ...\n"


with open(pyi_path, "w+", encoding="utf-8") as f:
    f.write(pyi_content)














