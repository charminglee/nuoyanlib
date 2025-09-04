<div align="center">

[//]: # (  <br>)

[//]: # (  <img src="/img/diamond_sword.png" alt="diamond_sword" width=64 height=64>)

  <img src="/img/logo/logo2.png" alt="logo">
  
  ---

  <h3>基于网易我的世界ModSDK的Mod开发工具库</h3>

  [![license](https://img.shields.io/github/license/charminglee/nuoyanlib.svg)](LICENSE) [![modsdk](https://img.shields.io/badge/ModSDK-3.5-green)](https://mc.163.com/dev/index.html) ![release](https://img.shields.io/github/release/charminglee/nuoyanlib.svg) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/charminglee/nuoyanlib) ![GitHub repo size](https://img.shields.io/github/repo-size/charminglee/nuoyanlib)  
  [![python](https://camo.githubusercontent.com/61a81b1dbe844fb6b43df995ae0b9b118c641df75220b27281aad6ea97e46622/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f7374796c653d666c6174266c6f676f3d507974686f6e266c6f676f436f6c6f723d666666666666)](https://www.python.org/) [![pycharm](https://img.shields.io/badge/-JetBrains%20PyCharm-black?style=flat&logo=pycharm)](https://www.jetbrains.com/pycharm/) [![github](https://img.shields.io/badge/-GitHub-black?style=flat&logo=github)](https://github.com/charminglee/nuoyanlib) [![gitee](https://img.shields.io/badge/-gitee-red?style=flat&logo=gitee)](https://gitee.com/charming-lee/nuoyanLib) [![qq](https://img.shields.io/badge/QQ-1279735247-green)](https://qm.qq.com/q/BknsDqOdsk)

</div>

<br>
<br>
<br>

> [!NOTE]  
> 目前该项目仍处于开发和测试阶段，一些功能仍未开发完善或存在未知bug，且其中的函数命名、具体实现等随时可能发生变化，请谨慎使用。

## 📖 简介 | Introduction

「nuoyanlib」是基于网易我的世界[ModSDK](https://mc.163.com/dev/index.html)的开发工具库，封装了许多常用的客户端、服务端工具和通用算法，帮助开发者更高效地实现复杂功能。  
您无需对现有的代码结构作任何修改，即可轻松引入「nuoyanlib」。  

> ✅ 已支持 **ModSDK 3.5**  
> 📌 适合**个人**或**团队**项目，可自由用于**商业**和**非商业**用途

<br>

## ✨ 亮点 | Features

- [**client（客户端库）**](/nuoyanlib/client)  
  提供了客户端扩展、特效管理器等客户端专用工具以及ScreenNode扩展、物品网格管理器等UI专用工具。  


- [**server（服务端库）**](/nuoyanlib/server)  
  提供了服务端扩展、实体获取、实体操作、范围伤害、背包管理等服务端专用工具。


- [**utils（通用工具库）**](/nuoyanlib/utils)  
  提供了多种数学计算函数、更多的枚举值等双端通用的工具。

<br>

## ⬇️ 下载 | Download

- [1.0.0-beta.1](https://gitee.com/charming-lee/nuoyanLib/releases/tag/1.0.0-beta.1)

<br>

## 🚀 开始 | Getting Started

1. 解压下载的压缩包，将`nuoyanlib`文件夹放至行为包Python脚本根目录下（即`modMain.py`文件所在位置）。  
    安装好后，你的行为包结构应为： 

    ```
    行为包/  
    ├── entities/  
    ├── 脚本根目录/  
    │   ├── nuoyanlib/  
    │   │   ├── _core/  
    │   │   ├── client/  
    │   │   ├── server/  
    │   │   ├── utils/  
    │   │   ├── __init__.py  
    │   │   ├── config.py  
    │   │   └── LICENSE  
    │   ├── __init__.py  
    │   ├── modMain.py  
    │   ...  
    ...
    ```

2. 在`modMain.py`中添加以下代码以启动「nuoyanlib」：

    ```python
    import nuoyanlib
    nuoyanlib.run(globals())
    ```

    例如：

    ```python
    from mod.common.mod import Mod
    import mod.client.extraClientApi as client_api
    import mod.server.extraServerApi as server_api
   
   
    import nuoyanlib
    nuoyanlib.run(globals())


    @Mod.Binding(name="MyMod", version="1.0.0")
    class ModMain(object):
        @Mod.InitServer()
        def init_server(self):
            server_api.RegisterSystem("MyMod", "MyServerSystem", "myScripts.myServerSystem.MyServerSystem")
    
        @Mod.InitClient()
        def init_client(self):
            client_api.RegisterSystem("MyMod", "MyClientSystem", "myScripts.myClientSystem.MyClientSystem")
    ```

3. 之后，在你的业务代码中导入「nuoyanlib」即可使用，推荐使用以下方式进行导入，其中`<scripts_root>`是你的Python脚本根目录名称：
    #### 导入客户端库

    ```python
    import <scripts_root>.nuoyanlib.client as nyl
   
    # 导入常用工具
    from <scripts_root>.nuoyanlib.client import (
        PLAYER_ID,   
        CF,          
        PlrComp,     
        LvComp,      
        event,       
    )
    ```

    #### 导入服务端库

    ```python
    import <scripts_root>.nuoyanlib.server as nyl
   
    # 导入常用工具
    from <scripts_root>.nuoyanlib.client import (
        CF,          
        LvComp,      
        event,       
    )
    ```
   
    #### 调用「nuoyanlib」函数

    ```python
    nyl.pos_distance(pos1, pos2)
    ```

> [!WARNING]  
> 为确保环境安全，请勿将客户端和服务端代码写在同一个py文件内，且**禁止**跨端导入（如在客户端导入服务端库，在服务端导入客户端库），如果你强制这么做，「nuoyanlib」将抛出`AcrossImportError`。

4. 更多信息详见[入门指南](/docs/入门指南.md)。

<br>

## 🔍 参考文档 | Documentation

作者正在熬夜编写中......

<br>

## 🎉 更新信息 | Changelog

作者正在熬夜编写中......

<br>

## 🌞 未来计划 | TODO

- [ ] 重新整理文档注释，完成参考文档的编写
- [ ] 编写测试包
- [ ] 编写demo
- [ ] 发布1.0第一个测试版
- [ ] 搭建项目网站
- [ ] ...

<br>

## 👑 贡献 | Contributing

如果您有更好的算法或修改建议，欢迎通过Issue或PR的方式提交，为MC Mod社区的健康发展助一份力！

<br>

## 👴 联系作者 | Contact

如果在使用过程中遇到问题，可通过以下方式联系作者：

- QQ：[1279735247](https://qm.qq.com/q/BknsDqOdsk)
- 邮箱：1279735247@qq.com