import pandas as pd
import numpy as np
from ruamel.yaml import YAML
from pathlib import Path
from typing import Any, Dict, List
import itertools
from tqdm import tqdm
import shutil
from utils.log import get_logger

logger = get_logger(__name__)


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


class TileTypeOverlayConfigGenerator:
    TILE_CONFIG_PATH: Path = Path(__file__).parent.joinpath('terrain_type_mapping.yaml')
    OUTPUT_TILE_SCORE_PATH: Path = Path(__file__).parent.joinpath('subtile_combination_scores.tsv')
    PENALTY_COLNAME = 'COMBO_PENALTY'

    def __init__(self, random_initial_penalties: bool = True):
        self.tile_config: Dict[str, Dict[str, int]] = self.load_tile_config()
        self.meta_types: List[str] = list(self.tile_config.keys())

        self.cfg_combo_dframe: pd.DataFrame = pd.DataFrame()
        self.random_initial_penalties: bool = random_initial_penalties

    def generate_equal_width_config_file(self, tgt_path: Path = OUTPUT_TILE_SCORE_PATH):

        self.cfg_combo_dframe = self.init_combo_dframe()

        self.cfg_combo_dframe = self.fill_dataframe(combo_df=self.cfg_combo_dframe)

        self.backup_if_exists(tgt_path=tgt_path)

        self.cfg_combo_dframe.to_csv(path_or_buf=tgt_path, sep='\t')

        logger.info("Saved combo dataframe to %s", str(tgt_path.absolute()))

    @staticmethod
    def backup_if_exists(tgt_path: Path):
        if tgt_path.exists():
            logger.info(''.join(["Found existing combo dataframe file; ",
                                 "copying current one to backup to prevent overwriting ",
                                 "of manually and painstakingly adjusted scores."]))
            backup_file_path = tgt_path.parent.joinpath(tgt_path.with_suffix(f'{tgt_path.suffix}.LAST').name)

            shutil.copy(src=tgt_path, dst=backup_file_path)

    def get_subtile_combos(self) -> List[Dict[str, str]]:
        # Get all combinations of tile_meta_type: tile_subtype
        return list(product_dict(**self.tile_config))

    def get_combo_dframe_column_names(self) -> List[str]:
        """Builds columns for dataframe (e.g. CLIMATE_SEA, CLIMATE_CONTINENTAL)"""
        # Make column names
        colnames = [self.PENALTY_COLNAME]
        for tile_metatype, subtile_dict in self.tile_config.items():
            for subtile_type, subtile_id in subtile_dict.items():
                colnames.append('_'.join([tile_metatype, subtile_type]))
        return colnames

    def init_combo_dframe(self) -> pd.DataFrame:
        colnames = self.get_combo_dframe_column_names()
        subtile_combos = self.get_subtile_combos()

        cfg_df = pd.DataFrame(columns=colnames,
                              data=np.zeros(shape=(len(subtile_combos), len(colnames)),
                                            dtype=np.uint8))
        cfg_df[self.PENALTY_COLNAME] = cfg_df[self.PENALTY_COLNAME].astype(np.int64)
        return cfg_df

    def fill_dataframe(self,
                       combo_df: pd.DataFrame) -> pd.DataFrame:

        subtile_combos = self.get_subtile_combos()

        for icombo, combo in tqdm(enumerate(subtile_combos), total=len(subtile_combos),
                                  desc='Filling combo dataframe...',
                                  unit=' subtile type combinations'):
            for tile_metatype, subtile_type in combo.items():
                colname = '_'.join([tile_metatype, subtile_type])
                combo_df.loc[combo_df.index[icombo], colname] = 1

        if self.random_initial_penalties:
            combo_df.loc[:, self.PENALTY_COLNAME] = np.random.randint(low=1, high=100, size=combo_df.shape[0])

        return combo_df

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

    def __repr__(self):
        return f"{type(self).__name__}(meta_types={self.meta_types})"


if __name__ == '__main__':
    tov = TileTypeOverlayConfigGenerator()
    tov.generate_equal_width_config_file()
