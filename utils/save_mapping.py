import json

MAPPING_DATA = "mapping_data.txt"


def save(data):
    with open(MAPPING_DATA, 'w') as outfile:
        json.dump(data, outfile)


def load():
    try:
        with open(MAPPING_DATA) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None
