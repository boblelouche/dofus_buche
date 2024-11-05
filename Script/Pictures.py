from os import path
from utility import  make_image_hash
from json_utility import update_pkl , read_pkl

class Picture:
    # def __init__(self, name, categorie, path, hash):
    def __init__(self, path, name,screen_type, category ):
        self.path = path
        self.screen_type = screen_type
        self.category = category
        self.name = name
        self.hash = make_image_hash(self.path)
        # self.__get_info()
    def __repr__(self):
        # return "Picture()"
        cls = self.__class__
        return  f"<{cls.__module__}.{cls.__qualname__} object with hash {self.hash}>"
    def __str__(self):
        cls = self.__class__
        return  f"<{cls.__module__}.{cls.__qualname__} object with hash {self.hash}>"
        # return str(self.hash)

    # def __get_info(self):
