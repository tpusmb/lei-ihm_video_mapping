import io
import json


def save(data, file_name):
    with io.open(file_name, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=True)


def load(file_name):
    try:
        with io.open(file_name, encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None
