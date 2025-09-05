.. _server:
.. currentmodule:: nuoyanlib.server


============
服务端工具包
============


事件监听
~~~~~~~~

.. autosummary::
    :toctree: api/

    ServerEventProxy
    Events
    ALL_SERVER_ENGINE_EVENTS
    ALL_SERVER_LIB_EVENTS


方块
~~~~

.. autosummary::
    :toctree: api/

    spawn_ground_shatter_effect


实体
~~~~

.. autosummary::
    :toctree: api/

    set_query_mod_var
    clear_effects
    bounce_entities
    attract_entities
    is_mob
    all_mob
    any_mob
    entity_filter
    is_entity_type
    sort_entity_list_by_dist
    launch_projectile
    entity_plunge
    entity_plunge_by_dir
    entity_plunge_by_rot
    get_all_entities
    get_entities_by_name
    get_entities_by_type
    get_entities_in_area
    get_entities_by_locking
    get_nearest_entity
    attack_nearest_mob
    has_effect
    get_entities_by_ray
    entity_distance


伤害
~~~~

.. autosummary::
    :toctree: api/

    ignore_dmg_cd
    EntityFilter
    hurt
    hurt_mobs
    explode_damage
    cylinder_damage
    ball_damage
    sector_damage
    rectangle_damage
    percent_damage


背包
~~~~

.. autosummary::
    :toctree: api/

    set_items_to_item_grid
    get_items_from_item_grid
    update_item_grids
    deduct_inv_item
    clear_items
    get_item_pos
    change_item_count


结构
~~~~

.. autosummary::
    :toctree: api/

    place_large_structure
