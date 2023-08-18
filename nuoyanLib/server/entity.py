# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-08-02
#
# ====================================================


from copy import copy as _copy
import mod.server.extraServerApi as _serverApi
from mod.common.minecraftEnum import EntityType as _EntityType
from ..mctypes.server.system.serverSystem import ServerSystem as _ServerSystem
from ..utils.calculator import pos_distance as _pos_distance, perlin_noise as _perlin_noise
from ..utils.vector import vector_p2p as _vector_p2p, composite_vector as _composite_vector


__all__ = [
    "clear_effects",
    "bounce_entities",
    "attract_entities",
    "is_mob",
    "all_mob",
    "has_mob",
    "entity_filter",
    "is_entity_type",
    "sort_entity_list_by_distance",
    "launch_projectile",
    "entity_plunge",
    "entity_plunge_by_dir",
    "entity_plunge_by_rot",
    "get_all_entities",
    "get_entities_by_name",
    "get_entities_by_type",
    "get_entities_in_area",
    "get_entities_by_locking",
    "get_nearest_entity",
    "attack_nearest_mob",
    "has_effect",
    "set_entity_motion",
]


_LEVEL_ID = _serverApi.GetLevelId()
_ServerCompFactory = _serverApi.GetEngineCompFactory()
_LevelProjectileComp = _ServerCompFactory.CreateProjectile(_LEVEL_ID)
_LevelGameComp = _ServerCompFactory.CreateGame(_LEVEL_ID)


def clear_effects(entityId):
    # type: (str) -> None
    """
    清除指定实体的全部药水效果。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    -----------------------------------------------------------
    NoReturn
    """
    comp = _ServerCompFactory.CreateEffect(entityId)
    effects = comp.GetAllEffects()
    if not effects:
        return
    for eff in effects:
        comp.RemoveEffectFromEntity(eff['effectName'])

def bounce_entities(pos, dim, radius, power, filterIdList=None, filterTypeIdList=None, filterTypeStrList=None,
                    filterAbiotic=False):
    # type: (tuple[float, float, float], int, float, float, list[str] | None, list[int] | None, list[str] | None, bool) -> list[str]
    """
    从中心弹开指定范围内的实体。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 弹开中心坐标
    【dim: int】 维度ID
    【radius: float】 弹开半径
    【power: float】 弹开强度
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【filterTypeStrList: Optional[List[str]] = None】 过滤的实体类型ID列表
    【filterAbiotic: bool = False】 是否过滤非生物实体
    -----------------------------------------------------------
    return: List[str] -> 被弹开的实体ID列表
    """
    return attract_entities(pos, dim, radius, -power, filterIdList, filterTypeIdList, filterTypeStrList, filterAbiotic)


def attract_entities(pos, dim, radius, power, filterIdList=None, filterTypeIdList=None, filterTypeStrList=None,
                     filterAbiotic=False):
    # type: (tuple[float, float, float], int, float, float, list[str] | None, list[int] | None, list[str] | None, bool) -> list[str]
    """
    吸引指定范围内的实体到中心。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 吸引中心坐标
    【dim: int】 维度ID
    【radius: float】 吸引半径
    【power: float】 吸引强度
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【filterTypeStrList: Optional[List[str]] = None】 过滤的实体类型ID列表
    【filterAbiotic: bool = False】 是否过滤非生物实体
    -----------------------------------------------------------
    return: List[str] -> 被吸引的实体ID列表
    """
    ents = get_entities_in_area(pos, radius, dim, filterIdList, filterTypeIdList, filterTypeStrList, filterAbiotic)
    res = []
    for eid in ents:
        epos = _ServerCompFactory.CreatePos(eid).GetFootPos()
        if not epos:
            continue
        comp = _ServerCompFactory.CreateActorMotion(eid)
        origMotion = comp.GetMotion()
        vec = _vector_p2p(epos, pos)
        vec = tuple(i * power for i in vec)
        resMotion = _composite_vector(origMotion, vec)
        etype = _ServerCompFactory.CreateEngineType(eid).GetEngineType()
        if etype == _EntityType.Player:
            if comp.SetPlayerMotion(resMotion):
                res.append(eid)
        else:
            if comp.SetMotion(resMotion):
                res.append(eid)
    return res


