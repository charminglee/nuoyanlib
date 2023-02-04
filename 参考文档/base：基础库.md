###  clientcomp 

<br/>

-  **概述** 

该模块使用本地玩家实体ID和LevelId预创建了所有可能用到客户端组件，还包括ScreenNode、ViewBinder、ViewRequest等，省去了每次都要编写一长串代码的麻烦。 

-  **示例** 

```python
from myscripts.nuoyanLib.base.clientcomp import *
LevelGameComp.AddTimer(1.0, myfunc)
```

<br/>

###  servercomp

<br/>

-  **概述**

该模块使用LevelId预创建了所有服务端组件，省去了每次都要编写一长串代码的麻烦。

-  **示例** 

```python
from myscripts.nuoyanLib.base.servercomp import *
LevelGameComp.AddTimer(1.0, myfunc)
```

<br/>

###  nuoyanClientSystem

<br/>

-  **概述**

该模块包含NuoyanClientSystem，为ClientSystem扩展类，将自定义ClientSystem继承本类即可使用本类的全部功能。

-  **基础功能** 

1.  所有官方文档中收录的客户端引擎事件以及新增事件均无需手动监听，只需重写对应事件的回调函数即可（支持热更）；回调函数的命名规则为：On+去掉“Client”、“Event”、“On”字眼的事件名；如：OnScriptTickClient -> OnScriptTick、UiInitFinished -> OnUiInitFinished、AddEntityClientEvent -> OnAddEntity等；
2.  支持对在__init__方法中新增的事件监听或客户端属性（变量）执行热更；
3.  支持一键调用服务端属性（变量）、方法（函数）；
4.  无需重写Destroy方法进行事件的反监听。

-  **示例**

```python
from myscripts.nuoyanLib.base.nuoyanClientSystem import NuoyanClientSystem

class MyClientSystem(NuoyanClientSystem):
    def __init__(self, namespace, systemName):
        super(MyClientSystem, self).__init__(namespace, systemName)

    def OnScriptTick(self):
        """
        监听OnScriptTickClient事件。
        """

    def OnUiInitFinished(self, args):
        """
        监听UiInitFinished事件。
        """

    def OnGameTick(self):
        """
        监听GameTick事件。
        """
```

-  **新增方法** 

1.  **BroadcastToAllClient(eventName, eventData)**  
广播事件到所有客户端。

| 参数       | 数据类型 | 默认值  | 说明     |
|-----------|----------|--------|----------|
| eventName | str      | 无     | 事件名称  |
| eventData | Any      | 无     | 数据     |
|   **返回值**   | None | - | 无 |

```python
self.BroadcastToAllClient("MyCustomEvent", data)
``` 
 
2.  **ListenForEventV2(eventName, callback, t=0, namespace="", systemName="", priority=0)**  
监听事件（简化版）。

| 参数       | 数据类型       | 默认值  | 说明     |
|------------|---------------|--------|----------|
| eventName  | str           | 无     | 事件名称 |
| callback   | (Any) -> None | 无     | 回调函数 |
| t          | int           | 0      | 0表示监听当前Mod服务端传来的自定义事件，1表示监听当前Mod客户端引擎事件，2表示监听其他Mod的事件 |
| namespace  | str           | ""     | 其他Mod的命名空间 |
| systemName | str           | ""     | 其他Mod的系统名称 |
| priority   | int           | 0      | 优先级 |
|   **返回值**   | None | - | 无 |

```python
self.ListenForEventV2("MyCustomEvent", self.myfunc)
```

-  **新增事件**

1.   **GameTick**  
\*tick\*  
频率与游戏实时帧率同步的Tick事件。比如房主的游戏帧率为60帧，则该事件每秒触发60次。  
需要注意的是，因为受游戏帧率影响，该事件的触发帧率并不稳定。  
如果没有特殊需求，建议使用OnScriptTick。  

-  **注意事项**

1.  带有\*tick\*标签的事件为帧事件，需要注意编写相关逻辑；
2.  事件回调参数中，参数名前面的美元符号$表示该参数可进行修改。

<br/>

### nuoyanServerSystem

<br/>

-  **概述**

该模块包含NuoyanServerSystem，为ServerSystem扩展类，将自定义ServerSystem继承本类即可使用本类的全部功能。

-  **基础功能** 

1. 所有官方文档中收录的服务端引擎事件以及新增事件均无需手动监听，只需重写对应事件的回调函数即可（支持热更）；回调函数的命名规则为：On+去掉“Server”、“Event”、“On”字眼的事件名；如：OnScriptTickServer -> OnScriptTick、OnCarriedNewItemChangedServerEvent -> OnCarriedNewItemChanged、EntityRemoveEvent -> OnEntityRemove等；
2. 支持对在__init__方法中新增的事件监听或服务端属性（变量）执行热更；
3. 支持一键调用客户端属性（变量）、方法（函数）；
4. 无需重写Destroy方法进行事件的反监听。

-  **示例**

