#
# import random
# random.seed()
#
# tile_name = ["fer3", "fer4", "fer2", "clay", "sand", "vgra", "sili", "basa", "gran", "lime", "ssto", "schi", "marb", "grav",
#              "sgra", "COPP", "IRON", "SILV", "GOLD", "COAL", "TINN", "silt", "ASHE", "CHAR", "OBSI", "SHEL", "26",
#              "27", "28", "29", "30", "31", "32", "33", "34", "35"]
# # vgra is very gravelly vs grav which is regular fert 1 gravel. sgra is sandy gravel
# from utils.log import get_logger
#
# logger = get_logger(__name__)
#
#
# def map_output(filename):
#     f = open(filename, "rb")
#
#     # total groups counter
#     g_count = 0
#
#     while g_count < 39200 and False:
#         tile_type = tile_name[int.from_bytes(f.read(1), "big")]
#         tile_height = int.from_bytes(f.read(1), "big")  # 0 = 50
#         tile_object = int.from_bytes(f.read(1), "big")
#         logger.debug('map_output -> tile_type = %s', tile_type)
#         logger.debug('map_output -> tile_object = %s', tile_object)
#         #print('tile_type, end=" ")
#         #print(tile_object, end=" | ")
#         g_count = g_count + 1
#         if g_count % 140 == 0:
#             print("")
#
#     for y in range(280):
#         for x in range(140):
#             tile_type = tile_name[int.from_bytes(f.read(1), "big")]
#             tile_height = int.from_bytes(f.read(1), "big")  # 0 = 50
#             tile_object = int.from_bytes(f.read(1), "big")
#             print(tile_type, end=" ")
#             # print(tile_object, end=" | ")
#             g_count = g_count + 1
#             if g_count % 140 == 0:
#                 print("")
#     # final bytes list resources in tile. I'm not sure what there affect.
#     map_byte = f.read(1)
#     while map_byte:
#         print(int.from_bytes(map_byte, "big"), end=" ")
#         map_byte = f.read(1)
#     f.close()
#
# def map_input(filename):
#     f = open(filename, "r+b")
#     group = [chr(21), chr(55), chr(0)]
#     g_count = 0
#
#     while g_count < 39200:
# 		f.write(chr(21).encode()
# 		f.write(chr(50).encode()
# 		f.write(chr(0).encode()
#         g_count = g_count + 1
#     f.close()
#
# def map_edit(filename):
#     f = open(filename, "r+b")
#     row_list = []  # each 140 tile row
#     g_count = 0
#     resource_list = []
#
#     # read in the base
#     for y in range(280):
#         row = []
#         for x in range(140):
#             tile_type = int.from_bytes(f.read(1), "big")
#             tile_height = int.from_bytes(f.read(1), "big")  # 0 = 50
#             tile_object = int.from_bytes(f.read(1), "big")
#             row.append([tile_type, tile_height, tile_object])
#             g_count = g_count + 1
#         row_list.append(row)
#     map_byte = f.read(1)
#     while map_byte:
#         resource_list.append(int.from_bytes(map_byte, "big"))
#         map_byte = f.read(1)
#     print(resource_list)
#
#     for y in range(280):
#         for x in range(140):
#
#             if (y < 20) and False:
#                 if x < 10:
#                     row_list[y][x][0] = 24
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 34
#                 elif x < 20:
#                     row_list[y][x][0] = 15
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 38
#                 elif x < 30:
#                     row_list[y][x][0] = 16
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 71
#                 elif x < 40:
#                     row_list[y][x][0] = 20
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 69
#                 elif x < 50:
#                     row_list[y][x][0] = 17
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 0
#                 elif x < 60:
#                     row_list[y][x][0] = 18
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 0
#                 elif x < 70:
#                     row_list[y][x][0] = 19
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 0
#                 elif x < 90:
#                     row_list[y][x][0] = 3
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 28
#                 else:
#                     row_list[y][x][0] = 21
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 29
#
#             if (20 <= y < 40) and False:
#                 if x < 20:
#                     row_list[y][x][0] = 3
#                     row_list[y][x][1] = 50
#                 elif x < 60:
#                     row_list[y][x][0] = 21
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 42
#                 else:
#                     row_list[y][x][0] = 21
#                     row_list[y][x][1] = 50
#                     row_list[y][x][2] = 14
#
#             if (40 <= y < 60) and False:
#                 row_list[y][x][0] = 21
#                 row_list[y][x][1] = 50
#
#             # all dirt to silt
#             if row_list[y][x][0] < 3 or True:
#                 row_list[y][x][0] = 21
#
#             if row_list[y][x][2] == 51:
#                 row_list[y][x][2] = 0
#
#             if row_list[y][x][1] > 50:
#                 row_list[y][x][1] = 50
#
#         row_list[279][6][2] = 52
#
#         add_water = True
#         add_pearl = False
#
#         if add_water:
#             # add water_id to the bottom left corner
#             row_list[279][0][1] = 48
#             row_list[279][1][1] = 48
#             row_list[279][2][1] = 48
#
#             row_list[278][0][1] = 48
#             row_list[278][1][1] = 48
#             row_list[277][0][1] = 48
#             row_list[277][1][1] = 48
#
#             row_list[276][0][1] = 48
#             row_list[275][0][1] = 48
#
#             row_list[279][0][2] = 2  # water_id in the corner
#             row_list[278][0][2] = 51
#             row_list[279][1][2] = 51
#             row_list[277][0][2] = 51
#
#         if add_pearl:
#             # add water_id to the bottom right corner
#             row_list[279][139][1] = 48
#             row_list[279][139][2] = 2  # water_id in the corner
#
#             row_list[279][138][1] = 48
#             row_list[279][138][2] = 108
#             row_list[279][137][1] = 48
#             row_list[279][137][2] = 108
#
#             row_list[278][139][1] = 48
#             row_list[278][138][1] = 48
#             row_list[278][137][1] = 48
#
#             row_list[278][139][2] = 108
#             row_list[278][138][2] = 108
#             row_list[278][137][2] = 108
#
#             row_list[277][139][1] = 48
#             row_list[277][138][1] = 48
#             row_list[276][139][1] = 48
#             row_list[276][138][1] = 48
#
#             row_list[275][139][1] = 48
#             row_list[274][139][1] = 48
#
#             row_list[277][139][2] = 108
#             row_list[277][138][2] = 108
#             row_list[276][139][2] = 108
#             row_list[276][138][2] = 108
#
#             row_list[275][139][2] = 108
#             row_list[274][139][2] = 108
#
#     f.seek(0, 0)  # return to start
#     for y in range(280):
#         for x in range(140):
#             tile_type = row_list[y][x][0]
#             tile_height = row_list[y][x][1]  # 0 = 50
#             tile_object = row_list[y][x][2]
#             f.write(chr(tile_type).encode())
#             f.write(chr(tile_height).encode())
#             f.write(chr(tile_object).encode())
#
#     # f.seek(-1, 1)
#     # resource_list = [132, 30, 18, 54, 55, 56, 57, 58, 59, 87]
#     for item in resource_list:
#         print(item)
#         f.write(chr(item).encode())
#
#     print(g_count)
#     f.close()
#     # f = open(filename, "ab")
#     # f.write(chr(59).encode())
#     # f.write(chr(54).encode())
#     # f.close()
#
#
# # map_input("65_32.zon")
# # map_edit("43_14.zon")
# # map_output("43_14.zon")
#
#
