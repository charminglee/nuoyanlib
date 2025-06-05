<h1 align="center" style="line-height: 0;">「nuoyanlib」</h1>
<h1 align="center" style="line-height: 0;">🐱</h1>
<h1 align="center" style="line-height: 0;">基于ModSDK的开发工具库</h1>
<h2 align="center" style="line-height: 0.5;">v0.9.3-beta</h2>

<br></br>

<br></br>

## 💼 介绍

---

> **[注意]**  
目前该项目仍处于测试阶段，部分功能仍未开发完成或存在未知bug，且其中的函数命名、具体实现等随时可能发生变化，请谨慎使用。

「nuoyanlib」是基于我的世界中国版[ModSDK](https://mc.163.com/dev/index.html)开发的开源工具库，封装了许多开发中常用的功能算法，致力于为广大开发者提高代码编写效率，更轻松地实现复杂效果。  
「nuoyanlib」可供大家学习参考，也可应用于任何个人/团队的商业/非商业项目中。  
您无需对现有的代码结构作任何修改，即可轻松引入「nuoyanlib」。  

#### **兼容ModSDK版本：3.4及以下**

<br></br>

## ✨ 亮点

---

- [**client（客户端库）**](/nuoyanlib/client)  
  提供了客户端扩展、特效管理器等客户端专用工具以及ScreenNode扩展、物品网格管理器等UI专用工具。  


- [**server（服务端库）**](/nuoyanlib/server)  
  提供了服务端扩展、实体获取、实体操作、范围伤害、背包管理等服务端专用工具。


- [**utils（通用工具库）**](/nuoyanlib/utils)  
  提供了多种数学计算函数、更多的枚举值等双端通用的工具。

<br></br>

## ⬇️ 下载

---

- [v0.6.0-beta](https://gitee.com/charming-lee/nuoyanLib/releases/tag/v0.6.0-beta)

<br></br>

## ⚙️ 配置

---

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
3. 之后，在需要时导入「nuoyanlib」即可，推荐使用以下方式进行导入，其中`<scripts_root>`是你的Python脚本根目录名称：
   #### 导入客户端库
    ```python
    import <scripts_root>.nuoyanlib.client as nyl
    ```
   #### 导入服务端库
    ```python
    import <scripts_root>.nuoyanlib.server as nyl
    ```
    > **[警告]**  
    为确保环境安全，请勿将客户端和服务端代码写在同一个py文件内，且禁止导入对立端库（如在客户端导入服务端库，在服务端导入客户端库），否则可能导致「nuoyanlib」功能异常甚至游戏闪退。
4. 更多信息请参见[入门指南](/doc/入门指南.md)。

<br></br>

## 🎉 更新信息

---

作者正在熬夜编写中......

<br></br>

## 🔍 参考文档

---

作者正在熬夜编写中......

<br></br>

## 🌞 未来计划TODO

---

1. 重新整理函数文档注释，完成参考文档的编写；
2. 增加更多实用功能；
3. 编写demo；
4. 优化代码；
5. 完善Apollo版本；
6. ...

<br></br>

## 👑 贡献

---

本项目欢迎各位开发者共同参与开发，如果您有更好的算法或修改建议，可通过Issue或Pull Request的方式提交，成为本项目的贡献者。

[什么是Issue？](https://help.gitee.com/base/issue/intro)
[什么是Pull Request？](https://help.gitee.com/base/pullrequest/intro)

<br></br>

## 👴 联系作者

---

如果在使用过程中遇到问题，可通过以下方式联系作者：

- QQ：1279735247
- 邮箱：1279735247@qq.com

<br></br>