```python
from myscripts.nuoyanLib.base.nuoyanServerSystem import NuoyanServerSystem

class MyServerSystem(NuoyanServerSystem):
    def __init__(self, namespace, systemName):
        super(MyServerSystem, self).__init__(namespace, systemName)

    def OnScriptTick(self):
        """
        监听OnScriptTickServer事件。
        """

    def OnUiInitFinished(self, args):
        """
        监听UiInitFinished事件。
        """

    def OnGameTick(self):
        """
        监听GameTick事件。
        """
```

-  **新增方法** 
 
1. **ListenForEventV2(eventName, callback, t=0, namespace="", systemName="", priority=0)**  
监听事件（简化版）。

| 参数       | 数据类型       | 默认值  | 说明     |
|------------|---------------|--------|----------|
| eventName  | str           | 无     | 事件名称 |
| callback   | (Any) -> None | 无     | 回调函数 |
| t          | int           | 0      | 0表示监听当前Mod客户端传来的自定义事件，1表示监听当前Mod服务端引擎事件，2表示监听其他Mod的事件 |
| namespace  | str           | ""     | 其他Mod的命名空间 |
| systemName | str           | ""     | 其他Mod的系统名称 |
| priority   | int           | 0      | 优先级 |
|   **返回值**   | None | - | 无 |

```python
self.ListenForEventV2("MyCustomEvent", self.myfunc)
```

-  **新增事件**

1.   **UiInitFinished**  
客户端玩家UI框架初始化完成时，服务端触发。

| 参数         | 数据类型      | 说明    |
|-------------|---------------|---------|
| \_\_id\_\_  | str           | 玩家实体ID |

2.   **GameTick**  
\*tick\*  
触发帧率与房主玩家的游戏实时帧率同步的Tick事件。比如房主的游戏帧率为60帧，则该事件每秒触发60次。  
需要注意的是，因为受游戏帧率影响，该事件的触发帧率并不稳定。  
如果没有特殊需求，建议使用OnScriptTick。 

-  **新增属性**

1.   **allPlayerData**  
用于保存所有玩家数据的字典，key为玩家实体ID，value为玩家数据字典，可自行添加数据。  
玩家加入游戏时（客户端抛出UiInitFinished后，可在服务端的OnUiInitFinished中对数据进行初始化）会自动把玩家加入字典，玩家退出游戏时则会自动从字典中删除玩家及其数据。  
初始值为空字典。

```python
def OnUiInitFinished(self, args):
    self.allPlayerData[playerId]['data1'] = 0
    self.allPlayerData[playerId]['data2'] = []
```

2.   **homeownerPlayerId**  
房主玩家的实体ID；初始值为None。

```python
if self.homeownerPlayerId:
    LevelItemComp.SpawnItemToPlayerInv(
        {'newItemName': "minecraft:apple", 'count': 1}, self.homeownerPlayerId
    )
```

-  **注意事项**

1.  带有\*tick\*标签的事件为帧事件，需要注意编写相关逻辑；
2.  事件回调参数中，参数名前面的美元符号$表示该参数可进行修改。

<br/>

### nuoyanScreenNode

<br/>

-  **概述**

该模块包含NuoyanScreenNode，为ScreenNode扩展类。将自定义UI类继承本类即可使用本类的全部功能。

-  **示例**

```python
from myscripts.nuoyanLib.base.nuoyanScreenNode import NuoyanScreenNode

class MyUI(NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(MyUI, self).__init__(namespace, name, param)
```

-  **新增方法** 

1.   **SetButtonDoubleClickCallback(buttonPath, doubleClickCallback, touchUpCallback=None)**  
设置按钮双击监听。  
因为设置双击监听需要覆盖按钮的TouchUpCallback，如需单独设置TouchUpCallback请使用该方法的touchUpCallback参数。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| buttonPath  | str | 无 | 按钮路径 |
| doubleClickCallback | (dict) -> None | 无 | DoubleClick回调函数 |
| touchUpCallback | Optional[(dict) -> None] | None | TouchUp回调函数 |
|   **返回值**   | None | - | 无 |

```python
def OnDoubleClick(self, args):
    pass
self.SetButtonDoubleClickCallback(buttonPath, self.OnDoubleClick)
```

2.   **SetButtonMovable(btnPath, moveParent=False, associatedWidgetPath=(), touchMoveCallback=None)**  
设置按钮可拖动。  
因为设置按钮可拖动需要覆盖按钮的TouchMoveCallback，如需单独设置TouchMoveCallback请使用该方法的touchMoveCallback参数。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| btnPath | str | 无 | 按钮路径 |
| moveParent | bool | False | 是否同时拖动父控件 |
| associatedWidgetPath | Union[str, Tuple[str, ...]] | () | 关联拖动的其他控件的路径，多个控件请使用元组 |
| touchMoveCallback | Optional[(dict) -> None] | None | TouchMove回调函数 |
|   **返回值**   | None | - | 无 |

```python
def OnTouchMove(self, args):
    pass
self.SetButtonMovable(buttonPath, touchMoveCallback=self.OnTouchMove)
```

