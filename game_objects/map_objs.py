import itertools
from typing import Dict

from game_objects.conceptual_objs import Adjacency, Directions


class River:
    river_type: str

    def __init__(self,
                 river_adjacency: Adjacency,
                 coastal_adjacency: Adjacency):

        self.adj_rivers: Adjacency = river_adjacency
        self.adj_coasts: Adjacency = coastal_adjacency

        self.num_river = self.adj_rivers.n_tot
        self.num_coast = self.adj_coasts.n_tot
        self.river_type_str = 'UNDEF'
        self.update_river_type_str()

    def update_river_type_str(self):
        type_dict: Dict[bool, str] = {self.is_solo(): 'SOLO_',
                                     self.is_start(): 'START',
                                     self.is_mouth(): 'MOUTH',
                                     self.is_next_to_coast(): 'COAST',
                                     self.is_crossing(): 'CROSS'}

        river_type_str = '_AND_'.join(rtype for key, rtype in type_dict.items())
        if not river_type_str:
            river_type_str = 'UNDEF'
        self.river_type_str = river_type_str

    def encode(self,
               section_sep: str = '@',
               coastal_adj_demarkation: str = 'CADJ',
               river_adj_demarkation: str ='RADJ',
               sum_demarkation: str ='SADJ') -> str:
        """
        Encodes position/adjacency/state of river into string.
        Encoding comprises a 5-letter prefix followed by 4 numbers (N -> W -> S -> E, then sum of coastal + river adjacency encoded by another 8 numbers.
        Indicated, indicating their sum.
        SOLO_: solo
        CROSS: crossing
        COAST: next to coast
        MOUTH: is river mouth
        UNDEF: undefined (edge case?)
        """

        self.update_river_type_str()
        sections = [self.river_type_str]

        for adj_demarkation, adj_instance in zip((river_adj_demarkation,coastal_adj_demarkation,sum_demarkation),
                                          (self.adj_rivers, self.adj_coasts, self.adj_coasts+self.adj_rivers)):
            sections.extend([adj_demarkation, ''.join(str(int(bool(x))) for x in [adj_instance.north, adj_instance.west,
                                                           adj_instance.south, adj_instance.east])])
        return section_sep.join(sections)


    def is_solo(self) -> bool:
        return self.num_river == 0 and self.num_coast == 1

    def is_crossing(self) -> bool:
        """
        Detect when a crossing should be used, total of 2 cases;
         First case: 3 adjacent rivers
         Second case: 2 adjacent rivers and an adjacent coast.
        """
        return self.num_river >= 3 or (self.num_coast == 1 and self.num_river == 2)

    def is_start(self) -> bool:
        """River starts only have 1 river next to them, and never a coast."""
        return self.num_river == 1 and self.num_coast == 0

    def is_next_to_coast(self) -> bool:
        return self.num_coast > 0

    def is_mouth(self) -> bool:
        return (
                    (self.is_next_to_coast())
                    and
                    (
                            (self.adj_coasts.north and self.adj_rivers.south) or
                            (self.adj_coasts.west and self.adj_rivers.east) or
                            (self.adj_coasts.east and self.adj_rivers.west) or
                            (self.adj_coasts.south and self.adj_rivers.north)
                    )
        )

    def crossing_direction(self):
        adjsum = self.adj_coasts + self.adj_rivers
        if adjsum.north and adjsum.west and adjsum.south:
            return Directions.LEFT

    def get_sprite(self):
        pass


if __name__ == '__main__':
    all_adjmats = tuple(itertools.product([1, 0], repeat=8))

    all_river_coast_adj_combos = itertools.combinations_with_replacement([all_adjmats, all_adjmats], r=2)
    rivers = []

    for coastal_adjs, river_adjs in all_river_coast_adj_combos:
        for coastal_adj in coastal_adjs:
            for river_adj in river_adjs:
                if coastal_adj != river_adj:
                    river = River(coastal_adjacency=Adjacency(coastal_adj),
                                        river_adjacency=Adjacency(river_adj))
                    print(river.encode())

