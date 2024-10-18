# from utility import *
from math import sqrt
from Personage import *
# get_screenshot_region()
# print(detect_click_left())
# print(get_pixel_color())
# save_road('buche_bonta')
# follow_saved_road(Personage.Taz,'key_masters')
print(get_pixel_color_on_click())
# print(find_actual_map("Ironamo"))
# print('ok')
# def click_on_picture(picture,zone=(0,0,1920,1080)):
# def get_map_info(Perso):
# get_map_name_picture()
# Iro = Player("Ironamo", 8, 3, "test", 86, [-26,21], "enutrof", ["bucheron" ,"mineur"])
# direction_dict = {
#             "u": (1, -1),
#             "d": (1, 1),
#             "r": (0, 1),
#             "l": (0, -1)
#         }
# for direction in direction_dict.keys():

#     index, value = direction_dict[direction]
#     Iro.position[index] = int(Iro.position[index]) + value
#     # Iro.position[index] = f'{str(int(Iro.position[index]) + value)}'.replace("'","\"")
#     print(Iro.position, direction)
# print(confirme_changement_map())

def calcule_distance(A,B):
    return int(sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2))


def remove_closest_point():

# # Handle JSON file reading and writing
    try:
        with open(files["map_position"], 'r+') as file:
            if path.getsize(files["map_position"]) > 0:
                file_data = json.load(file)
            else:
                file_data = {}
    except json.JSONDecodeError:
        file_data = {}
    keys = list(file_data.keys())
    for key in keys:
        ressource_types = list(file_data[key]["ressource"].keys())
        if len(ressource_types)!=0:
            for ressource_type in ressource_types:
                checked = []
                temp=file_data[key]["ressource"][ressource_type]
                # print(file_data[key]["ressource"][ressource_type])
                for Point in temp:
                    checked.append(Point)
                    temp.remove(Point)                
                    for Second_point in temp:
                        if calcule_distance(Point, Second_point)<2000:
                            file_data[key]["ressource"][ressource_type].remove(Second_point)
    file_data.update()
    with open(files["map_position"], 'w+') as file:
        json.dump(file_data, file, indent=4)               

def calculate_path(actual_position, destination):
    distance_x =  sqrt((destination[0]-actual_position[0])**2)
    distance_y =  sqrt((destination[1]-actual_position[1])**2)
    if destination[0]<actual_position[0]:
        distance_x*=-1
    if destination[1]>actual_position[1]:
        distance_y*=-1
    return (distance_x,distance_y)

# calculate_path([-1,1],[2,2])

# remove_closest_point()
# for key in keys:


#             if 'image_hash' in file_data[key]:
#                 stored_hash = hex_to_hash(file_data[key]['image_hash'])  # Convert the string back to an imagehash object
#                 if stored_hash == actual_hash:  # Now this comparison should work
#                     print(f"Image hash found in key: {key}")
#                     return key
#         new_key = str(len(keys)+1)
#         map_changer = find_map_changer()
#         # print(map_changer)
#         t = { new_key: {
#             # "position" :["x","y"],
#             "position" :actual_position,
#             "name":"",
#             "picture_path": path.join(map_name_picture_folder,f'{new_key}.png'),
#             "image_hash":f'{actual_hash}',
#             "map_changer": map_changer,
#             "ressource": {}}}    
#         file_data.update(t)
#         with open(files["map_position"], 'w+') as file:
#             json.dump(file_data, file, indent=4)
