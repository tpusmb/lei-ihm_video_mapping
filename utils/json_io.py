import io
import json


def save(data, file_name):
    """
    Save a dic to json file
    :param data: (dic) dictionary to save in json file
    :param file_name: (string) path to file
    """
    with io.open(file_name, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=True)


def load(file_name):
    """
    Read a json file
    :param file_name: (string)  path to file
    :return: (dic) dictionary read into the file
    """
    try:
        with io.open(file_name, encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None
