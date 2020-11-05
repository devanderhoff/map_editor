from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
import numpy as np


# Image size is 300x225 pixels
class WorldmapSprites:
    def __init__(self):
        self.blank_canvas = np.ones((225, 300, 4))
        self.empty_array = np.zeros((225, 300, 4))
        self.empty = Image.fromarray(self.empty_array.astype(np.uint8))


        # Colours
        self.sea_colour_code = np.array([70, 119, 152, 255])
        self.cont_colour_code = np.array([120, 128, 58, 255])
        self.oceanic_colour_code = np.array([86, 153, 69, 255])
        self.medi_colour_code = np.array([182, 159, 97, 255])
        self.tropical_colour_code = np.array([122, 156, 35, 255])
        self.arid_colour_code = np.array([190, 149, 72, 255])
        self.desert_colour_code = np.array([187, 169, 132, 255])
        self.nordic_colour_code = np.array([120, 156, 101, 255])
        self.polar_colour_code = np.array([190, 190, 190, 255])

        self.sea_colour = self.sea_colour_code * self.blank_canvas
        self.cont_colour = self.cont_colour_code * self.blank_canvas
        self.oceanic_colour = self.oceanic_colour_code * self.blank_canvas
        self.medi_colour = self.medi_colour_code * self.blank_canvas
        self.tropical_colour = self.tropical_colour_code * self.blank_canvas
        self.arid_colour = self.arid_colour_code * self.blank_canvas
        self.desert_colour = self.desert_colour_code * self.blank_canvas
        self.nordic_colour = self.nordic_colour_code * self.blank_canvas
        self.polar_colour = self.polar_colour_code * self.blank_canvas

        self.BACKGROUND = (
        self.sea_colour, self.cont_colour, self.oceanic_colour, self.medi_colour, self.tropical_colour,
        self.arid_colour, self.desert_colour, self.nordic_colour, self.polar_colour, self.empty_array)

        # Crop values
        # self.crop = [(0,0,300,225), (300,0,600,225), (600,0,900,225)]

        "Load worldmap sprites"
        self.plains = Image.open("./worldmap/world_grassland.png")
        self.flat = self.plains
        self.rocky = Image.open("./worldmap/world_rocky.png")
        self.hills = Image.open("./worldmap/world_hills.png")
        self.mountains = Image.open("./worldmap/world_mountains.png")

        self.RELIEF = (self.plains, self.flat, self.rocky, self.hills, self.mountains, self.empty)

        "Vegatiation"
        self.grass = Image.open("./worldmap/world_grass_1.png")
        self.cont_forrest = Image.open("./worldmap/world_continental_forest.png")
        self.cont_trees = Image.open("./worldmap/world_continental_trees.png")
        self.oceanic_forrest = Image.open("./worldmap/world_oceanic_forest.png")
        self.oceanic_trees = Image.open("./worldmap/world_oceanic_trees.png")
        self.medi_forrest = Image.open('./worldmap/world_mediterran_forest.png')
        self.medi_trees = Image.open("./worldmap/world_mediterran_trees.png")
        self.tropical_forrest = Image.open("./worldmap/world_tropical_forest.png")
        self.tropical_trees = Image.open("./worldmap/world_tropical_trees.png")
        self.arid_forrest = Image.open("./worldmap/world_arid_forest.png")
        self.arid_trees = Image.open("./worldmap/world_arid_trees.png")
        self.nordic_forrest = Image.open("./worldmap/world_nordic_forest.png")
        self.nordic_trees = Image.open("./worldmap/world_nordic_trees.png")

        "water"
        self.lake = Image.open('./worldmap/world_lake.png')
        self.swamp = Image.open('./worldmap/world_swamp.png')

        "straight"
        self.river_horizontal = Image.open('./worldmap/postprocess/world_river_horizontal.png')
        self.river_vertical = Image.open('./worldmap/postprocess/world_river_vertical.png')
        "corners"
        self.river_bottom_left = Image.open('./worldmap/postprocess/world_river_leftbottom.png')
        self.river_bottom_right = Image.open('./worldmap/postprocess/world_river_rightbottom.png')
        self.river_top_left = Image.open('./worldmap/postprocess/world_river_leftTop.png')
        self.river_top_right = Image.open('./worldmap/postprocess/world_river_topright.png')
        "Crossings"
        self.river_crossing_left = Image.open('./worldmap/postprocess/world_river_crossing_left.png')
        self.river_crossing_top = Image.open('./worldmap/postprocess/world_river_crossing_up.png')
        self.river_crossing_right = Image.open('./worldmap/postprocess/world_river_crossing_right.png')
        self.river_crossing_bottom = Image.open('./worldmap/postprocess/world_river_crossing_bottom.png')
        "Mouths"
        self.river_mouth_left = Image.open('./worldmap/postprocess/world_river_mouth_west.png')
        self.river_mouth_top = Image.open('./worldmap/postprocess/world_river_mouth_north.png')
        self.river_mouth_right = Image.open('./worldmap/postprocess/world_river_mouth_east.png')
        self.river_mouth_bottom = Image.open('./worldmap/postprocess/world_river_mouth_south.png')
        "starts"
        self.river_start_left = Image.open('./worldmap/postprocess/world_river_start_left.png')
        self.river_start_top = Image.open('./worldmap/postprocess/world_river_start_up.png')
        self.river_start_right = Image.open('./worldmap/postprocess/world_river_start_right.png')
        self.river_start_bottom = Image.open('./worldmap/postprocess/world_river_start_bottom.png')
        self.crop_river = [(0, 0, self.river_start_left.size[0] / 3, self.river_start_left.size[1]),
                           (self.river_start_left.size[0] / 3, 0, 2 * self.river_start_left.size[0] / 3,
                            self.river_start_left.size[1]),
                           (2 * self.river_start_left.size[0] / 3, 0, 3 * self.river_start_left.size[0] / 3,
                            self.river_start_left.size[1])]
        # self.primitive = Image.open('./prim.png')

        # Coast
        self.coast_left = Image.open('./worldmap/postprocess/world_coast_left.png')
        self.coast_bottom = Image.open('./worldmap/postprocess/world_coast_bottom.png')
        self.coast_right = Image.open('./worldmap/postprocess/world_coast_right.png')
        self.coast_top = Image.open('./worldmap/postprocess/world_coast_top.png')

        self.coast_top_left = Image.open('./worldmap/postprocess/world_coast_topleft.png')
        self.coast_top_right = Image.open('./worldmap/postprocess/world_coast_topright.png')
        self.coast_bottom_right = Image.open('./worldmap/postprocess/world_coast_bottomright.png')
        self.coast_bottom_left = Image.open('./worldmap/postprocess/world_coast_bottomleft.png')

        self.coast_3top = Image.open('./worldmap/postprocess/world_coast_3top.png')
        self.coast_3right = Image.open('./worldmap/postprocess/world_coast_3right.png')
        self.coast_3bottom = Image.open('./worldmap/postprocess/world_coast_3bottom.png')
        self.coast_3left = Image.open('./worldmap/postprocess/world_coast_3left.png')

        self.coast4 = Image.open('./worldmap/postprocess/world_coast_4surround.png')

        self.coast_corner_bottom_left = Image.open('./worldmap/postprocess/world_coast_corner_bottomleft.png')
        self.coast_corner_bottom_right = Image.open('./worldmap/postprocess/world_coast_corner_bottomright.png')
        self.coast_corner_top_left = Image.open('./worldmap/postprocess/world_coast_corner_topleft.png')
        self.coast_corner_top_right = Image.open('./worldmap/postprocess/world_coast_corner_toprigh.png')

    def create_required_sprite(self, climate_id, relief_id, vegetation_id, water_id, world_object_id, coastal_adjacency,
                               river_adjacency, pixmap_flag=True, scale = 1):
        # Background first
        background, flagGround = self.select_background(climate_id)
        if climate_id != 0:
            relief, flagRelief = self.select_relief_sprite(relief_id)
        else:
            flagRelief = False
        grass, flagGrass = self.add_grass_sprite(climate_id, relief_id)
        vegatation, flagVeg = self.select_vegetation_sprite(vegetation_id, climate_id, relief_id)

        # prim, flagPrim = self.checkPrim(worldObjectID)
        if climate_id != 0:
            coast, flagCoast, secondCoast, secondFlagcoast = self.select_coast_sprite(coastal_adjacency)
            corner, flagCorner, secondCorner, secondFlagcorner = self.select_corner_sprite(coastal_adjacency)
        else:
            flagCoast = False
            flagCorner = False
            secondFlagcorner = False

        if water_id != 0:
            water, flagWater = self.select_water_sprite(water_id, river_adjacency, coastal_adjacency)
        else:
            flagWater = False

        if not flagGround:
            print('NO BACKGROUND FOUND')
        background_image = Image.fromarray(background.astype(np.uint8))
        if flagRelief:
            background_image.alpha_composite(relief)
        if flagGrass:
            background_image.alpha_composite(grass)
        if flagVeg:
            background_image.alpha_composite(vegatation)
        # if flagPrim:
        #     background_image.alpha_composite(prim)
        if flagCoast:
            background_image.alpha_composite(coast)
            if secondFlagcoast:
                background_image.alpha_composite(secondCoast)
        if flagCorner:
            background_image.alpha_composite(corner)
            if secondFlagcorner:
                background_image.alpha_composite(secondCorner)
        if flagWater:
            background_image.alpha_composite(water)

        background_image.thumbnail((background_image.size[0]*scale[0], background_image.size[1]*scale[1],), Image.ANTIALIAS)
        if pixmap_flag:
            background_image = ImageQt.ImageQt(background_image)
            background_image = QPixmap.fromImage(background_image)

        return background_image

    def select_background(self, climate_id):
        return self.BACKGROUND[climate_id], True

    def select_relief_sprite(self, relief_id):
        n = np.random.randint(0, 3)
        return self.RELIEF[relief_id].crop(self.create_crop(self.RELIEF[relief_id])[n]), True

    def select_vegetation_sprite(self, vegetation_id, climate_id, relief_id):
        n = np.random.randint(0, 3)
        flag_found = False
        vegetation_sprite = self.empty
        # if vegetationID == 0:
        #     vegetationSprite = self.empty
        treeChance = 6
        if climate_id == 1:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.cont_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.cont_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        elif climate_id == 2:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.oceanic_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.oceanic_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        elif climate_id == 3:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.medi_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.medi_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        elif climate_id == 4:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.tropical_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.tropical_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        elif climate_id == 5:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.arid_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.arid_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        elif climate_id == 7:
            if vegetation_id == 0 and (relief_id == 0 or relief_id == 1):
                i = np.random.randint(0, 10)
                if i >= treeChance:
                    vegetation_sprite = self.nordic_trees
                    vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                else:
                    vegetation_sprite = self.empty
                flag_found = True
            elif vegetation_id == 1:
                vegetation_sprite = self.nordic_forrest
                vegetation_sprite = vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
                flag_found = True
        return vegetation_sprite, flag_found

    def select_water_sprite(self, water_id, river_adjacency, coastal_adjacency):
        n = np.random.randint(0, 3)
        found_flag = False
        water_sprite = self.empty
        river_adjacency = np.asarray(river_adjacency)
        coastal_adjacency = np.asarray(coastal_adjacency)

        if water_id == 4:
            water_sprite = self.lake
            water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
            found_flag = True
        elif water_id == 5:
            water_sprite = self.swamp
            water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
            found_flag = True

        else:
            # First determine if it's a crossing
            nr_river = sum(river_adjacency[[0, 2, 4, 6]])
            nr_coast = sum(coastal_adjacency[[0, 2, 4, 6]])
            # Detect when a crossing should be used. 2 cases
            # first case, 3 adjacent rivers.
            # 2nd case, 2 adjecent rivers, and a coast.
            crossing = nr_river >= 3 or (nr_coast == 1 and nr_river == 2)

            # Check for coastal rivers, either solo, or should be next to coast.
            solo_river = (nr_river == 0 and nr_coast == 1)
            next_to_coast = nr_coast >= 1

            # River starts only have 1 river next to them, and never a coast.
            river_start = (nr_river == 1 and nr_coast == 0)

            # First put in river mouths.
            # cases;
            # Mouth has to be nextToCoast. Then it can be normal mouth, or river crossing, or soloRiver.
            if next_to_coast:
                if solo_river:
                    if coastal_adjacency[0] == 1:
                        water_sprite = self.river_start_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[2] == 1:
                        water_sprite = self.river_start_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[4] == 1:
                        water_sprite = self.river_start_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[6] == 1:
                        water_sprite = self.river_start_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                elif crossing:
                    adjacencySum = coastal_adjacency + river_adjacency
                    if adjacencySum[0] >= 1 and adjacencySum[2] >= 1 and adjacencySum[4] >= 1:
                        water_sprite = self.river_crossing_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[2] >= 1 and adjacencySum[4] >= 1 and adjacencySum[6] >= 1:
                        water_sprite = self.river_crossing_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[4] >= 1 and adjacencySum[6] >= 1 and adjacencySum[0] >= 1:
                        water_sprite = self.river_crossing_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[6] >= 1 and adjacencySum[0] >= 1 and adjacencySum[2] >= 1:
                        water_sprite = self.river_crossing_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                else:
                    if coastal_adjacency[0] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.river_mouth_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[2] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.river_mouth_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[4] == 1 and river_adjacency[0] == 1:
                        water_sprite = self.river_mouth_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[6] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.river_mouth_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[0] == 1 and river_adjacency[2] == 1) or (
                            coastal_adjacency[2] == 1 and river_adjacency[0] == 1):
                        water_sprite = self.river_top_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[0] == 1 and river_adjacency[6] == 1) or (
                            coastal_adjacency[6] == 1 and river_adjacency[0] == 1):
                        water_sprite = self.river_top_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[2] == 1 and river_adjacency[4] == 1) or (
                            coastal_adjacency[4] == 1 and river_adjacency[2] == 1):
                        water_sprite = self.river_bottom_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[4] == 1 and river_adjacency[6] == 1) or (
                            coastal_adjacency[6] == 1 and river_adjacency[4] == 1):
                        water_sprite = self.river_bottom_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
            elif river_start:
                if river_adjacency[0] == 1:
                    water_sprite = self.river_start_top
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[2] == 1:
                    water_sprite = self.river_start_left
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[4] == 1:
                    water_sprite = self.river_start_bottom
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[6] == 1:
                    water_sprite = self.river_start_right
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
            elif not next_to_coast:
                if not crossing:
                    if river_adjacency[0] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.river_vertical
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[2] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.river_horizontal
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[0] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.river_top_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[0] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.river_top_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.river_bottom_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.river_bottom_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                if crossing:
                    if river_adjacency[0] == 1 and river_adjacency[2] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.river_crossing_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[2] == 1 and river_adjacency[4] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.river_crossing_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[6] == 1 and river_adjacency[0] == 1:
                        water_sprite = self.river_crossing_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[6] == 1 and river_adjacency[0] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.river_crossing_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True

        return water_sprite, found_flag

    def add_grass_sprite(self, climate_id, relief_id):
        n = np.random.randint(0, 3)
        grass_sprite = self.empty
        grass_flag = False
        if climate_id != 0 and climate_id != 6 and climate_id != 8 and climate_id != -1 and relief_id != 4:
            grass_sprite = self.grass
            grass_sprite = grass_sprite.crop(self.create_crop(grass_sprite)[n])
            if climate_id == 1:
                colour = self.cont_colour_code / 255
            elif climate_id == 2:
                colour = self.oceanic_colour_code / 255
            elif climate_id == 3:
                colour = self.medi_colour_code / 255
            elif climate_id == 4:
                colour = self.tropical_colour_code / 255
            elif climate_id == 5:
                colour = self.arid_colour_code / 255
            elif climate_id == 7:
                colour = (self.nordic_colour_code / 255)
            else:
                print('Unknown climate, DEBUG')
                colour = np.array([1, 1, 1, 1])

            grass_sprite = np.array(grass_sprite) * colour
            grass_sprite = Image.fromarray(grass_sprite.astype(np.uint8))
            grass_flag = True

        return grass_sprite, grass_flag

    def checkPrim(self, worldObjectID):
        primFlag = False
        primSprite = self.empty
        if worldObjectID == 1:
            primFlag = True
            primSprite = self.primitive
        return primSprite, primFlag

    def select_coast_sprite(self, coastal_adjacency):
        #     topID = n - self.xWidth
        #     topLeftID = n - self.xWidth - 1
        #     leftID = n - 1
        #     bottomLeftID = n + self.xWidth - 1
        #     bottomID = n + self.xWidth
        #     bottomRightID = n + self.xWidth + 1
        #     rightID = n + 1
        #     topRightID = n - self.xWidth + 1
        coast_id = [0, 2, 4, 6]
        n = np.random.randint(0, 3)
        coast_sprite = self.empty
        coast_flag = False
        second_coast_sprite = self.empty
        second_coast_flag = False

        coastal_adjacency = np.asarray(coastal_adjacency)
        if sum(coastal_adjacency[coast_id]) == 1:
            if coastal_adjacency[0] == 1:
                coast_sprite = self.coast_top
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[2] == 1:
                coast_sprite = self.coast_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[4] == 1:
                coast_sprite = self.coast_bottom
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[6] == 1:
                coast_sprite = self.coast_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
        if sum(coastal_adjacency[coast_id]) == 2:
            if coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1:
                coast_sprite = self.coast_top_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.coast_bottom_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.coast_bottom_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[0] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.coast_top_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[0] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.coast_top
                second_coast_sprite = self.coast_bottom
                coast_flag = True
                second_coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.coast_left
                second_coast_sprite = self.coast_right
                coast_flag = True
                second_coast_flag = True

        if sum(coastal_adjacency[coast_id]) == 3:
            if coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.coast_3left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.coast_3bottom
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1 and coastal_adjacency[0] == 1:
                coast_sprite = self.coast_3right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[6] == 1 and coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1:
                coast_sprite = self.coast_3top
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

        if sum(coastal_adjacency[coast_id]) == 4:
            coast_sprite = self.coast4
            coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
            coast_flag = True

        return coast_sprite, coast_flag, second_coast_sprite, second_coast_flag

    def select_corner_sprite(self, coastal_adjacency):
        # bottomleft, bottomright, topright, topleft
        corner_sprite = self.empty
        corner_flag = False
        corner_sprite_secondary = self.empty
        corner_flag_secondary = False
        coastal_adjacency = np.asarray(coastal_adjacency)

        if (coastal_adjacency[0] == 0) and (coastal_adjacency[1] == 1) and (coastal_adjacency[2] == 0):
            corner_sprite = self.coast_corner_top_left
            corner_flag = True

        if coastal_adjacency[2] == 0 and coastal_adjacency[3] == 1 and coastal_adjacency[4] == 0:
            if corner_flag:
                corner_sprite_secondary = self.coast_corner_bottom_left
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.coast_corner_bottom_left
            corner_flag = True

        if coastal_adjacency[4] == 0 and coastal_adjacency[5] == 1 and coastal_adjacency[6] == 0:
            if corner_flag:
                corner_sprite_secondary = self.coast_corner_bottom_right
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.coast_corner_bottom_right
            corner_flag = True

        if coastal_adjacency[6] == 0 and coastal_adjacency[7] == 1 and coastal_adjacency[0] == 0:
            if corner_flag:
                corner_sprite_secondary = self.coast_corner_top_right
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.coast_corner_top_right
            corner_flag = True

        return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary

    def create_crop(self, image):
        return [(0, 0, image.size[0] / 3, image.size[1]), (image.size[0] / 3, 0, 2 * image.size[0] / 3, image.size[1]),
                    (2 * image.size[0] / 3, 0, 3 * image.size[0] / 3, image.size[1])]
