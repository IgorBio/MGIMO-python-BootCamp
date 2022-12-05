import json


def open_file(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    return data


def convert_to_str(data_file):
    return "".join(data_file)


def some_logic(file_path):
    temp = open_file(file_path)
    output = convert_to_str(temp)
    return output
