
from os import path, listdir, walk
from config import * 
from Pictures import *
from json_utility import *

def scan_pictures(root_folder, screen_type):    
    new_pictures = {}
    screen_type_folder = path.join(root_folder, screen_type)
    for category in listdir(screen_type_folder):
        category_folder = path.join(screen_type_folder,category)
        if path.isdir(category_folder):
                for file in listdir(category_folder):
                    if file.lower().endswith((".jpeg",".jpg",".png")):
                        if not category in new_pictures.keys():
                            new_pictures[category] = {}
                        picture = Picture(path.join(category_folder, file), file.split(".")[0], screen_type, category)                        
                        print(picture.hash)
                        new_pictures[category][picture.name] = picture  
    return new_pictures
    


def make_dict_from_photo_folder(db_file, picture_folder):
    pictures = {}
    for screen_type in listdir(picture_folder):
        if path.isdir(path.join(picture_folder, screen_type)):
            pictures[screen_type] = scan_pictures(picture_folder,screen_type)

    update_pkl(db_file, pictures)

def get_info_from_pictures_db(file):
    return read_pkl(file)

make_dict_from_photo_folder(files['pictures_db'], directories["photo"])

print(get_info_from_pictures_db(files["pictures_db"]))
# t = get_info_from_pictures_db(files["pictures_db"])
# print(t["screen_type"]["bois"]["inventaire_plein"])