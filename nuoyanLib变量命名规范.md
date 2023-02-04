## nuoyanLib变量命名规范

在nuoyanLib的开发过程中，应当遵循以下命名规范：

### **一般变量名（包括函数名、函数参数等）：小驼峰**

```python
variableName = ...

def funcName(paramName): 
    ...
```

### **常量：全大写，单词间下划线隔开**

```python
CONSTANT_NAME = ...
```

### **库函数名：全小写，单词间下划线隔开**

```python
def pos_distance(...): 
    ...
```

### **类名：大驼峰**

```python
class ClassName(...): 
    ...
```

### **属性名、方法名：小驼峰**

```python
class ...(...):
    classAttr = ...
    
    def __init__(...):
        self.classAttr = ...

    def classMethod(...):
        ...
```

### **接口名：大驼峰**

```python
class ...(...):
    def InterfaceName(...):
```

### **回调函数名：On+大驼峰**

```python
def OnEntityRemove(...):
    ...

def OnButtonTouchUp(...):
    ...
```

### **事件名：大驼峰**

```python
self.ListenForEvent(..., "EventName", ...)
```

### **包名、模块名：小驼峰**

### **系统命名空间、系统名：大驼峰**

```python
clientApi.RegisterSystem("ModName", "SystemName", ...)
```

### **字典键名：小驼峰**

```python
{'keyName': ...}
```