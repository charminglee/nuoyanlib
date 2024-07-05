# -*- coding: utf-8 -*-


import os
import sys


# 程序运行配置------------------------------------------------------------------------------------------------------------

# 是否清理行为包/资源包图标文件
clearIcon = True
# 是否清理编辑器数据文件
clearMcsFiles = True
# 保留以下空文件夹
ignoreDirs = [
    "entities",
    "Presets",
    "textures",
]
# 保留以下文件
ignoreFiles = [
    # "blocks.json",
    # "terrain_texture.json",
    # "netease_models.json",
    # "invisible_bind_skeleton.json",
    # "_bind.json",
    # "_effect.json",
]

# ----------------------------------------------------------------------------------------------------------------------


cwd = os.getcwd()
path = ""
for dn in os.listdir(cwd):
    p = os.path.join(cwd, dn)
    if os.path.isdir(p):
        for i in os.listdir(p):
            if "BehaviorPack" in i:
                path = p
                break
    if path:
        break
if not path:
    sys.exit(0)


mcsFiles = [
    "editor.name",
    "studio.json",
    "work.mcscfg",
]
clearPng = [
    "custom_sun.png",
    "sun.png",
    "custom_brah.png",
    "custom_dirt.png",
    "custom_apple.png",
    "brah.png",
]
iconFiles = [
    "pack_icon.jpg",
]
checkClear = {
    'blocks.json': ("{\n"
                    "    \"format_version\": [\n"
                    "        1,\n"
                    "        1,\n"
                    "        0\n"
                    "    ]\n"
                    "}"),
    'terrain_texture.json': ("{\n"
                             "    \"resource_pack_name\": \"vanilla\",\n"
                             "    \"texture_data\": {\n"
                             "\n"
                             "    },\n"
                             "    \"texture_name\": \"atlas.terrain\"\n"
                             "}"),
    'netease_models.json': ("{\n"
                            "\n"
                            "}"),
    'invisible_bind_skeleton.json': ("{\n"
                                     "    \"skeleton\": [\n"
                                     "        {\n"
                                     "            \"name\": \"root\",\n"
                                     "            \"parent\": \"root\",\n"
                                     "            \"initpos\": [\n"
                                     "                0.0,\n"
                                     "                0.0,\n"
                                     "                -0.0\n"
                                     "            ],\n"
                                     "            \"initquaternion\": [\n"
                                     "                -0.0000016026669982238673,\n"
                                     "                -0.0000015070728522914579,\n"
                                     "                0.697554349899292,\n"
                                     "                0.7165318727493286\n"
                                     "            ],\n"
                                     "            \"initscale\": [\n"
                                     "                1.0,\n"
                                     "                1.0,\n"
                                     "                1.0\n"
                                     "            ],\n"
                                     "            \"offmtx\": [\n"
                                     "                [\n"
                                     "                    0.026835869997739793,\n"
                                     "                    0.9996398091316223,\n"
                                     "                    -1.1985919456947159e-7,\n"
                                     "                    -2.22485263889673e-17\n"
                                     "                ],\n"
                                     "                [\n"
                                     "                    -0.9996398091316223,\n"
                                     "                    0.026835869997739793,\n"
                                     "                    -0.000004400427314976696,\n"
                                     "                    -8.168171115038121e-16\n"
                                     "                ],\n"
                                     "                [\n"
                                     "                    -0.000004395626092446037,\n"
                                     "                    2.3790533987266827e-7,\n"
                                     "                    1.0,\n"
                                     "                    1.856222120455442e-10\n"
                                     "                ]\n"
                                     "            ]\n"
                                     "        }\n"
                                     "    ],\n"
                                     "    \"boundingbox\": [\n"
                                     "        [\n"
                                     "            -0.007048234809190035,\n"
                                     "            -7.17939763195119e-10,\n"
                                     "            -0.012045030482113362\n"
                                     "        ],\n"
                                     "        [\n"
                                     "            0.007048234809190035,\n"
                                     "            0.01892676018178463,\n"
                                     "            0.012045029550790787\n"
                                     "        ]\n"
                                     "    ]\n"
                                     "}"),
    '_bind.json': ("{\n"
                   "    \"version\": \"1.2.0\",\n"
                   "    \"description\": {\n"
                   "        \"file_type\": \"bind\",\n"
                   "        \"model\": \"\",\n"
                   "        \"model_type\": \"\"\n"
                   "    },\n"
                   "    \"model\": {\n"
                   "        \"\": {\n"
                   "            \"bind\": {\n"
                   "                \"default\": {}\n"
                   "            },\n"
                   "            \"animation\": {\n"
                   "                \"\": \"default\"\n"
                   "            },\n"
                   "            \"sounds\": {\n"
                   "                \"default\": []\n"
                   "            },\n"
                   "            \"animation_speed\": {}\n"
                   "        }\n"
                   "    },\n"
                   "    \"editor\": {\n"
                   "        \"show\": {\n"
                   "            \"default\": true\n"
                   "        }\n"
                   "    }\n"
                   "}"),
    '_effect.json': ("{\n"
                     "    \"effect\": [\n"
                     "\n"
                     "    ],\n"
                     "    \"model\": [\n"
                     "        {\n"
                     "            \"animation\": {\n"
                     "\n"
                     "            },\n"
                     "            \"name\": \"\",\n"
                     "            \"type\": \"model\"\n"
                     "        }\n"
                     "    ]\n"
                     "}"),
}


def message(p):
    print "[DELETE] ..." + p[len(path):]


for root, dirs, files in os.walk(path, topdown=False):
    for fn in files:
        if fn in ignoreFiles:
            continue
        filePath = root + "\\" + fn
        if fn in checkClear:
            with open(filePath, "r") as f:
                c = f.read()
            if c == checkClear[fn]:
                os.remove(filePath)
                message(filePath)
        elif (clearIcon and fn in iconFiles) \
                or (clearMcsFiles and (fn in mcsFiles or ".mcs" in root)) \
                or fn in clearPng:
            os.remove(filePath)
            message(filePath)
    dirName = root.split("\\")[-1]
    if dirName not in ignoreDirs and not os.listdir(root):
        os.rmdir(root)
        message(root)


