def is_mob(entityId):
    # type: (str) -> bool
    """
    判断实体是否为生物。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    -----------------------------------------------------------
    return: bool -> 是生物返回True，否则返回False
    """
    typeStr = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    return typeStr & _EntityType.Mob == _EntityType.Mob


def all_mob(entityIdList):
    # type: (list[str]) -> bool
    """
    判断一个实体ID列表内的实体是否均为生物。
    -----------------------------------------------------------
    【entityIdList: List[str]】 实体ID列表
    -----------------------------------------------------------
    return: bool -> 均为生物返回True，否则返回False
    """
    return all(is_mob(i) for i in entityIdList)


def has_mob(entityIdList):
    # type: (list[str]) -> bool
    """
    判断一个实体ID列表内的实体是否含有生物。
    -----------------------------------------------------------
    【entityIdList: List[str]】 实体ID列表
    -----------------------------------------------------------
    return: bool -> 含有生物返回True，否则返回False
    """
    return any(is_mob(i) for i in entityIdList)


def entity_filter(entityList, *args):
    # type: (list[str], tuple[tuple[float, float, float], float] | int | list[str] | list[int]) -> list[str]
    """
    实体ID过滤器。
    自动过滤无法获取坐标的实体。
    请自行检查传入的过滤参数是否存在冲突，若存在冲突，可能会返回错误的结果。
    过滤参数的优先级从左至右递减。
    过滤参数说明及示例：
    1. 传入一个tuple，tuple的第一个元素为坐标，第二个元素为半径，表示保留该坐标半径范围内的所有实体；
    entity_filter(entityList, (pos, 60))     # 保留以pos为中心60格半径内的实体
    2. 将EntityType枚举放入集合传入，表示保留这些类型的所有实体；
    entity_filter(entityList, {EntityType.Mob})     # 保留所有生物
    entity_filter(entityList, {EntityType.Pig, EntityType.Wolf})     # 保留所有猪和狼
    3. 将字符串形式的维度ID放入集合传入，表示保留这些维度的所有实体；
    entity_filter(entityList, {"0", "1"})     # 保留所有主世界和地狱的实体
    4. 将实体ID放入列表传入，表示抛弃这些实体ID；
    entityList = ["-123", "-456", "-789"]
    entity_filter(entityList, ["-123", "-456"])     # ["-789"]
    5. 将EntityType枚举放入列表传入，表示抛弃这些类型的所有实体；
    entity_filter(entityList, [EntityType.Mob])     # 抛弃所有生物
    entity_filter(entityList, [EntityType.Pig, EntityType.Wolf])     # 抛弃所有猪和狼
    6. 以上5种过滤参数均可混合使用；
    entity_filter(entityList, {"0"}, (pos, 60), {EntityType.Mob})     # 保留主世界中以pos为中心60格半径内的所有生物
    -----------------------------------------------------------
    【entityList: List[str]】 实体ID列表
    【args: Union[Tuple[tuple, float], int, List[str], List[int]]】 过滤参数
    -----------------------------------------------------------
    return: List[str] -> 过滤后的实体ID列表
    """
    def _filter(eid):
        entPos = _ServerCompFactory.CreatePos(eid).GetFootPos()
        entType = _ServerCompFactory.CreateEngineType(eid).GetEngineType()
        entTypeStr = _ServerCompFactory.CreateEngineType(eid).GetEngineTypeStr()
        entDim = str(_ServerCompFactory.CreateDimension(eid).GetEntityDimensionId())
        if not entPos:
            return False
        for arg in args:
            if not arg:
                continue
            if isinstance(arg, tuple) and _pos_distance(arg[0], entPos) > arg[1]:
                return False
            if isinstance(arg, set):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == entTypeStr:
                            break
                        if ":" not in i and i == entDim:
                            break
                    if isinstance(i, int) and entType & i == i:
                        break
                else:
                    return False
            if isinstance(arg, list):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == entTypeStr:
                            return False
                        if ":" not in i and i == eid:
                            return False
                    if isinstance(i, int) and entType & i == i:
                        return False
        return True
    return filter(_filter, entityList)


