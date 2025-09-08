=======
API文档
=======

「nuoyanlib」包含以下公开的模块：

- ``nuoyanlib.client``：客户端工具包
    提供了NyUI框架、容器UI框架、特效管理、渲染、运镜工具等实用工具。
- ``nuoyanlib.server``：服务端工具包
    提供了实体工具、伤害工具等实用工具。
- ``nuoyanlib.utils``：通用工具包
    提供了事件监听框架、多种与MC密切相关的数学计算函数、向量工具、双端通信工具、随机性工具等实用工具。
- ``nuoyanlib.extensions``：「nuoyanlib」扩展包
    供开发者按需选择，可自行删除不需要的模块。
- ``nuoyanlib.enum``：枚举值模块
    包含「nuoyanlib」提供的枚举类。
- ``nuoyanlib.errors``：异常处理模块
    包含由「nuoyanlib」抛出的自定义异常类。

其他以下划线开头的模块/函数/变量/类是 **私有** 的，用于内部实现，不保证其功能的稳定性。其中， ``nuoyanlib._core`` 模块为「nuoyanlib」正常运行的最小依赖，请勿删除其中的任何 ``.py`` 文件。

.. warning::

    再次提醒，你只能在客户端/服务端环境导入 ``nuoyanlib.client`` / ``nuoyanlib.server`` 。否则，「nuoyanlib」将抛出 ``AcrossImportError`` 。

为简化表达，文档中的示例代码将省略 ``import`` 语句，并以 ``nyl`` 指代 ``nuoyanlib.<client/server>`` 。


.. toctree::
    :maxdepth: 2

    api/client
    api/server
    api/utils
