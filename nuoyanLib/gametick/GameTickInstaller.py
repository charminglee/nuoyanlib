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
#   Last Modified : 2023-01-15
#
# ====================================================


import json
import re
import tkFileDialog
import tkMessageBox
import os


gameTickJson = {
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


path = "/".join(re.split("[\\\\/]", __file__))
initialDir = "/".join(path.split("/")[:-4])
manifestPath = ""
rpPath = ""
while not manifestPath:
    rpPath = tkFileDialog.askdirectory(initialdir=initialDir, title="请选择您的资源包（resource_pack）根目录并点击确认：")
    if rpPath:
        print "选择目录：" + str(rpPath)
    try:
        for fileName in os.walk(rpPath).next()[2]:
            if "manifest" in fileName:
                manifestPath = rpPath + "/" + fileName
                break
        else:
            print "资源包打开失败。"
            tkMessageBox.showwarning("资源包打开失败", "该目录下找不到manifest清单文件，请重新选择！")
    except StopIteration:
        print "程序退出。"
        break
    if manifestPath:
        print "找到清单文件：" + str(manifestPath)
        try:
            manifestDict = json.load(open(manifestPath))
        except:
            print "ERROR: 清单文件解析失败！"
            raise
        isRp = (manifestDict['modules'][0]['type'] == "resources")
        if isRp:
            print "确认资源包路径。"
        else:
            print "资源包打开失败。"
            tkMessageBox.showwarning("资源包打开失败", "该目录不是资源包，请选择资源包根目录！")
            manifestPath = ""


if manifestPath:
    print "开始安装GameTick模块"
    try:
        print "正在写入_GameTick.json..."
        gtPath = rpPath + "/ui/_GameTick.json"
        f = open(gtPath, "w+")
        f.write(json.dumps(gameTickJson, indent=4))
        f.close()
        print "_GameTick.json写入成功！"
        print "正在写入_ui_defs.json..."
        defsPath = rpPath + "/ui/_ui_defs.json"
        if os.path.exists(defsPath):
            defsDict = json.load(open(defsPath))
            defs = "ui/_GameTick.json"
            if defs not in defsDict['ui_defs']:
                defsDict['ui_defs'].append(defs)
                f = open(defsPath, "w+")
                f.write(json.dumps(defsDict, indent=4))
                f.close()
        else:
            f = open(defsPath, "w+")
            f.write(json.dumps(gameTickJson, indent=4))
            f.close()
        print "_ui_defs.json写入成功！"
    except:
        print "ERROR: GameTick模块安装失败！"
        raise
    print "=" * 50
    print "GameTick模块已完成安装！"















