# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN AS IS BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-05
#
# ====================================================


import shutil
import os
import sys
import json


core_files = [
    "__init__.py",
    "_const.py",
    "_const.pyi",
    "_sys.py",
    "_sys.pyi",
    "_typing.pyi",
    "_utils.py",
    "_utils.pyi",
]
copy_res = [
    "GameTick",
    "ItemGrid",
]


def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def copy_folder(src, dest):
    shutil.copytree(src, dest)

def copy_file(src, dest):
    shutil.copyfile(src, dest)


cwd = os.getcwd()
root_path = "\\".join(cwd.split("\\")[:-2])
dest_path = r"%s\release\nuoyanlib" % root_path
delete_folder(dest_path)
copy_folder("nuoyanlib", dest_path)

copy_folder(r"%s\nuoyanlib\client" % root_path, dest_path + r"\behavior_packs\nuoyanlibBeh\nuoyanlib\client")
copy_folder(r"%s\nuoyanlib\server" % root_path, dest_path + r"\developer_mods\nuoyanlibDev\nuoyanlib\server")
copy_folder(r"%s\nuoyanlib\utils" % root_path, dest_path + r"\behavior_packs\nuoyanlibBeh\nuoyanlib\utils")
copy_folder(r"%s\nuoyanlib\utils" % root_path, dest_path + r"\developer_mods\nuoyanlibDev\nuoyanlib\utils")
copy_folder(r"%s\nuoyanlib\_core\_client" % root_path, dest_path + r"\behavior_packs\nuoyanlibBeh\nuoyanlib\_core\_client")
copy_folder(r"%s\nuoyanlib\_core\_server" % root_path, dest_path + r"\developer_mods\nuoyanlibDev\nuoyanlib\_core\_server")

for f in core_files:
    p = r"%s\nuoyanlib\_core\%s" % (root_path, f)
    copy_file(p, dest_path + r"\developer_mods\nuoyanlibDev\nuoyanlib\_core\%s" % f)
    copy_file(p, dest_path + r"\behavior_packs\nuoyanlibBeh\nuoyanlib\_core\%s" % f)
root_init_path = r"%s\nuoyanlib\__init__.py" % root_path
copy_file(root_init_path, dest_path + r"\developer_mods\nuoyanlibDev\nuoyanlib\__init__.py")
copy_file(root_init_path, dest_path + r"\behavior_packs\nuoyanlibBeh\nuoyanlib\__init__.py")


dest_ui_def = {'ui_defs': []}
for res in copy_res:
    res_src_dir = root_path + r"\ui\%s" % res
    for root, dirs, files in os.walk(res_src_dir, True):
        for f in files:
            if f.endswith(".md"):
                continue
            fp = root + r"\%s" % f
            dp = dest_path + r"\resource_packs\nuoyanlibRes" + fp.replace(res_src_dir, "")
            if f == "_ui_defs.json":
                with open(fp, "r") as file_:
                    src_ui_def = json.load(file_)['ui_defs']
                    dest_ui_def['ui_defs'].extend(src_ui_def)
            elif os.path.exists(dp):
                print >> sys.stderr, "[Res Conflict] " + fp
            else:
                dir_name = os.path.dirname(dp)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                copy_file(fp, dp)
with open(dest_path + r"\resource_packs\nuoyanlibRes\ui\_ui_defs.json", "w") as file_:
    json.dump(dest_ui_def, file_, indent=4, separators=(", ", ": "), sort_keys=True)


for root, dirs, files in os.walk(dest_path):
    for f in files:
        if not f.endswith(".py") and not f.endswith(".pyi"):
            continue
        if f == "modMain.py":
            continue
        fp = root + r"\%s" % f
        src_path = root_path + r"\%s\%s" % (root[root.rindex("nuoyanlib"):], f)
        with open(fp, "r") as file_:
            content = file_.read()
        with open(src_path, "r") as file_:
            src_content = file_.read()
        if content != src_content:
            print >> sys.stderr, "[Diff] " + fp


import _version








