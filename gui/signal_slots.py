from game_objects.object_types import PrimitiveType, UtilityType, ClimateType, ReliefType, VegetationType, \
    WaterType

class SignalSlot:
    ## CLIMATE BUTTONS ##
    def press_climate_button_sea(self):
        self.cur_paint_id = ClimateType.SEA
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_cont(self):
        self.cur_paint_id = ClimateType.CONTINENTAL
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_oceanic(self):
        self.cur_paint_id = ClimateType.OCEANIC
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_medi(self):
        self.cur_paint_id = ClimateType.MEDITTERANEAN
        self.brush_id = 0
        # return self.paint_climate

    def press_climate_button_tropical(self):
        self.cur_paint_id = ClimateType.TROPICAL
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_arid(self):
        self.cur_paint_id = ClimateType.ARID
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_desert(self):
        self.cur_paint_id = ClimateType.DESERT
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_nordic(self):
        self.cur_paint_id = ClimateType.NORDIC
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_polar(self):
        self.cur_paint_id = ClimateType.POLAR
        self.brush_id = 0
        # return self.paint_climate

    ## RELIEF BUTTONS ##
    def press_relief_button_none(self):
        self.cur_paint_id = ReliefType.FLAT
        self.brush_id = 1

    def press_relief_button_plains(self):
        self.cur_paint_id = ReliefType.PLAIN
        self.brush_id = 1

    def press_relief_button_rocky(self):
        self.cur_paint_id = ReliefType.ROCKY
        self.brush_id = 1

    def press_relief_button_hills(self):
        self.cur_paint_id = ReliefType.HILLS
        self.brush_id = 1

    def press_relief_button_mountains(self):
        self.cur_paint_id = ReliefType.MOUNTAINS
        self.brush_id = 1

    ## Vegetation buttons
    def press_vegetation_button_none(self):
        self.cur_paint_id = VegetationType.NONE
        self.brush_id = 2

    def press_vegetation_button_forest(self):
        self.cur_paint_id = VegetationType.FOREST
        self.brush_id = 2

    ## River buttons
    def press_river_button_none(self):
        self.cur_paint_id = WaterType.NONE
        self.brush_id = 3

    def press_river_button_estuary(self):
        self.cur_paint_id = WaterType.RIVER_SMALL
        self.brush_id = 3

    def press_river_button_river(self):
        self.cur_paint_id = WaterType.RIVER_MED
        self.brush_id = 3

    def press_river_button_maw(self):
        self.cur_paint_id = WaterType.RIVER_LARGE
        self.brush_id = 3

    def press_river_button_lake(self):
        self.cur_paint_id = WaterType.LAKE
        self.brush_id = 3

    def press_river_button_swamp(self):
        self.cur_paint_id = WaterType.SWAMP
        self.brush_id = 3

    def press_primitive_button_none(self):
        self.cur_paint_id = PrimitiveType.NONE
        self.brush_id = 4

    def press_primitive_button_prim(self):
        self.cur_paint_id = PrimitiveType.PRIM
        self.brush_id = 4

    def press_utility_button_only_sea(self):
        self.cur_paint_id = UtilityType.ONLY_SEA
        self.brush_id = 5

    def press_utility_button_cont_flatlands(self):
        self.cur_paint_id = UtilityType.CONT_FLATLANDS
        self.brush_id = 5

