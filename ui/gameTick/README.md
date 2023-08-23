# GameTick

## 简介

当我们实现某些需要帧执行的功能时，常常会用到ModApi提供的OnScriptTickClient/OnScriptTickServer事件，这两个事件提供的每秒30次的触发帧率能满足我们大部分的需求。  

但面对某些特殊的需求时，如丝滑的自定义UI动画、精确判断高速飞行的箭的位置等，30帧就显得有些吃力了，于是GameTick就派上了用场。  

顾名思义，GameTick即游戏刻/游戏帧，对GameTick的监听可以让我们的tick事件实现与游戏帧率的同步。  

> 比如当前游戏实时帧率为60，那么监听了GameTick的事件就会每秒触发60次。

## 原理

监听GameTick的原理很简单，UI可以获取到一些引擎的相关信息，因此我们可以通过UI来监听GameTick。  

新建一个空白UI，然后在main画布中绑定引擎变量#main.gametick，并在Python代码中绑定对应的回调函数，即完成了对GameTick的监听。 随后在UiInitFinished事件中注册并创建该UI，我们就能观察到刚刚绑定的回调函数开始运行了。  

> 详见：https://pd.qq.com/s/dnm1v9ax8?shareSource=5

## 安装方法

- 将`_GameTick.json`复制到您的`RP/ui`目录下；  
- 如果您的`RP/ui`目录下没有`_ui_defs.json`文件，将`_ui_defs.json`一并复制过去即可；  
- 如果您的`RP/ui`目录下已存在`_ui_defs.json`文件，将其打开并添加一行`ui/_GameTick.json`即可。

## 使用方法

- 客户端：将您的客户端继承NuoyanClientSystem，重写OnGameTick方法。

```python
class MyClientSystem(NuoyanClientSystem):
    def __init__(self, namespace, systemName):
      super(MyClientSystem, self).__init__(namespace, systemName)
        
    def OnGameTick(self):
        pass
```

- 服务端：将您的服务端继承NuoyanServerSystem，重写OnGameTick方法。

```python
class MyServerSystem(NuoyanServerSystem):
    def __init__(self, namespace, systemName):
      super(MyServerSystem, self).__init__(namespace, systemName)
        
    def OnGameTick(self):
        pass
```