# from os import path, listdir, remove, rename
# import numpy as np
import json
import pickle
from config import * 

# t = r'C:\Users\apeir\Documents\code\dofus\map_info\test.json'

def write_json(new_data, filename,object_name):
    with open(filename,'w+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[object_name].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def json2pkl(json_file,output_pkl):
    # Load the JSON data
    with open(json_file, 'r') as jf:
        data = json.load(jf)

    # Check if the pkl file already exists
    try:
        with open(output_pkl, 'rb') as pf:
            existing_data = pickle.load(pf)
    except (FileNotFoundError, EOFError):
        existing_data = {}
    # Update the existing data with the new data
    existing_data.update(data)
    # Write the updated data to the pkl file
    with open(output_pkl, 'wb') as pf:
        pickle.dump(existing_data, pf)

def read_pkl(db):
  try:
    with open(db, 'rb') as pf:
      existing_data = pickle.load(pf)
  except (FileNotFoundError, EOFError):
      existing_data = {}
  return existing_data

def update_pkl(db, new_data):
    # Load existing data
    existing_data = read_pkl(db)
    # Update existing data with new data
    existing_data.update(new_data)
    # Write the updated data back to the pkl file
    with open(db, 'wb') as pf:
        pickle.dump(existing_data, pf)

# js= r'C:\Users\apeir\Documents\code\dofus\map_info\position.json'
# db=r'C:\Users\apeir\Documents\code\dofus\map_info\position.pkl'
# json2pkl(js,db)



# print(read_pkl(db)['1']['name'])