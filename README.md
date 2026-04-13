<div align="center">
   <img src="/img/logo/logo2.png" alt="logo">

   ---

   <h3>基于网易我的世界ModSDK的Mod开发工具库</h3>

   [![license](https://img.shields.io/github/license/charminglee/nuoyanlib.svg)](LICENSE) [![modsdk](https://img.shields.io/badge/ModSDK-3.6-green)](https://mc.163.com/dev/index.html) ![release](https://img.shields.io/github/release/charminglee/nuoyanlib.svg)  
   ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/charminglee/nuoyanlib) ![GitHub repo size](https://img.shields.io/github/repo-size/charminglee/nuoyanlib) [![github](https://img.shields.io/badge/-GitHub-black?style=flat&logo=github)](https://github.com/charminglee/nuoyanlib) [![gitee](https://img.shields.io/badge/-gitee-red?style=flat&logo=gitee)](https://gitee.com/charming-lee/nuoyanLib)

   [入门指南](/docs/source/getting_started.rst) ● [API文档]() ● [QQ群]()
</div>

<br>
<br>
<br>

> [!NOTE]  
> 目前该项目仍处于开发和测试阶段，一些功能仍未开发完善或存在未知bug，且其中的函数命名、具体实现等随时可能发生变化，请谨慎使用。

## 📖 简介

「nuoyanlib」是基于网易我的世界（我的世界中国版）[ModSDK](https://mc.163.com/dev/index.html)的开发工具库，封装了许多常用的客户端/服务端工具和通用算法，帮助开发者更高效地实现复杂功能。  
您无需对现有的代码结构作任何修改，即可轻松引入「nuoyanlib」。  

> ✅ 已支持 **ModSDK 3.8**  
> 📌 适合**个人**或**团队**项目，可自由用于**商业**和**非商业**用途

<br>

## ✨ 亮点

- [`nuoyanlib.client`](/docs/source/api/client.rst)：客户端工具包，提供了NyUI框架、容器UI框架、特效管理、渲染、运镜工具等实用工具。  


- [`nuoyanlib.server`](/docs/source/api/server.rst)：服务端工具包，提供了实体工具、伤害工具等实用工具。


- [`nuoyanlib.common`](/docs/source/api/utils.rst)：通用工具包，提供了事件监听框架、多种与MC密切相关的数学计算函数、向量工具、双端通信工具、随机数工具等实用工具。

<br>

## ⬇️ 下载

- ~~[1.0.0-beta.1]()~~
- [开发版](https://codeload.github.com/charminglee/nuoyanlib/zip/refs/heads/master)

<br>

## 🚀 快速上手

1. 解压下载的压缩包，将`nuoyanlib`文件夹放至行为包Python脚本根目录下（即`modMain.py`文件所在位置）。安装好后，你的行为包结构应为： 

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

3. 在业务代码中导入「nuoyanlib」，其中`<scripts_root>`是你的Python脚本根目录名称：
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
    from <scripts_root>.nuoyanlib.server import (
        CF,          
        LvComp,      
        event,       
    )
    ```
   
    #### 调用示例
   
    假设你已经按照以上方法导入了「nuoyanlib」，对于所有「nuoyanlib」中的公开函数，都可通过`nyl.<func_name>`进行调用，例如：

    ```python
    entity_list = nyl.get_all_entities()
    ```
   
    需要注意的是，`nuoyanlib.client`为客户端工具包，其中的函数只能在客户端环境使用；`nuoyanlib.server`同理，只能在服务端环境使用；`nuoyanlib.common`则无环境限制，双端均可使用。

> [!WARNING]  
> 为确保环境安全，请勿将客户端和服务端代码写在同一个py文件内，且**禁止**跨端导入（如在客户端导入服务端库，在服务端导入客户端库），如果你强制这么做，「nuoyanlib」将抛出`AcrossImportError`。

4. 更多信息详见[入门指南](/docs/source/getting_started.rst)。

<br>

## 🔍 参考文档

作者正在熬夜编写中......

<br>

## 🎉 更新信息

作者正在熬夜编写中......

<br>

## 🌞 未来计划

- [ ] 重新整理文档注释，完成参考文档的编写
- [ ] 编写测试包
- [ ] 编写demo
- [ ] 发布1.0第一个测试版
- [ ] 搭建项目网站
- [ ] ...

<br>

## 👑 贡献

如果您有更好的算法或修改建议，欢迎通过Issue或PR的方式提交，为MC Mod社区的健康发展助一份力！

<br>

## 🌹 特别鸣谢

1. [创新工坊-小坊](https://github.com/cxgf666)：发现了[`spawn_ground_shatter_effect()`](https://github.com/charminglee/nuoyanlib/blob/03d9efb26a3f3cf4f93f786ae1779dc6f8e26b7c/src/nuoyanlib/server/block.py#L41)的一个bug；「nuoyanlib」内测用户。
2. [xiaoweii](https://github.com/645359132)：「nuoyanlib」内测用户。
3. [幻尘](https://github.com/HuanChen19)：「nuoyanlib」内测用户。

<br>

## 🔗 作者的其他项目

- [网易我的世界ModSDK补全库修正版](https://github.com/charminglee/mc-netease-sdk-nyrev)

<br>

## 👴 联系作者

如果在使用过程中遇到问题，可通过以下方式联系作者，作者将尽全力为你解答。

- QQ：[1279735247](https://qm.qq.com/q/BknsDqOdsk)
- 邮箱：1279735247@qq.com