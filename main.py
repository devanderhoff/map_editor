import binascii
from PIL import Image
import numpy as np

from region import Region
from world import World
from image import WorldmapSprites

filename = "worldzal.ybin"

# test = Region(1,1,'test')

blank_world = World()
blank_world.create_new_world(5,5)
blank_world.create_world_image()
blank_world.worldmap_image.show()

# worldmap = World()
# worldmap.load_world('./tiny_world.ybin')
# # worldmap.create_world_image()
# # worldmap.worldmap_image.show()



# Spritegen = WorldmapSprites()
# test, _ = Spritegen.select_relief_sprite(1)
# test.show()
# print('penis')
# worldmap = World(filename)
# SpriteGen = WorldmapSprites()
# # worldmap.generateCoastal()
# # worldmap.generateRiver()
# print('worldmap')
#
# imsave = []
# i = 0
# for region in worldmap.regions:
#     # print(i)
#     i += 1
#     # if i == 2610:
#         # print('penis')
#
#
#     temp_sprite = SpriteGen.create_required_sprite(region.climate_id, region.relief_id, region.vegetation_id, region.water_id, region.world_object_id, region.coastal_adjacency, region.river_adjacency)
#     imsave.append(temp_sprite)
#
# width = 300
# height = 225
# total_width = width * worldmap.x_width
# total_height = height * worldmap.y_height
#
# saveFlag = False
# tempconcat = []
# for n, sprite in enumerate(imsave):
#     if n % worldmap.x_width == 0:
#         if saveFlag:
#             tempconcat.append(temp_im)
#         temp_im = Image.new("RGB", (total_width, height))
#         new_pos = 0
#         saveFlag = True
#     temp_im.paste(sprite, (new_pos, 0))
#     new_pos += sprite.size[0]
#
# Image.MAX_IMAGE_PIXELS = None
# final_img = Image.new("RGB", (total_width, total_height))
# new_pos = 0
# for sprite in tempconcat:
#     final_img.paste(sprite, (0, new_pos))
#     new_pos += sprite.size[1]
# x_half = final_img.size[0]*0.5
# x_full = final_img.size[0]
# print(final_img.size[0])
# final_img.thumbnail((final_img.size[0]*0.3, final_img.size[1]*0.3), Image.ANTIALIAS)
# final_img.save('full_worldmap.jpeg')
#
# final_img_crop = final_img.crop((x_half, 0, x_full, final_img.size[1]))
# final_img_crop.save("current_world.jpeg", "JPEG", quality=10)
# final_img_crop.thumbnail((final_img.size[0]*0.5, final_img.size[1]*0.5), Image.ANTIALIAS)
# final_img_crop.save("current_world_smaller.jpeg")
#
#
# print('penis')
# # # testimage = Spritetest.CreateRequiredSprite(worldmap.regions[n].climateID, worldmap.regions[n].reliefID, worldmap.regions[n].vegetationID, worldmap.regions[n].waterID)
# # #
# # # testimage.show()
# #
# # seaColour = np.array([0,0,128])
# # contColour = np.array([0, 182, 36])
# # oceaColour = np.array([0, 144, 115])
# # mediColour = np.array([219, 153, 0])
# # tropColour = np.array([0,255,0])
# # aridColour = np.array([255,255,0])
# # desertColour = np.array([220,255,0])
# # nordicColour = np.array([0,124,149])
# # polarColour = np.array([255,255,255])
#
# # imagetest = np.zeros((worldmap.yHeight, worldmap.xWidth, 3))
# #
# # for regions in worldmap.regions:
# #     if regions.climateID == 0:
# #         imagetest[regions.y, regions.x] = seaColour
# #     elif regions.climateID == 1:
# #         imagetest[regions.y, regions.x] = contColour
# #     elif regions.climateID == 2:
# #         imagetest[regions.y, regions.x] = oceaColour
# #     elif regions.climateID == 3:
# #         imagetest[regions.y, regions.x] = mediColour
# #     elif regions.climateID == 4:
#         imagetest[regions.y, regions.x] = tropColour
#     elif regions.climateID == 5:
#         imagetest[regions.y, regions.x] = aridColour
#     elif regions.climateID == 6:
#         imagetest[regions.y, regions.x] = desertColour
#     elif regions.climateID == 7:
#         imagetest[regions.y, regions.x] = nordicColour
#     elif regions.climateID == 8:
#         imagetest[regions.y, regions.x] = polarColour
#
# testtest = Image.fromarray(imagetest.astype(np.uint8))
# testtest.show()
#