3.   **CancelButtonMovable(btnPath)**  
取消按钮可拖动。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| btnPath | str | 无 | 按钮路径 |
|   **返回值**   | None | - | 无 |

```python
self.CancelButtonMovable(buttonPath)
```

4.   **SetButtonLongClickCallback(btnPath, longClickFunc, touchUpFunc=None, touchMoveOutFunc=None, touchDownFunc=None, touchCancelFunc=None)**  
设置按钮长按监听。  
因为设置按钮可拖动需要覆盖按钮的TouchUpCallback、TouchMoveOutCallback、TouchDownCallback和TouchCancelCallback，如需单独设置这些Callback请使用该方法对应的参数。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| btnPath | str | 无 | 按钮路径 |
| longClickFunc | (dict) -> None | 无 | LongClick回调函数 |
| touchUpFunc | Optional[(dict) -> None] | None | TouchUp回调函数 |
| touchMoveOutFunc | Optional[(dict) -> None] | None | TouchMoveOut回调函数 |
| touchDownFunc | Optional[(dict) -> None] | None | TouchDown回调函数 |
| touchCancelFunc | Optional[(dict) -> None] | None | TouchCancel回调函数 |
|   **返回值**   | None | - | 无 |

```python
def OnLongClick(self, args):
    pass
def OnTouchUp(self, args):
    pass
self.SetButtonLongClickCallback(buttonPath, self.OnLongClick, touchUpFunc=self.OnTouchUp)
```

5.   **RemoveButtonLongClickCallback(btnPath)**  
移除按钮长按监听。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| btnPath | str | 无 | 按钮路径 |
|   **返回值**   | None | - | 无 |

```python
self.RemoveButtonLongClickCallback(buttonPath)
```

6.   **SetLongClickVibrateTime(time)**  
设置长按后震动反馈的时长。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| time | int | 无 | 毫秒 |
|   **返回值**   | None | - | 无 |

```python
self.SetLongClickVibrateTime(1000)
```

7.   **HasLongClicked(bp)**  
用于判断按钮在当次按下中是否已经触发了长按。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| bp | str | 无 | 按钮路径 |
|   **返回值**   | bool | - | 从按钮按下到触发长按前，该方法返回False；从触发长按到下次按钮按下前，该方法返回True |

```python
if self.HasLongClicked(buttonPath):
    pass
```

8.   **SetButtonMovableAfterLongClick(btnPath, moveParent=False, associatedWidgetPath=(), touchUpFunc=None, longClickFunc=None, touchMoveCallback=None, touchMoveOutFunc=None, touchDownFunc=None, touchCancelFunc=None)**  
设置按钮长按拖动。  
该方法设置的按钮拖动会自动保存位置，下次启动游戏时按钮会恢复到上次游戏时的位置。  
因为设置按钮可拖动需要覆盖按钮的TouchUpCallback、LongClickCallback、TouchMoveCallback、TouchMoveOutCallback、TouchDownCallback和TouchCancelCallback，如需单独设置这些Callback请使用该方法对应的参数。

| 参数         | 数据类型      | 默认值   | 说明    |
|-------------|---------------|---------|---------|
| btnPath | str | 无 | 按钮路径 |
| moveParent | bool | False | 是否同时拖动父控件 |
| associatedWidgetPath | Union[str, Tuple[str, ...]] | () | 关联拖动的其他控件的路径，多个控件请使用元组 |
| touchUpFunc | Optional[(dict) -> None] | None | TouchUp回调函数 |
| longClickFunc | Optional[(dict) -> None] | None | LongClick回调函数 |
| touchMoveCallback | Optional[(dict) -> None] | None | TouchMove回调函数 |
| touchMoveOutFunc | Optional[(dict) -> None] | None | TouchMoveOut回调函数 |
| touchDownFunc | Optional[(dict) -> None] | None | TouchDown回调函数 |
| touchCancelFunc | Optional[(dict) -> None] | None | TouchCancel回调函数 |
|   **返回值**   | None | - | 无 |

```python
def OnLongClick(self, args):
    pass
def OnTouchUp(self, args):
    pass
self.SetButtonMovableAfterLongClick(buttonPath, touchUpFunc=self.OnTouchUp, longClickFunc=self.OnLongClick)
```

-  **新增属性** 

1.  **cs**  
注册该UI的ClientSystem实例，可直接使用该属性在UI类中调用客户端的接口、方法、属性等。

```python
# 调用客户端接口
self.cs.NotifyToServer("MyCustomEvent", {})
# 调用客户端方法
self.cs.myfunc(args)
# 给客户端属性赋值
self.cs.variable = 1
```

2.   **screenSize**  
屏幕尺寸元组：(宽度, 高度)；屏幕尺寸改变时，该属性也会跟着改变。

```python
self.GetBaseUIControl(uiPath).SetSize(self.screenSize)
```

-  **注意事项** 
 
1.  重写Create和Update方法时请调用一次父类的同名方法，如：`super(MyUI, self).Create()` 或 `NuoyanScreenNode.Create(self)`；
2.  带有\*tick\*标签的事件为帧事件，需要注意编写相关逻辑；
