import json

def write_data(file_path, data):
    with open(file_path, 'w') as file:  
        json.dump(data, file, indent=4)
