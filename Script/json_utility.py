import json
import pickle
from mergedeep import merge


def write_json(new_data, filename, object_name):
    file = open(filename, "w+")
    # First we load existing data into a dict.
    file_data = json.load(file)
    # Join new_data with file_data inside emp_details
    file_data[object_name].append(new_data)
    # Sets file's current position at offset.
    file.seek(0)
    # convert back to json.
    json.dump(file_data, file, indent=4)
    file.close()


def json2pkl(json_file, output_pkl):
    # Load the JSON data
    jso = open(json_file, "r")
    data = json.load(jso)

    # Check if the pkl file already exists
    dbo = open(output_pkl, "rb")
    try:
        existing_data = pickle.load(dbo)
    except (FileNotFoundError, EOFError):
        existing_data = {}
    finally:
        dbo.close()
    # Update the existing data with the new data
    existing_data.update(data)

    # Write the updated data to the pkl file
    dbw = open(output_pkl, "wb")
    pickle.dump(existing_data, dbw)
    dbw.close()


def read_pkl(db):
    dbo = open(db, "rb")
    try:
        existing_data = pickle.load(dbo)
    except (FileNotFoundError, EOFError):
        existing_data = {}
    finally:
        dbo.close()
    return existing_data


def update_pkl(db, data):
    # Load existing data
    existing_data = read_pkl(db)
    # Update existing data with new data
    new_data = merge(existing_data, data)
    # Write the updated data back to the pkl file

    dbo = open(db, "wb")
    pickle.dump(new_data, dbo)
    dbo.close()


# js= r'C:\Users\apeir\Documents\code\dofus\map_info\position.json'
# db=r'C:\Users\apeir\Documents\code\dofus\map_info\position.pkl'
# json2pkl(js,db)
