# GameTick

## 简介

当我们实现某些需要帧执行的功能时，常常会用到ModApi提供的OnScriptTickClient/OnScriptTickServer事件，这两个事件提供的每秒30次的触发帧率能满足我们大部分的需求。  

但面对某些特殊的需求时，如丝滑的自定义UI动画、精确判断高速飞行的箭的位置等，30帧就显得有些吃力了，于是GameTick就派上了用场。  

顾名思义，GameTick即游戏刻/游戏帧，对GameTick的监听可以让我们的tick事件实现与游戏帧率的同步。  

> 比如当前游戏实时帧率为60，那么监听了GameTick的事件就会每秒触发60次。

## 原理

监听GameTick的原理很简单。既然是游戏帧率，那当然也包括了UI的帧率，因此我们可以通过UI来监听GameTick。  

通过在UI的main画布中绑定变量#main.gametick，并在py中绑定对应的回调函数，即完成了对GameTick的监听。 

随后在UiInitFinished事件中注册并创建UI，我们就能观察到刚刚绑定的回调函数开始运行了。  
> 详见：https://pd.qq.com/s/dnm1v9ax8?shareSource=5

## 安装方法

为了方便大家使用GameTick，作者已经帮大家写好了相关的json和py代码逻辑，您可以选择使用本函数库附带的GameTickInstaller一键安装，也可以选择手动安装。
- 使用GameTickInstaller安装步骤：  
  - 将GameTickInstaller.py用Pycharm或VS Code等软件打开并运行，或直接使用Python解释器运行（请使用Python2运行）；  
  - 在弹出的窗口中找到您的资源包（resource_pack）根目录，将其选中并点击确认即可。


- 手动安装步骤：  
  - 将_GameTick.json复制到您的resource_pack/ui目录下；  
  - 如果您的resource_pack/ui目录下没有_ui_defs.json文件，将_ui_defs.json一并复制过去即可；  
  - 如果您的resource_pack/ui目录下已存在_ui_defs.json文件，将其打开并添加一行 `ui/_GameTick.json` 即可。

## 使用方法

- 客户端：将您的客户端继承NuoyanClientSystem，并重写OnGameTick方法。
```python
class MyClientSystem(NuoyanClientSystem):
    def __init__(self, namespace, systemName):
      super(MyClientSystem, self).__init__(namespace, systemName)
        
    def OnGameTick(self):
        pass
```
- 服务端：将您的服务端继承NuoyanServerSystem，并重写OnGameTick方法。
```python
class MyServerSystem(NuoyanServerSystem):
    def __init__(self, namespace, systemName):
      super(MyServerSystem, self).__init__(namespace, systemName)
        
    def OnGameTick(self):
        pass
```