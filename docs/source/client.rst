.. _client:
.. currentmodule:: nuoyanlib.client


============
客户端工具包
============


原版接口
~~~~~~~~

.. autosummary::
    :toctree: api/

    ENGINE_NAMESPACE
    ENGINE_SYSTEM_NAME
    ClientSystem
    CompFactory


事件监听
~~~~~~~~

.. autosummary::
    :toctree: api/

    ClientEventProxy
    Events
    ALL_CLIENT_ENGINE_EVENTS
    ALL_CLIENT_LIB_EVENTS


UI
~~

**UI工具**

.. autosummary::
    :toctree: api/

    ScreenNodeExtension
    create_ui
    to_path
    to_control
    iter_children_path_by_level
    iter_children_by_level
    get_parent_path
    get_parent
    notify_server

**Ny控件**

.. autosummary::
    :toctree: api/

    NyControl
    NyButton
    NyLabel
    NyImage
    NyProgressBar
    NyToggle
    NyItemRenderer
    NyEditBox
    NyStackPanel
    NyInputPanel
    NyGrid
    ElemGroup
    GridData
    NyScrollView
    NyPaperDoll
    NyMiniMap
    NyComboBox
    NySelectionWheel
    NySlider


摄像机
~~~~~~

.. autosummary::
    :toctree: api/

    get_entities_within_view


特效
~~~~

.. autosummary::
    :toctree: api/

    NeteaseParticle
    NeteaseFrameAnim


本地玩家
~~~~~~~~

.. autosummary::
    :toctree: api/

    player_plunge


渲染
~~~~

.. autosummary::
    :toctree: api/

    set_query_mod_var
    add_player_render_resources
    add_entity_render_resources


设置
~~~~

.. autosummary::
    :toctree: api/

    save_setting
    read_setting
    check_setting


音效
~~~~

.. autosummary::
    :toctree: api/

    play_custom_sound
    stop_custom_sound
