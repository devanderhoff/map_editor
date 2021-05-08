from __future__ import annotations

import enum
from enum import IntEnum
from typing import Dict, Optional, Tuple, Union


class EntMeta(type):
    _instances = {}

    def __new__(mcs, classname: str, base_classes: Tuple[type], attrs: Dict) -> EntMeta:
        qualname = attrs.get('__qualname__')
        if qualname not in EntMeta._instances:
            EntMeta._instances[qualname] = super().__new__(mcs, classname, base_classes, attrs)

        return EntMeta._instances[qualname]

    def __call__(cls, entity: str, label: Optional[str] = None) -> EntMeta:
        if label is None:
            qualname = entity
        else:
            qualname = '.'.join([entity, label])
        try:
            return cls._instances[qualname]
        except KeyError:
            raise ValueError(f"{qualname} is not a recognized entity")


class Entity(metaclass=EntMeta):
    pass


class Label(metaclass=EntMeta):

    @property
    def spellings(self) -> List[str]:
        raise NotImplementedError

class PeriodLabel(Label):

    @property
    def months(self) -> int:
        raise NotImplementedError

@enum.unique
class ObjectTypeEnum(IntEnum):
    pass



class ClimateType(ObjectTypeEnum):
    SEA = 0
    CONTINENTAL = 1
    OCEANIC = 2
    MEDITTERANEAN = 3
    TROPICAL = 4
    ARID = 5
    DESERT = 6
    NORDIC = 7
    POLAR = 8
    UNKNOWN = -1


class ReliefType(ObjectTypeEnum):
    FLAT = 0
    PLAIN = 1
    ROCKY = 2
    HILLS = 3
    MOUNTAINS = 4


class VegetationType(ObjectTypeEnum):
    NONE = 0
    FOREST = 1


class WaterType(ObjectTypeEnum):
    NONE = 0
    RIVER_SMALL = 1
    RIVER_MED = 2
    RIVER_LARGE = 3
    LAKE = 4
    SWAMP = 5


class WorldObjectType(ObjectTypeEnum):
    NONE = 0
    SPAWN = 1


class UtilityType(ObjectTypeEnum):
    ONLY_SEA = 0
    CONT_FLATLANDS = 1


class PrimitiveType(ObjectTypeEnum):
    NONE = 0
    PRIM = 1


class ObjectTypes:
    CLIMATE: ClimateType = ClimateType
    RELIEF: ReliefType = ReliefType
    VEGETATION: VegetationType = VegetationType
    WATER: WaterType = WaterType
    WORLD_OBJECT: WorldObjectType = WorldObjectType
    UTILITY: UtilityType = UtilityType

    _MAPPING = {x: type_enum for x, type_enum in enumerate((CLIMATE, RELIEF, VEGETATION, WATER, WORLD_OBJECT, UTILITY))}

    def __get_item__(self, key: Union[int, str, ObjectTypeEnum]) -> ObjectTypeEnum:
        if type(key) == int:
            return self._MAPPING[key]
        elif type(key) == str:
            return getattr(self, key)
        elif type(key) == ObjectTypeEnum:
            for val in vars(self).values():
                if type(val) == type(key):
                    return val


if __name__ == '__main__':
    print(f"Temporary breakpoint in {__name__}")
