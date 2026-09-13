<div align="center">
   <img src="/img/logo/logo2.png" alt="logo">

   ---

   <h3>基于网易我的世界 [ModSDK](https://mc.163.com/dev/index.html) 的 Mod 开发工具库</h3>

   [![license](https://img.shields.io/github/license/charminglee/nuoyanlib.svg)](LICENSE) [![modsdk](https://img.shields.io/badge/ModSDK-3.9-green)](https://mc.163.com/dev/index.html) ![release](https://img.shields.io/github/release/charminglee/nuoyanlib.svg)  
   ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/charminglee/nuoyanlib) ![GitHub repo size](https://img.shields.io/github/repo-size/charminglee/nuoyanlib) [![github](https://img.shields.io/badge/-GitHub-black?style=flat&logo=github)](https://github.com/charminglee/nuoyanlib) [![gitee](https://img.shields.io/badge/-gitee-red?style=flat&logo=gitee)](https://gitee.com/charming-lee/nuoyanLib)

   [入门指南](/docs/source/getting_started.rst) ● [开发指南](/docs/dev/开发指南.md) ● [API文档]() ● [QQ群]()
</div>

<br>
<br>
<br>

> [!NOTE]  
> 目前该项目仍处于开发和测试阶段，一些功能仍未开发完善或存在未知 bug ，且其中的函数命名、具体实现等随时可能发生变化，请谨慎使用。

## 📖 简介

「nuoyanlib」是基于网易我的世界（我的世界中国版） [ModSDK](https://mc.163.com/dev/index.html) 的开发工具库，封装了许多常用的客户端 / 服务端工具和通用算法，帮助开发者更高效地实现复杂功能。

「nuoyanlib」主要包含以下三个工具库：

- [`nuoyanlib.client`](/docs/source/api/client.rst) ：客户端工具包，提供了 NyUI 声明式 UI 框架、容器 UI 框架、特效管理、渲染、运镜工具等实用工具。  


- [`nuoyanlib.server`](/docs/source/api/server.rst) ：服务端工具包，提供了实体工具、伤害工具等实用工具。


- [`nuoyanlib.common`](/docs/source/api/utils.rst) ：通用工具包，提供了事件监听框架、多种与MC密切相关的数学计算函数、向量工具、双端通信工具、随机数工具等实用工具。

## 🛠️ 安装

### 使用 nuoyanlib-installer 一键安装

下载 [nuoyanlib-installer]() ，选择要安装的脚本文件夹后点击安装即可。

### 手动安装

1. 下载「nuoyanlib」压缩包：

   - ~~[1.0.0-beta.1]()~~
   - [开发版](https://codeload.github.com/charminglee/nuoyanlib/zip/refs/heads/master)

2. 解压后将 `nuoyanlib` 文件夹复制到行为包 Python 脚本根目录下（即 `modMain.py` 所在位置）。安装好后，你的行为包结构应与下方类似： 

    ```
    行为包/  
    ├── entities/  
    ├── 脚本根目录/  
    │   ├── nuoyanlib/  
    │   │   ├── _core/  
    │   │   ├── client/  
    │   │   ├── server/  
    │   │   ├── common/  
    │   │   ├── __init__.py  
    │   │   ├── config.py  
    │   │   └── LICENSE  
    │   ├── __init__.py  
    │   ├── modMain.py  
    │   ...  
    ...
    ```

## 🚀 快速上手

1. 在 `modMain.py` 中添加模组启动逻辑：

    ```python
    from mod.common.mod import Mod
    import mod.client.extraClientApi as client_api
    import mod.server.extraServerApi as server_api
   
   
    import nuoyanlib
    nuoyanlib.run(
        "MyMod"
        clients=[
            ("MyClientSystem", "my_scripts.my_client_system"),
            ("MyScreen", "my_scripts.ui.my_screen"),
        ],
        servers=[
            ("MyServerSystem", "my_scripts.my_server_system"),
        ]
    )
    ```
   
   [`nuoyanlib.run()`](https://github.com/charminglee/nuoyanlib/blob/feac9641c9ddeeaee82e7dce8707240d5ab173f7/src/nuoyanlib/__init__.py#L121) 的第一个参数为模组名称； `clients` / `servers` 参数需通过关键字形式传入，请在这两个参数中列出所有需要加载的客户端/服务端模块的名称（需保证在当前模组中唯一）和路径（注意是模块路径，无需写到类名）。
   
   模块按列表顺序加载。一般情况下，不需要列出每一个模块的路径，只需列出客户端/服务端的入口模块和其他需要主动加载的模块（如 UI 模块）。

> [!NOTE]
> 如果你还使用了其他带有类似启动逻辑的框架（如 [QuModLibs](https://qumod.cc/) ），也需保留该框架的启动逻辑。

2. 「nuoyanlib」导入和调用示例：

    #### 导入客户端库

    ```python
    # 写法一
    # 将 <scripts_root> 替换成你具体的 Python 脚本根目录名称
    import <scripts_root>.nuoyanlib.client as nyl
    ```
    
    ```python
    # 写法二
    # 使用相对导入，具体写法需根据模块实际路径而定，如不熟悉相对导入建议使用第一种写法
    # 例如模块： my_scripts/ui/my_screen.py
    from ..nuoyanlib import client as nyl
    ```

    #### 导入服务端库
   
    写法同上。

    ```python
    import <scripts_root>.nuoyanlib.server as nyl
    ```
    
    ```python
    from ..nuoyanlib import server as nyl
    ```

> [!NOTE]
> `client` / `server` 库已包含 `common` 库，因此无需单独导入 `nuoyanlib.common` 。

    #### 调用示例
   
    假设你已经按照以上方法导入了「nuoyanlib」，对于所有「nuoyanlib」中的公开接口，都可通过 `nyl.<func_name>` 进行调用，例如：

    ```python
    entity_list = nyl.get_all_entities()
    ```
   
   如果你不想每次都编写 `nyl.` 前缀，也可以直接导入你需要的接口：
   
    ```python
    from <scripts_root>.nuoyanlib.client import get_all_entities
    ```
   
    需要注意的是， `nuoyanlib.client` 为客户端工具包，其中的函数只能在客户端环境使用； `nuoyanlib.server` 同理，只能在服务端环境使用； `nuoyanlib.common` 则无环境限制，双端均可使用。

> [!WARNING]  
> 为确保环境安全，请勿将客户端和服务端代码写在同一个py文件内，且**禁止**跨端导入（如在客户端导入服务端库，在服务端导入客户端库）。如果你强制这么做，「nuoyanlib」将抛出 `AcrossImportError` 。

3. 更多信息详见[入门指南](/docs/source/getting_started.rst)。

## 🔍 参考文档

作者正在熬夜编写中......

## 🌞 未来计划

- [ ] 重新整理文档注释，完成参考文档的编写
- [ ] 编写测试包
- [ ] 编写 Demo
- [ ] 发布 1.0 第一个测试版
- [ ] 搭建项目网站
- [ ] ...

## 🧾 开源许可

本项目使用 [BSD-3-Clause](https://opensource.org/license/bsd-3-clause) 许可，允许用于商业项目，允许以修改或未修改的形式进行再发布，仅保留以下两个权利：

- 保留许可证的可读副本
- 保留「nuoyanlib」源代码中的版权声明

## 👑 贡献

「nuoyanlib」欢迎广大 MC 开发者参与开发，不管你是想提出修改建议、算法建议，还是接口需求，都可通过 Issue 或 PR 的方式提交，共同构建一个更现代化的 MC Mod 框架！

开发指南详见： [「nuoyanlib」开发指南](/docs/dev/开发指南.md)

如果你可以给本项目点个 Star ，那将是对作者最大的鼓励，也不失为一种贡献！

## 🌹 特别鸣谢

1. [创新工坊-小坊](https://github.com/cxgf666) ：发现了 [`spawn_ground_shatter_effect()`](https://github.com/charminglee/nuoyanlib/blob/03d9efb26a3f3cf4f93f786ae1779dc6f8e26b7c/src/nuoyanlib/server/block.py#L41) 的一个bug；「nuoyanlib」内测用户。
2. [xiaoweii](https://github.com/645359132) ：「nuoyanlib」内测用户。
3. [幻尘](https://github.com/HuanChen19) ：「nuoyanlib」内测用户。

## 🔗 作者的其他项目

- [网易我的世界 ModSDK 补全库修正版](https://github.com/charminglee/mc-netease-sdk-nyrev)
