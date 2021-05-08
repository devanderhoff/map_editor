class SignalSlot:
    ## CLIMATE BUTTONS ##
    def press_climate_button_sea(self):
        self.cur_paint_id = 0
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_cont(self):
        self.cur_paint_id = 1
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_oceanic(self):
        self.cur_paint_id = 2
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_medi(self):
        self.cur_paint_id = 3
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_tropical(self):
        self.cur_paint_id = 4
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_arid(self):
        self.cur_paint_id = 5
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_desert(self):
        self.cur_paint_id = 6
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_nordic(self):
        self.cur_paint_id = 7
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_polar(self):
        self.cur_paint_id = 8
        self.brush_id = 0
        # return self.paint_climate

    ## RELIEF BUTTONS ##
    def press_relief_button_none(self):
        self.cur_paint_id = 0
        self.brush_id = 1

    def press_relief_button_plains(self):
        self.cur_paint_id = 1
        self.brush_id = 1

    def press_relief_button_rocky(self):
        self.cur_paint_id = 2
        self.brush_id = 1

    def press_relief_button_hills(self):
        self.cur_paint_id = 3
        self.brush_id = 1

    def press_relief_button_mountains(self):
        self.cur_paint_id = 4
        self.brush_id = 1

    ## Vegetation buttons
    def press_vegetation_button_none(self):
        self.cur_paint_id = 0
        self.brush_id = 2

    def press_vegetation_button_forrest(self):
        self.cur_paint_id = 1
        self.brush_id = 2

    ## River buttons
    def press_river_button_none(self):
        self.cur_paint_id = 0
        self.brush_id = 3

    def press_river_button_estuary(self):
        self.cur_paint_id = 1
        self.brush_id = 3

    def press_river_button_river(self):
        self.cur_paint_id = 2
        self.brush_id = 3

    def press_river_button_maw(self):
        self.cur_paint_id = 3
        self.brush_id = 3

    def press_river_button_lake(self):
        self.cur_paint_id = 4
        self.brush_id = 3

    def press_river_button_swamp(self):
        self.cur_paint_id = 5
        self.brush_id = 3

    def press_primitive_button_none(self):
        self.cur_paint_id = 0
        self.brush_id = 4

    def press_primitive_button_prim(self):
        self.cur_paint_id = 1
        self.brush_id = 4

    def press_utility_button_only_sea(self):
        self.cur_paint_id = 0
        self.brush_id = 5

    def press_utility_button_cont_flatlands(self):
        self.cur_paint_id = 1
        self.brush_id = 5

