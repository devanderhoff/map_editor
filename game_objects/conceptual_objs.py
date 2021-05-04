from __future__ import annotations

from enum import IntEnum
from typing import List, Union

import numpy as np
from numpy import ndarray


class Directions(IntEnum):
    """Defines direction names and there indices"""
    NORTH = N = TOP = 0
    NORTHWEST = NW = UPPERLEFT = 1
    WEST = W = LEFT = 2
    SOUTHWEST = SW = LOWERLEFT = 3
    SOUTH = S = BOTTOM = BOT = 4
    SOUTHEAST = SE = LOWERRIGHT = 5
    EAST = E = RIGHT = 6
    NORTHEAST = NE = UPPERRIGHT = 7


class Adjacency:

    def __init__(self, adjacency_list_or_arr: Union[List[int], ndarray]):

        self.adjacency_arr: ndarray = np.asarray(adjacency_list_or_arr)

        assert self.adjacency_arr.ndim == 1, "Adjacency list or arr should be passed as 1D list/array."

        self.n_tot: int = self.adjacency_arr.sum()

    # Directions here are properties, such that if adjacency_arr is updated,
    #  directions are as well.
    @property
    def north(self) -> int:
        return self.adjacency_arr[Directions.NORTH]

    @property
    def northwest(self) -> int:
        return self.adjacency_arr[Directions.NORTHWEST]

    @property
    def west(self) -> int:
        return self.adjacency_arr[Directions.NORTHEAST]

    @property
    def southwest(self) -> int:
        return self.adjacency_arr[Directions.SOUTHWEST]

    @property
    def south(self) -> int:
        return self.adjacency_arr[Directions.SOUTH]

    @property
    def southeast(self) -> int:
        return self.adjacency_arr[Directions.SOUTHEAST]

    @property
    def east(self) -> int:
        return self.adjacency_arr[Directions.EAST]

    @property
    def northeast(self) -> int:
        return self.adjacency_arr[Directions.NORTHEAST]

    def __add__(self, other: Adjacency):
        self.adjacency_arr += other.adjacency_arr
        self.n_tot += other.n_tot
        return self

    def __sub__(self, other: Adjacency):
        self.adjacency_arr -= other.adjacency_arr
        self.n_tot -= other.n_tot
        return self

    def __mul__(self, other: Adjacency):
        self.adjacency_arr = np.multiply(self.adjacency_arr, other.adjacency_arr)
        self.n_tot *= other.n_tot
        return self

    def __div__(self, other: Adjacency):
        self.adjacency_arr = np.divide(self.adjacency_arr, other.adjacency_arr)
        self.n_tot = round(self.n_tot / other.n_tot)
