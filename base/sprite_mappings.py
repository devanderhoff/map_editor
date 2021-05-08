from typing import Dict, List, Set, Tuple

from PIL import Image, PngImagePlugin
import numpy as np
from base.sprites import Sprites

# Type aliases
from game_objects.map_objs import River
from utils.utils import default_repr, funcname
from utils.custom_exceptions import MethodCannotBeCalledOnBaseClassError

Sprite = PngImagePlugin.PngImageFile


class SpriteMapperBase:

    NAME: str = 'SpriteMappingBaseClass'
    ID_KEYS: Set[str] = {'example_id', 'another_id', 'someother_id_key'}

    MAPPING: Dict[str, Sprite] = {
        '0011': 'ExampleSprite000_which_would_be_a_sprite_object_not_a_string',
        '1001': 'ExampleSprite100',
        '10*1': 'ExampleSprite100_or_101_or_102_etc',
        '1021': 'ExampleSprite102_has_priority_over_examplesprite_10*',
    }

    def __init__(self, fallback_sprite: Sprite, wildcard: str = '*'):
        """
        Class used to map a set of IDs or parameters to Sprite objects.

        :param fallback_sprite: Sprite to return if the combination IDs/parameters was not found in the mapping.
        """
        self.wildcard: str = wildcard
        self.fallback_sprite: Sprite = fallback_sprite

        self.validate_mapping_keys()

    def validate_mapping_keys(self):

        err_prefix = f"{type(self).__name__}.{funcname()}() reports: "
        mapping_name = f"{type(self).__name__}(name={self.NAME!r}).MAPPING. "

        if not len(set(len(key) for key in self.MAPPING.keys())) == 1:  # I.e. if not all key lengths are the same
            raise ValueError(''.join([err_prefix, "Keys of different lengths occur in mapping ",
                                      mapping_name, " All mapping keys must be strings of equal length."]))

        if len(list(self.MAPPING.keys())[0]) != len(self.ID_KEYS):
            raise ValueError(''.join([err_prefix, "Keys for mapping ",
                                      mapping_name, " must be of the same length as ",
                                      "the number of mapping IDs in the ID_KEYS attribute,",
                                      " as they have a one-to-one correspondence."]))

    def get_sprite(self, **kwargs) -> Tuple[Sprite, bool]:
        """
        Gets sprite object corresponding to a combination of the relevant IDs.

        :returns: Tuple[Sprite, bool] (bool indicates wheter a sprite was found (True) or was empty (False))
        """
        if type(self) == SpriteMapperBase:
            raise MethodCannotBeCalledOnBaseClassError

        self._validate_get_sprite_kwargs(**kwargs)

        cvr_id_str = ''.join(str(id_) for id_ in (kwargs.values()))

        try:
            return self.MAPPING[cvr_id_str], True
        except KeyError:
            return self.try_wildcard_keys(cvr_id_str=cvr_id_str)

    def try_wildcard_keys(self,
                          cvr_id_str: str) -> Tuple[Sprite, bool]:

        for istr in reversed(range(len(cvr_id_str))):

            cvr_id_w_wildcard = f"{cvr_id_str[:istr]}{self.wildcard * (len(cvr_id_str) - istr)}"
            try:
                return self.MAPPING[cvr_id_w_wildcard], True
            except KeyError:
                continue
        else:
            return self.fallback_sprite, False

    def _validate_get_sprite_kwargs(self, **kwargs):
        if set(kwargs.keys()) != set(self.ID_KEYS):
            raise ValueError(''.join([f"{type(self).__name__}.{funcname()}() reports: ",
                                      "keyword arguments passed to this method ",
                                      "must consist of exactly these keys: ",
                                      ', '.join([f'{idkey!r}' for idkey in self.ID_KEYS])]))

    def __repr__(self):
        return default_repr(self)


class SpriteMapperContainer:

    def __init__(self, sprite_mappers: List[SpriteMapperBase]):
        self._mappers = {smap.NAME: smap for smap in sprite_mappers}

    def __getitem__(self, key):
        for keyvariant in (key, key.lower(), key.upper()):
            try:
                return self._mappers[keyvariant]
            except KeyError as err:
                continue
        raise KeyError(f"{type(self).__name__} does not contain a SpriteMapper for key {key!r}") from err

    def __delitem__(self, key):
        del self._mappers[key]

    def __contains__(self, key_or_instance):
        if type(key_or_instance) == str:
            return key_or_instance in self._mappers
        elif isinstance(key_or_instance, SpriteMapperBase):
            return key_or_instance in self._mappers.values()


class SpriteMapperVegetation(SpriteMapperBase):

    NAME: str = 'VEGETATION'

    ID_KEYS: Set[str] = {'climate_id', 'vegetation_id', 'relief_id'}

    MAPPING: Dict[str, Sprite] = {
        '100': Sprites.sprite_cont_trees,
        '11*': Sprites.sprite_cont_forest,
        '200': Sprites.sprite_oceanic_trees,
        '201': Sprites.sprite_oceanic_forest,
        '300': Sprites.sprite_medi_trees,
        '31*': Sprites.sprite_medi_forest,
        '400': Sprites.sprite_tropical_trees,
        '41*': Sprites.sprite_tropical_forest,
        '500': Sprites.sprite_arid_trees,
        '51*': Sprites.sprite_arid_forest,
        '700': Sprites.sprite_nordic_trees,
        '71*': Sprites.sprite_nordic_forest,
    }

    def __init__(self, fallback_sprite: Sprite, wildcard: str = '*'):
        """
        Class used to map climate/vegetation/relief IDs to Sprite objects.

        :param fallback_sprite: Sprite to return if the combination of climate/vegetation/relief IDs was not found in the mapping.
        """
        super().__init__(fallback_sprite=fallback_sprite,
                         wildcard=wildcard)

    def get_sprite(self,
                   climate_id: int,
                   vegetation_id: int,
                   relief_id: int) -> Tuple[Sprite, bool]:
        """
        Gets sprite object corresponding to a combination of climate/vegetation/relief IDs.

        :returns: Tuple[Sprite, bool] (bool indicates wheter a sprite was found (True) or was empty (False))
        """
        return super().get_sprite(**{'climate_id': climate_id, 'vegetation_id': vegetation_id, 'relief_id': relief_id})


class SpriteMapperRiver(SpriteMapperBase):
    NAME = 'RIVER'
    ID_KEYS: Set[str] = {'water_id',
                         'river_id',
                         'next_to_coast',
                         'crossing',
                         'solo_river',
                         'coastal_adjacency',
                         'river_adjacency'}

    MAPPING: Dict[str, Sprite] = {

    }

    def get_sprite(self,
                   water_id: int,
                   river_adjacency: List[int],
                   coastal_adjacency: List[int]) -> Tuple[Sprite, bool]:
        """
        Gets sprite object corresponding to a combination of water ID, river adjacency and coastal adjacency.

        :returns: Tuple[Sprite, bool] (bool indicates wheter a sprite was found (True) or was empty (False))
        """


        river = River(river_adjacency=river_adjacency, coastal_adjacency=coastal_adjacency)

        river_encoding_str = river.encode()

        #return super().get_sprite(**{'water_id': water_id,
         #                            'river_id': river_adjacency,
          #                           'coastal_id': coastal_adjacency})






# water_id, river_adjacency, coastal_adjacency

if __name__ == '__main__':
    fbs = Image.fromarray(np.zeros((225, 300, 4,)).astype(np.uint8))
    SpriteMapperBase(fallback_sprite=fbs)