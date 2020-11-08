class SignalSlot:
    ## CLIMATE BUTTONS ##
    def press_climate_button_sea(self):
        self.paint_id = 0
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_cont(self):
        self.paint_id = 1
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_oceanic(self):
        self.paint_id = 2
        self.brush_id = 0
        # return paint_climate

    def press_climate_button_medi(self):
        self.paint_id = 3
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_tropical(self):
        self.paint_id = 4
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_arid(self):
        self.paint_id = 5
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_desert(self):
        self.paint_id = 6
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_nordic(self):
        self.paint_id = 7
        self.brush_id = 0
        # return self.paint_climate
        #

    def press_climate_button_polar(self):
        self.paint_id = 8
        self.brush_id = 0
        # return self.paint_climate

    ## RELIEF BUTTONS ##
    def press_relief_button_none(self):
        self.paint_id = 0
        self.brush_id = 1

    def press_relief_button_plains(self):
        self.paint_id = 1
        self.brush_id = 1

    def press_relief_button_rocky(self):
        self.paint_id = 2
        self.brush_id = 1

    def press_relief_button_hills(self):
        self.paint_id = 3
        self.brush_id = 1

    def press_relief_button_mountains(self):
        self.paint_id = 4
        self.brush_id = 1

    ## Vegetation buttons
    def press_vegetation_button_none(self):
        self.paint_id = 0
        self.brush_id = 2

    def press_vegetation_button_forrest(self):
        self.paint_id = 1
        self.brush_id = 2

    ## River buttons
    def press_river_button_none(self):
        self.paint_id = 0
        self.brush_id = 3

    def press_river_button_estuary(self):
        self.paint_id = 1
        self.brush_id = 3

    def press_river_button_river(self):
        self.paint_id = 2
        self.brush_id = 3

    def press_river_button_maw(self):
        self.paint_id = 3
        self.brush_id = 3

    def press_river_button_lake(self):
        self.paint_id = 4
        self.brush_id = 3

    def press_river_button_swamp(self):
        self.paint_id = 5
        self.brush_id = 3

    def press_primitive_button_none(self):
        self.paint_id = 0
        self.brush_id = 4

    def press_primitive_button_prim(self):
        self.paint_id = 1
        self.brush_id = 4

