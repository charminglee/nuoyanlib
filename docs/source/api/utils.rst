.. _utils:
.. currentmodule:: nuoyanlib.utils


==========
通用工具包
==========


所有在 ``nuoyanlib.utils`` 中公开的接口都可以在 ``nuoyanlib.<client/server>`` 中获得，因此你不必单独 ``import nuoyanlib.utils`` 。


事件监听
~~~~~~~~

.. autosummary::
    :toctree: apis/

    EventArgsProxy
    event
    listen_event
    unlisten_event
    listen_all_events
    unlisten_all_events


通信
~~~~

.. autosummary::
    :toctree: apis/

    Caller
    call
    broadcast_to_all_systems


物品
~~~~

.. autosummary::
    :toctree: apis/

    deepcopy_item_dict
    gen_item_dict
    get_item_count
    set_namespace
    is_same_item
    is_empty_item
    are_same_item
    get_max_stack


数学
~~~~

.. autosummary::
    :toctree: apis/

    pos_distance_square
    clamp
    pos_block_facing
    to_polar_coordinate
    to_cartesian_coordinate
    probability_true_i
    probability_true_f
    pos_distance_to_line
    pos_floor
    pos_distance
    to_relative_pos
    to_screen_pos
    pos_rotate
    midpoint
    camera_rot_p2p
    pos_entity_facing
    pos_forward_rot
    n_quantiles_index_list
    cube_center
    cube_longest_side_len
    is_in_sector
    is_in_cube
    rot_diff
    ray_aabb_intersection


随机
~~~~

.. autosummary::
    :toctree: apis/

    random_pos
    random_string
    random_even_poses


计时器
~~~~~~

.. autosummary::
    :toctree: apis/

    McTimer


坐标生成
~~~~~~~~

.. autosummary::
    :toctree: apis/

    gen_line_pos
    gen_circle_pos
    gen_sphere_pos
    gen_cube_pos
    gen_spiral_pos


时间缓动
~~~~~~~~

.. autosummary::
    :toctree: apis/

    TimeEaseFunc
    TimeEase


向量
~~~~

.. autosummary::
    :toctree: apis/

    is_zero_vec
    set_vec_length
    vec_orthogonal_decomposition
    vec_entity_left
    vec_entity_right
    vec_entity_front
    vec_entity_back
    vec_normalize
    vec_rot_p2p
    vec_p2p
    vec_length
    vec_angle
    vec_euler_rotate
    vec_rotate_around
    outgoing_vec
    vec_composite
    vec_scale


其他工具
~~~~~~~~

.. autosummary::
    :toctree: apis/

    notify_error
    call_interval
    add_condition_to_func
    rm_condition_to_func
    all_indexes
    check_string
    check_string2
    turn_dict_value_to_tuple
    turn_list_to_tuple
    is_method_overridden
    translate_time
    try_exec
    iter_obj_attrs
    cached_property
    CachedObject
    cached_method
    cached_func
    singleton


异常
~~~~

.. autosummary::
    :toctree: apis/

    NuoyanLibServerSystemRegisterError
    NuoyanLibClientSystemRegisterError
    PathMatchError
    AcrossImportError
    GetPropertyError
    ScreenNodeNotFoundError
    EventParameterError
    VectorError
    EventSourceError
    EventNotFoundError


枚举
~~~~

.. autosummary::
    :toctree: apis/

    Enum
    GridCallbackType
    ComboBoxCallbackType
    ButtonCallbackType
    ControlType
    FriendlyMob
    HostileMob
    Mob
    Feature
    UiContainer
    Container
    PositiveEffect
    NegativeEffect
    NeutralEffect
    ENTITY_NAME_MAP
    BIOME_NAME_MAP
    STRUCTURE_NAME_MAP
    EFFECT_NAME_MAP
    ENCHANT_NAME_MAP