def is_entity_type(entityId, typeId):
    # type: (str, int) -> bool
    """
    判断实体是否是某一类型。
    示例：
    pigEntityId = ...
    is_entity_type(pigEntityId, EntityType.Pig)     # True
    is_entity_type(pigEntityId, EntityType.Mob)     # True
    is_entity_type(pigEntityId, EntityType.Wolf)     # False
    is_entity_type(pigEntityId, EntityType.Monster)     # False
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【typeId: int】 实体类型ID（网易版）
    -----------------------------------------------------------
    return: bool -> 是则返回True，否则返回False
    """
    et = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    return et & typeId == typeId


def sort_entity_list_by_distance(pos, entityList):
    # type: (tuple[float, float, float], list[str]) -> None
    """
    根据距离从小到大对实体列表进行排序。该函数直接修改原列表，无法获取坐标的实体将会从列表中删除。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 参照坐标
    【entityList: List[str]】 实体ID列表
    -----------------------------------------------------------
    NoReturn
    """
    if not entityList or not pos:
        return []
    notExist = []
    def func(eid):
        ep = _ServerCompFactory.CreatePos(eid).GetFootPos()
        if not ep:
            notExist.append(eid)
        return _pos_distance(ep, pos)
    entityList.sort(key=func)
    for i in notExist:
        entityList.remove(i)


def launch_projectile(projectileName, spawnerId, power=None, damage=None, position=None, direction=None, gravity=None,
                      targetId="",  isDamageOwner=False, error=0.0):
    # type: (str, str, float | None, int | None, tuple[float, float, float] | None, tuple[float, float, float] | None, float | None, str, bool, float) -> str
    """
    发射抛射物。
    -----------------------------------------------------------
    【projectileName: str】 抛射物名字
    【spawnerId: str】 发射者的实体ID
    【power: Optional[float]】 抛射物威力（速度），默认为json配置中的值
    【damage: Optional[int]】 抛射物伤害，默认为json配置中的值
    【position: Optional[Tuple[float, float, float]] = None】 初始位置，默认为比发射者脚底高1.6格的位置
    【direction: Optional[Tuple[float, float, float]] = None】 初始朝向，默认为发射者准星方向
    【gravity: Optional[float] = None】 抛射物重力，默认为json配置中的值
    【targetId: str = ""】 抛射物目标（指定了targetId之后，会和潜影贝导弹是一个效果）
    【isDamageOwner: bool = False】 对创建者是否造成伤害
    【error: float = 0.0】 误差；范围为[0, 1]；0表示无误差，发射后的实际朝向为direction；1表示最大误差，发射后的实际朝向与direction偏差较大；
    -----------------------------------------------------------
    return: str -> 抛射物ID；创建失败返回"-1"
    """
    if not position:
        position = _ServerCompFactory.CreatePos(spawnerId).GetFootPos()
        if not position:
            return "-1"
        position = (position[0], position[1] + 1.6, position[2])
    if not direction:
        rot = _ServerCompFactory.CreateRot(spawnerId).GetRot()
        if not rot:
            return "-1"
        direction = _serverApi.GetDirFromRot(rot)
    # noise = (_perlin_noise(*direction) * error for _ in range(3))
    # direction = tuple(map(lambda (x, y): x + y, zip(direction, noise)))
    param = {
        'position': position,
        'direction': direction,
        'isDamageOwner': isDamageOwner,
    }
    if power is not None:
        param['power'] = power
    if damage is not None:
        param['damage'] = damage
    if gravity is not None:
        param['gravity'] = gravity
    if targetId:
        param['targetId'] = targetId
    return _LevelProjectileComp.CreateProjectileEntity(spawnerId, projectileName, param)


def entity_plunge(entityId1, entityId2, speed):
    # type: (str, str, float) -> None
    """
    使实体1向实体2的准星方向突进。
    -----------------------------------------------------------
    【entityId1: str】 实体1ID
    【entityId2: str】 实体2ID
    【speed: float】 突进速度
    -----------------------------------------------------------
    NoReturn
    """
    rot = _ServerCompFactory.CreateRot(entityId2).GetRot()
    if not rot:
        return
    entity_plunge_by_rot(entityId1, rot, speed)


