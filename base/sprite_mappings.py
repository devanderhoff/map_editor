from typing import Dict, Set, Tuple

from PIL import Image, PngImagePlugin
import numpy as np
from base.sprites import Sprites

# Type aliases
from utils.utils import default_repr, funcname
from utils.custom_exceptions import MethodCannotBeCalledOnBaseClassError

Sprite = PngImagePlugin.PngImageFile


class SpriteMappingBase:

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
        self.mapping_namekey: str = 'name'

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

    def get_sprite(self,
                   sprite_type: str,
                   **kwargs) -> Tuple[Sprite, bool]:
        """
        Gets sprite object corresponding to a combination of the relevant IDs.

        :returns: Tuple[Sprite, bool] (bool indicates wheter a sprite was found (True) or was empty (False))
        """
        if type(self) == SpriteMappingBase:
            raise MethodCannotBeCalledOnBaseClassError

        self._validate_get_sprite_kwargs(**kwargs)

        cur_sprite_dict = self._get_spritedict(sprite_type=sprite_type)
        cvr_id_str = ''.join(str(id_) for id_ in (kwargs.values()))

        try:
            return cur_sprite_dict[cvr_id_str], True
        except KeyError:
            return self.try_wildcard_keys(cvr_id_str=cvr_id_str, sprite_dict=cur_sprite_dict)

    def try_wildcard_keys(self,
                          cvr_id_str: str,
                          sprite_dict: Dict[str, Sprite]) -> Tuple[Sprite, bool]:

        for istr in reversed(range(len(cvr_id_str))):

            cvr_id_w_wildcard = f"{cvr_id_str[:istr]}{self.wildcard * (len(cvr_id_str) - istr)}"
            try:
                return sprite_dict[cvr_id_w_wildcard], True
            except KeyError:
                continue
        else:
            return self.fallback_sprite, False

    @classmethod
    def _get_spritedict(cls, sprite_type: str) -> Dict[str, Sprite]:
        sprite_type_uppercase = sprite_type.upper()

        if hasattr(cls, sprite_type_uppercase):
            return getattr(cls, sprite_type_uppercase)

        else:
            raise AttributeError(''.join([
                f"{cls.__name__}() does not have a sprite dictionary for ",
                f"sprite type {sprite_type!r} nor {sprite_type_uppercase!r}... ",
                f"""Valid alternatives: ['{", ".join(attr for attr in dir(cls)
                                                     if not '_' in attr and attr.isupper())}']"""]))

    def _validate_get_sprite_kwargs(self, **kwargs):
        if set(kwargs.keys()) != set(self.ID_KEYS):
            raise ValueError(''.join([f"{type(self).__name__}.{funcname()}() reports: ",
                                      "keyword arguments passed to this method ",
                                      "must consist of exactly these keys: ",
                                      ', '.join([f'{idkey!r}' for idkey in self.ID_KEYS])]))

    def __repr__(self):
        return default_repr(self)


class SpriteMappingVegetation(SpriteMappingBase):

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
                   sprite_type: str,
                   climate_id: int,
                   vegetation_id: int,
                   relief_id: int) -> Tuple[Sprite, bool]:
        """
        Gets sprite object corresponding to a combination of climate/vegetation/relief IDs.

        :returns: Tuple[Sprite, bool] (bool indicates wheter a sprite was found (True) or was empty (False))
        """
        kwargs = {'sprite_type': sprite_type, 'climate_id': climate_id,
                  'vegetation_id': vegetation_id, 'relief_id': relief_id}
        return super().get_sprite(sprite_type=sprite_type, **kwargs)


class SpriteMappingRiver(SpriteMappingBase):
    ID_KEYS: Set[str] = {'water_id', 'river_adjacency', 'coastal_adjacency'}

    MAPPING: Dict[str, Sprite] = {
        '4**': Sprites.sprite_lake,
        '5**': Sprites.sprite_swamp,
        '6**': Sprites.sprite_oceanic_trees,
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


# water_id, river_adjacency, coastal_adjacency

if __name__ == '__main__':
    fbs = Image.fromarray(np.zeros((225, 300, 4,)).astype(np.uint8))
    SpriteMappingBase(fallback_sprite=fbs)