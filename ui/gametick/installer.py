# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-31
#
# ====================================================


"""
请使用Python2运行。
"""


import json
import re
import tkFileDialog
import tkMessageBox
import os


gt_ui_json = {
    'main': {
        'bindings': [
            {
                'binding_condition': "always",
                'binding_name': "#main.gametick"
            }
        ],
        'type': "screen"
    },
    'namespace': "_GameTick"
}
gt_def = "ui/_GameTick.json"
gt_def_json = {
    'ui_defs': [
        "ui/_GameTick.json"
    ]
}


path = "/".join(re.split(r"[\\/]", __file__))
initial_dir = "/".join(path.split("/")[:-4])
manifest_path = ""
rp_path = ""
while not manifest_path:
    rp_path = tkFileDialog.askdirectory(initialdir=initial_dir, title="请选择您的资源包（resource_pack）根目录并点击确认：")
    if rp_path:
        print "选择目录：" + str(rp_path)
    try:
        for file_name in os.walk(rp_path).next()[2]:
            if "manifest" in file_name:
                manifest_path = rp_path + "/" + file_name
                break
        else:
            print "ERROR: 资源包打开失败。"
            tkMessageBox.showwarning("资源包打开失败", "该目录下找不到manifest清单文件，请重新选择！")
    except StopIteration:
        print "ERROR: 程序退出。"
        break
    if manifest_path:
        print "找到清单文件：" + str(manifest_path)
        try:
            with open(manifest_path) as f:
                manifest_dict = json.load(f)
        except:
            print "ERROR: 清单文件解析失败！"
            raise
        is_rp = (manifest_dict['modules'][0]['type'] == "resources")
        if is_rp:
            print "确认资源包路径。"
        else:
            print "ERROR: 资源包打开失败。"
            tkMessageBox.showwarning("资源包打开失败", "该目录不是资源包，请选择资源包根目录！")
            manifest_path = ""


if manifest_path:
    print "开始安装GameTick模块"
    try:
        print "正在写入_GameTick.json..."
        gt_path = rp_path + "/ui/_GameTick.json"
        with open(gt_path, "w+") as f:
            f.write(json.dumps(gt_ui_json, indent=4))
        print "_GameTick.json写入成功！"
        print "正在写入_ui_defs.json..."
        defs_path = rp_path + "/ui/_ui_defs.json"
        if os.path.exists(defs_path):
            with open(defs_path, "w+") as f:
                defs_dict = json.load(f)
                if gt_def not in defs_dict['ui_defs']:
                    defs_dict['ui_defs'].append(gt_def)
                    f.write(json.dumps(defs_dict, indent=4))
        else:
            with open(defs_path, "w") as f:
                f.write(json.dumps(gt_def_json, indent=4))
        print "_ui_defs.json写入成功！"
    except:
        print "ERROR: GameTick模块安装失败！"
        raise
    print "=" * 50
    print "GameTick模块已完成安装！"















