import json
import io
MAPPING_DATA = "mapping_data.json"


def save(data):
    with io.open(MAPPING_DATA, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=True)


def load():
    try:
        with io.open(MAPPING_DATA, encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None
