# GameTick说明文档 [已废弃]

当我们实现某些需要帧执行的功能时，常常会用到ModAPI提供的`OnScriptTickClient`或`OnScriptTickServer`事件，这两个事件每秒30次的触发频率能满足我们绝大部分的需求。  

但面对某些特殊的需求时，如实现丝滑的自定义UI动画、精确判断高速飞行的箭的位置等，30的频率就显得有些吃力了，这时GameTick就派上了用场。  

GameTick可以提供与游戏实时帧率一致的触发频率，对GameTick的监听可以让我们的tick事件实现与游戏帧率的同步。比如当前游戏实时帧率为60，那么监听了GameTick的事件就会每秒触发60次。

## 原理

---

监听GameTick的原理很简单，因为UI的渲染是与游戏实时帧率息息相关的，所以我们可以通过UI来监听GameTick。  

新建一个空白UI，然后在main画布中绑定一个变量`#main.gametick`（该变量名可自定义），并在Python代码中绑定对应的回调函数，即完成了对GameTick的监听。 随后在`UiInitFinished`事件中注册并创建该UI，我们就能观察到刚刚绑定的回调函数开始运行了。  

> 详见：https://pd.qq.com/s/dnm1v9ax8?shareSource=5 （复制到QQ打开）

## 使用方法

---

「nuoyanlib」已对GameTick进行了封装，按照以下步骤即可轻松使用GameTick。

1. 确保您已正确安装「nuoyanlib」。
2. 将`NuoyanGameTick.json`复制到您的`RP/ui`目录下。
3. 如果您的`RP/ui`目录下没有`_ui_defs.json`文件，将`_ui_defs.json`一并复制过去即可；如果您的`RP/ui`目录下已存在`_ui_defs.json`文件，将其打开并添加一行`ui/NuoyanGameTick.json`即可。
4. 将您的客户端继承`NuoyanClientSystem`，并重写OnGameTick方法即可。例如：

```python
from modScripts.nuoyanlib.client import NuoyanClientSystem

class MyClientSystem(NuoyanClientSystem):
    def __init__(self, namespace, system_name):
        super(MyClientSystem, self).__init__(namespace, system_name)

    def OnGameTick(self):
        # 在此编写需要每帧执行的代码
        pass
```
