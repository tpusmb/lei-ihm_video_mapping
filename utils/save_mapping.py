import json


def save(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def load():
    try:
        with open('data.txt') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None
