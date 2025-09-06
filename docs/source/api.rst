=======
API文档
=======

「nuoyanlib」包含以下公开的工具包：

- ``nuoyanlib.client``：客户端工具包，提供了NyUI框架、容器UI框架、特效管理、渲染、运镜工具等实用工具。
- ``nuoyanlib.server``：服务端工具包，提供了实体工具、伤害工具等实用工具。
- ``nuoyanlib.utils``：通用工具包，提供了事件监听框架、多种与MC密切相关的数学计算函数、向量工具、双端通信工具、随机数工具等实用工具。
- ``nuoyanlib.extensions``：「nuoyanlib」扩展功能，供开发者按需选择。

其他以下划线开头的模块/函数/变量/类是私有的，用于内部实现，不保证功能稳定性。其中， ``nuoyanlib._core`` 模块为「nuoyanlib」运行的最小依赖，请勿删除其中的任何 ``.py`` 文件，以保证「nuoyanlib」的正常运行。

.. warning::

    再次提醒，你只能在客户端/服务端环境导入 ``nuoyanlib.client`` / ``nuoyanlib.server`` 。否则，「nuoyanlib」将抛出 ``AcrossImportError`` 。


.. toctree::
    :maxdepth: 2

    api/client
    api/server
    api/utils
