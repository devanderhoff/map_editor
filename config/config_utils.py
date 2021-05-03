import collections
from dataclasses import dataclass

import pandas as pd
import numpy as np
from ruamel.yaml import YAML
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import itertools
from tabulate import tabulate

# def generate_subtyle_cls():
#     return collections.namedtuple('')
# class TileSubTypeOverlay(collections.namedtuple):
#     name: str
#     id: int
#
# @dataclass
# class TileTypeOverlay:
#     name: str


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)


class TileTypeOverlays:
    META_ALIAS_PATH: Path = Path(__file__).parent.joinpath('tile_metatype_aliases.yaml')
    TILE_CONFIG_PATH: Path = Path(__file__).parent.joinpath('terrain_type_mapping.yaml')
    OUTPUT_TILE_SCORE_PATH: Path = Path(__file__).parent.joinpath('subtile_combination_scores.fwf')
    PENALTY_COLNAME = 'COMBO_PENALTY'

    def __init__(self, random_penalties: bool = False):
        self.tile_config: Dict[str, Dict[str, int]] = self.load_tile_config()
        self.meta_types: List[str] = list(self.tile_config.keys())
        self.meta_type_aliases: Dict[str, str] = self.load_metatype_alias_config()
        self.random_penalties: bool = random_penalties

    def _get_longest_subtile_name_len(self) -> int:
        return max([len(subtypekey) for subkeys in self.tile_config.values()
                    for subtypekey in subkeys.keys()])

    def generate_equal_width_config_file(self, tgt_path: Path = OUTPUT_TILE_SCORE_PATH):
        col_width = self._get_longest_subtile_name_len()
        if col_width < len(self.PENALTY_COLNAME):
            col_width = len(self.PENALTY_COLNAME)

        colnames = [self.PENALTY_COLNAME]

        for tile_name, subtile_dict in self.tile_config.items():
            for subtile_name, subtile_id in subtile_dict.items():
                colnames.append(
                    f'{self.meta_type_aliases[tile_name].upper()}_{subtile_name.upper()}')


        subtile_tuples = [tuple(subdict.keys()) for subdict in self.tile_config.values()]

        subtile_combos = list(product_dict(**self.tile_config))

        cfg_df = pd.DataFrame(columns=colnames,
                                      data=np.zeros(shape=(len(subtile_combos), len(colnames)), dtype=np.uint8))
        cfg_df[self.PENALTY_COLNAME] = cfg_df[self.PENALTY_COLNAME].astype(np.int64)

        for icombo, combo in enumerate(subtile_combos):
            for tile_metatype, tile_type in combo.items():
                colname = f'{self.meta_type_aliases[tile_metatype].upper()}_{tile_type.upper()}'
                cfg_df.loc[cfg_df.index[icombo], colname] = 1

        if self.random_penalties:
            cfg_df.loc[:, self.PENALTY_COLNAME] = np.random.randint(low=1, high=100, size=cfg_df.shape[0])
        to_fwf(df=cfg_df, fname=tgt_path)

    def load_metatype_alias_config(self, path: Path = META_ALIAS_PATH) -> Dict[str, str]:
        """
        Loads terrain metatype alias mappings. e.g. CLIMATE -> CL, RELIEF -> RF
        :param path: (Optional) pathlib.Path object pointing to config file
            (Default = META_ALIAS_PATH)
        """
        return self.load_yaml(path=path)

    def load_tile_config(self, path: Path = TILE_CONFIG_PATH) -> Dict[str, Dict[str, int]]:
        """
        Loads terrain type nested dict with as values int:value type maping.
        :param path: (Optional) pathlib.Path object pointing to config file
            (Default = TILE_CONFIG_PATH)
        """
        return self.load_yaml(path=path)

    @staticmethod
    def load_yaml(path: Path) -> Dict[Any, Any]:
        return YAML(typ='safe').load(path)

    def check_tile_and_meta_type_cfgs(self):
        """
        Check that the set of meta type aliases described in tile_metatype_aliases
        is equal to tiles defined in the tile config.
        """
        tilecfg_keys = set(self.tile_config.keys())
        meta_type_keys = set(self.meta_type_aliases.keys())
        missing = tilecfg_keys.symmetric_difference(meta_type_keys)
        if missing:
            raise ValueError(''.join(["1 or more keys were found in the ",
                                      "meta tile type alias configuration file which aren't ",
                                      "in the tile config file, or vice versa: ",
                                      f" {', '.join(missing)}"]))
        if any(len(meta_type_alias) != 2
               for meta_type_alias in self.meta_type_aliases.values()):
            raise ValueError("Meta type aliases must consist of two characters. (e.g. CLIMATE: CL)")

        if len(set(self.meta_type_aliases.values())) != len(self.meta_type_aliases.values()):
            raise ValueError("Meta type aliases must be unique.")

    def __repr__(self):
        return f"{type(self).__name__}(meta_types={self.meta_types})"


if __name__ == '__main__':
    tov = TileTypeOverlays()
    tov.generate_equal_width_config_file()
