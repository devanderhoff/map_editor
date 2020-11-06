with open('./test.ybin', mode='rb') as file:
     region_info_lst = list(file.read())
     print(region_info_lst)

with open('./tiny_world.ybin', mode='rb') as file2:

    kaas2 = file2.read()
    print(kaas2)