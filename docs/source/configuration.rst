.. _config:

========
全局配置
========

全局配置是位于 `nuoyanlib/config.py <https://github.com/charminglee/nuoyanlib/blob/master/src/nuoyanlib/config.py>`_ 中的常量，用于配置「nuoyanlib」的某些功能的行为。你可以直接在 ``config.py`` 修改配置项，也可以通过以下方式动态修改：

.. code-block:: python

    import <scripts_root>.nuoyanlib.<client/server> as nyl
    nyl.config.ENABLED_LOG = False # 禁用「nuoyanlib」日志输出

.. important::

    对配置项的修改仅限于其所在环境，即在客户端作的修改仅影响客户端，在服务端作的修改仅影响服务端。

以下列出「nuoyanlib」中所有全局配置项。

.. note::

    标注 [需要重载] 的配置项，修改后需重载存档方可生效。

**一般配置**

===========================  ========  ==========  ===========
          名称                  类型      初始值         解释
===========================  ========  ==========  ===========
ENABLED_LOG                  bool      True        [需要重载] 是否输出「nuoyanlib」日志信息。
DISABLED_MODSDK_LOG          bool      False       [需要重载] 是否关闭ModSDK日志输出。
ENABLED_TYPE_CHECKING        bool      True        [需要重载] 是否启用「nuoyanlib」对某些函数的参数类型的运行时检查（关闭可获得少许性能提升）。
ENABLED_MCP_MOD_LOG_DUMPING  bool      False       [需要重载] 是否将当前Mod的错误信息输出到McpModLog日志（目前正式服已阉割该功能）。
===========================  ========  ==========  ===========

:func:`spawn_ground_shatter_effect() <nuoyanlib.server.spawn_ground_shatter_effect>` **函数配置**

===========================  ========================  =======================================================================  ===========
          名称                         类型                                              初始值                                       解释
===========================  ========================  =======================================================================  ===========
GSE_IN_FUNC                  Callable[[float], float]  :any:`TimeEaseFunc.out_expo <nuoyanlib.utils.TimeEaseFunc.out_expo>`     裂地效果上浮阶段使用的缓动函数，如线性函数 ``lambda x: x`` ，参数 ``x`` 表示经过的时间比例，取值范围为 ``[0,⠀1]`` ，即只取缓动函数定义域中 ``[0,⠀1]`` 部分的值。
GSE_OUT_FUNC                 Callable[[float], float]  :any:`TimeEaseFunc.in_sine <nuoyanlib.utils.TimeEaseFunc.in_sine>`       裂地效果下沉阶段使用的缓动函数，含义同上。
GSE_USE_RENDER_TICK          bool                      False                                                                    [需要重载] 裂地效果是否使用渲染帧进行刷新。
===========================  ========================  =======================================================================  ===========


