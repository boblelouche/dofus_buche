import utility
# from json_utility import update_pkl , read_pkl


class Picture:
    def __init__(self, path, name, screen_type, category):
        self.path = path
        self.screen_type = screen_type
        self.category = category
        self.name = name
        self.hash = utility.make_image_hash(self.path)

    def __repr__(self):
        cls = self.__class__
        return f"<{cls.__module__}.{cls.__qualname__} object with hash {self.hash}>"

    def __str__(self):
        return str(self.hash)
