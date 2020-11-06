from dataclasses import dataclass
from typing import Tuple, Optional, List, Any

import numpy as np
from numpy import ndarray

from utils.log import get_logger


@dataclass
class Colours:
    
    blank_canvas: ndarray
    empty_array: ndarray
    
    # COLOURs
    COLOUR_SEA: ndarray = np.array([70, 119, 152, 255])
    COLOUR_CONTINENTAL: ndarray = np.array([120, 128, 58, 255])
    COLOUR_OCEANIC: ndarray = np.array([86, 153, 69, 255])
    COLOUR_MEDITERRANEAN: ndarray = np.array([182, 159, 97, 255])
    COLOUR_TROPICAL: ndarray = np.array([122, 156, 35, 255])
    COLOUR_ARID: ndarray = np.array([190, 149, 72, 255])
    COLOUR_DESERT: ndarray = np.array([187, 169, 132, 255])
    COLOUR_NORDIC: ndarray = np.array([120, 156, 101, 255])
    COLOUR_POLAR: ndarray = np.array([190, 190, 190, 255])
    COLOUR_GREY: ndarray = np.array([45, 45, 45, 255])

    COLOUR_SEA_ARR: Optional[ndarray] = None
    COLOUR_CONT_ARR: Optional[ndarray] = None
    COLOUR_OCEANIC_ARR: Optional[ndarray] = None
    COLOUR_MEDI_ARR: Optional[ndarray] = None
    COLOUR_TROPICAL_ARR: Optional[ndarray] = None
    COLOUR_ARID_ARR: Optional[ndarray] = None
    COLOUR_DESERT_ARR: Optional[ndarray] = None
    COLOUR_NORDIC_ARR: Optional[ndarray] = None
    COLOUR_POLAR_ARR: Optional[ndarray] = None
    COLOUR_UNKNOWN_ARR: Optional[ndarray] = None

    BACKGROUND: Optional[ndarray] = None

    def __post_init__(self):
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)
        self.update()

    def update(self, blank_canvas: Optional[ndarray] = None, empty_array: Optional[ndarray] = None):
        """Updates colours for new blank canvas or empty array size"""

        if blank_canvas is not None:
            self.blank_canvas = blank_canvas
        if empty_array is not None:
            self.empty_array = empty_array

        self.COLOUR_SEA_ARR = self.COLOUR_SEA * self.blank_canvas
        self.COLOUR_CONT_ARR = self.COLOUR_CONTINENTAL * self.blank_canvas
        self.COLOUR_OCEANIC_ARR = self.COLOUR_OCEANIC * self.blank_canvas
        self.COLOUR_MEDI_ARR = self.COLOUR_MEDITERRANEAN * self.blank_canvas
        self.COLOUR_TROPICAL_ARR = self.COLOUR_TROPICAL * self.blank_canvas
        self.COLOUR_ARID_ARR = self.COLOUR_ARID * self.blank_canvas
        self.COLOUR_DESERT_ARR = self.COLOUR_DESERT * self.blank_canvas
        self.COLOUR_NORDIC_ARR = self.COLOUR_NORDIC * self.blank_canvas
        self.COLOUR_POLAR_ARR = self.COLOUR_POLAR * self.blank_canvas
        self.COLOUR_UNKNOWN_ARR = self.COLOUR_GREY * self.blank_canvas

        self.BACKGROUND: Tuple[ndarray, ...] = (self.COLOUR_SEA_ARR, self.COLOUR_CONT_ARR, self.COLOUR_OCEANIC_ARR,
                                                self.COLOUR_MEDI_ARR, self.COLOUR_TROPICAL_ARR, self.COLOUR_ARID_ARR,
                                                self.COLOUR_DESERT_ARR, self.COLOUR_NORDIC_ARR, self.COLOUR_POLAR_ARR,
                                                self.COLOUR_UNKNOWN_ARR)

    def get_color_attributes(self) -> List[Tuple[str, Any]]:
        """Returns list of tuples with attribute names related to colour and their corresponding values"""
        return [(attr, self.__getattribute__(attr),) for attr in self.__dict__ if attr.isupper()]
