# from os import path, listdir, remove, rename
# import numpy as np
import json

# t = r'C:\Users\apeir\Documents\code\dofus\map_info\test.json'

def write_json(new_data, filename,object_name):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[object_name].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