def entity_plunge_by_dir(entityId, direction, speed):
    # type: (str, tuple[float, float, float], float) -> tuple[float, float, float]
    """
    使实体以指定方向和速度突进。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【direction: Tuple[float, float, float]】 方向的单位向量
    【speed: float】 速度大小
    -----------------------------------------------------------
    return: Tuple[float, float, float] -> 突进速度向量
    """
    motion = tuple(map(lambda x: x * speed, direction))
    comp = _ServerCompFactory.CreateActorMotion(entityId)
    etype = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    if etype == _EntityType.Player:
        comp.SetPlayerMotion(motion)
    else:
        comp.SetMotion(motion)
    return motion


def entity_plunge_by_rot(entityId, rot, speed):
    # type: (str, tuple[float, float], float) -> None
    """
    使实体向指定视角方向突进。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【rot: Tuple[float, float]】 视角
    【speed: float】 速度
    -----------------------------------------------------------
    NoReturn
    """
    direction = _serverApi.GetDirFromRot(rot)
    entity_plunge_by_dir(entityId, direction, speed)


def get_all_entities():
    # type: () -> list[str]
    """
    获取所有实体，包括玩家。
    -----------------------------------------------------------
    无参数
    -----------------------------------------------------------
    return: List[str] -> 实体ID列表
    """
    return _serverApi.GetEngineActor().keys() + _serverApi.GetPlayerList()


def get_entities_in_area(pos, radius, dimension=0, filterIdList=None, filterTypeIdList=None, filterTypeStrList=None,
                         filterAbiotic=False):
    # type: (tuple[float, float, float], float, int, list[str] | None, list[int] | None, list[str] | None, bool) -> list[str]
    """
    获取给定区域内的所有实体。
    -----------------------------------------------------------
    【pos: Tuple[float, float, float]】 区域中心点坐标
    【radius: float】 区域半径
    【dimension: int = 0】 维度
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【filterTypeStrList: Optional[List[str]] = None】 过滤的实体类型ID列表
    【filterAbiotic: bool = False】 是否过滤非生物实体
    -----------------------------------------------------------
    return: List[str] -> 实体ID列表
    """
    if not pos or radius <= 0:
        return []
    startPos = tuple(i - radius for i in pos)
    endPos = tuple(i + radius for i in pos)
    entities = _LevelGameComp.GetEntitiesInSquareArea(None, startPos, endPos, dimension)
    fa = {_EntityType.Mob} if filterAbiotic else None
    entities = entity_filter(entities, (pos, radius), fa, filterIdList, filterTypeIdList, filterTypeStrList)
    return entities


def get_entities_by_type(typeId, pos=None, dimension=0, radius=0.0):
    # type: (int, tuple[float, float, float], int, float) -> list[str]
    """
    获取指定类型的所有实体。
    -----------------------------------------------------------
    【typeId: int】 实体类型ID（网易版）
    【pos: Tuple[float, float, float] = None】 获取位置坐标（传入None表示全图范围）
    【dimension: int = 0】 获取维度（指定pos时生效）
    【radius: float = 0.0】 获取半径（指定pos时生效）
    -----------------------------------------------------------
    return: List[str] -> 实体ID列表
    """
    if pos:
        startPos = tuple(i - radius for i in pos)
        endPos = tuple(i + radius for i in pos)
        entities = _LevelGameComp.GetEntitiesInSquareArea(None, startPos, endPos, dimension)
        entities = entity_filter(entities, {typeId}, (pos, radius))
    else:
        entities = get_all_entities()
        entities = entity_filter(entities, {typeId})
    return entities


def get_entities_by_name(name):
    # type: (str) -> list[str]
    """
    获取自定义名称为name的所有实体。
    -----------------------------------------------------------
    【name: str】 自定义名称
    -----------------------------------------------------------
    return: List[str] -> 实体ID列表
    """
    result = []
    for i in get_all_entities():
        en = _ServerCompFactory.CreateName(i).GetName()
        if en == name:
            result.append(i)
    return result


def get_entities_by_locking(entityId, getDistance=-1, filterIdList=None, filterTypeIdList=None):
    # type: (str, float, list[str] | None, list[int] | None) -> list[str]
    """
    获取攻击目标为指定生物的所有生物。
    -----------------------------------------------------------
    【entityId: str】 生物的实体ID
    【getDistance: float】 最远获取距离，-1表示无视距离
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    -----------------------------------------------------------
    return: List[str] -> 实体ID列表
    """
    pos = _ServerCompFactory.CreatePos(entityId).GetFootPos()
    if not pos:
        return []
    if filterIdList is None:
        filterIdList = []
    filterIdList.append(entityId)
    ents = get_all_entities()
    r = (pos, getDistance) if getDistance != -1 else None
    ents = entity_filter(ents, r, _EntityType.Mob, filterIdList, filterTypeIdList)
    result = []
    for eid in ents:
        target = _ServerCompFactory.CreateAction(eid).GetAttackTarget()
        if target == entityId:
            result.append(eid)
    return result


def get_nearest_entity(obj, count=1, dim=0, radius=-1.0, filterIdList=None, filterTypeIdList=None, filterAbiotic=False):
    # type: (str | tuple[float, float, float], int, int, float, list[str] | None, list[int] | None, bool) -> str | list[str] | None
    """
    获取距离指定实体或位置最近的实体。
    -----------------------------------------------------------
    【obj: Union[str, Tuple[float, float, float]]】 实体ID或坐标
    【count: int = 1】 获取的实体数量
    【dim: int = 0】 获取维度（obj传入坐标时生效）
    【radius: float = -1.0】 获取半径，-1.0表示全图范围
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【filterAbiotic: bool = False】 是否过滤非生物实体
    -----------------------------------------------------------
    return: Union[str, List[str], None] -> 若count==1，返回实体ID；若count>1，返回实体ID列表；获取不到实体返回None
    """
    if isinstance(obj, str):
        pos = _ServerCompFactory.CreatePos(obj).GetFootPos()
        dim = _ServerCompFactory.CreateDimension(obj).GetEntityDimensionId()
        if filterIdList is None:
            filterIdList = []
        filterIdList = _copy(filterIdList)
        filterIdList.append(obj)
    else:
        pos = obj
    if not pos:
        return
    allEnts = get_all_entities()
    sort_entity_list_by_distance(pos, allEnts)
    r = (pos, radius) if radius != -1 else None
    fa = {_EntityType.Mob} if filterAbiotic else None
    allEnts = entity_filter(allEnts, r, fa, filterIdList, filterTypeIdList, {str(dim)})
    if not allEnts:
        return
    result = allEnts[:count]
    return result if count > 1 else result[0]


def attack_nearest_mob(entityId, r=15.0, filterIdList=None, filterTypeIdList=None):
    # type: (str, float, list[str] | None, list[int] | None) -> str | None
    """
    令指定实体攻击距离其最近的实体。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【r: float = 15.0】 最远攻击距离
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    -----------------------------------------------------------
    return: Optional[str] -> 攻击目标的实体ID；无攻击目标返回None
    """
    nearest = get_nearest_entity(
        entityId, radius=r, filterIdList=filterIdList, filterTypeIdList=filterTypeIdList, filterAbiotic=True
    )
    if nearest:
        _ServerCompFactory.CreateAction(entityId).SetAttackTarget(nearest)
    return nearest


def has_effect(entityId, effectId):
    # type: (str, str) -> bool
    """
    检测生物是否存在指定药水效果。
    -----------------------------------------------------------
    【entityId: str】 生物的实体ID
    【effectId: str】 药水效果ID
    -----------------------------------------------------------
    return: bool -> 存在返回True，否则返回False
    """
    effects = _ServerCompFactory.CreateEffect(entityId).GetAllEffects()
    for effDict in effects:
        if effDict['effectName'] == effectId:
            return True
    return False


def set_entity_motion(entity, motion, serSysCls=None):
    # type: (str, tuple[float, float, float], _ServerSystem | None) -> None
    """
    设置实体瞬时速度，包括玩家。
    设置玩家速度时，强烈建议将客户端继承NuoyanClientSystem，否则可能会出现客户端与服务端不同步的情况导致玩家被强制拉回。继承后客户端将会自动同步。
    -----------------------------------------------------------
    【entity: str】 实体ID
    【motion: Tuple[float, float, float]】 瞬时速度向量
    【serSysCls: Optional[ServerSystem] = None】 服务端实例（控制玩家时传入）
    -----------------------------------------------------------
    NoReturn
    """
    t = _ServerCompFactory.CreateEngineType(entity).GetEngineType()
    if t == _EntityType.Player and serSysCls:
        serSysCls.NotifyToClient(entity, "_SetMotion", motion)
    _ServerCompFactory.CreateActorMotion(entity).SetMotion(motion)



























