
import os
import requests
import json
import csv
import pathlib

data_folder = "data"
brain_folder = os.path.join(data_folder, "brain")
apis_folder = os.path.join(brain_folder, "apis")
in_folder = os.path.join(data_folder, "in")
out_folder = os.path.join(data_folder, "out")

rest_apis = {}

def is_empty(variable):
    if variable is None:
        return True

    if isinstance(variable, str) and variable == "":
        return True

    if isinstance(variable, list) and len(variable) <= 0:
        return True

    if isinstance(variable, dict) and len(variable.keys()) <= 0:
        return True

    return False

def file_exists(folder_name, json_filename):
    filename_full_path = os.path.join(folder_name, json_filename)
    file_path = pathlib.Path(filename_full_path)

    return file_path.is_file()

def load_json(folder_name, json_filename):
    full_filename = os.path.join(folder_name, json_filename)
    with open(full_filename, 'w', encoding='utf-8') as file_in:
        json_data = json.load(file_in)

    if is_empty(json_data):
        return {}

    return json_data

def output_text(folder_name, filename, text_data):
    if is_empty(text_data):
        return

    full_filename = os.path.join(folder_name, filename)
    with open(full_filename, 'w', encoding='utf-8') as file_out:
        file_out.write(text_data)

def output_json(folder_name, json_filename, json_data):
    if is_empty(json_data):
        return

    full_filename = os.path.join(folder_name, json_filename)
    with open(full_filename, 'w', encoding='utf-8') as file_out:
        json.dump(json_data, file_out, ensure_ascii=False, indent=4)

def load_config():
    global brain_folder
    global rest_apis

    full_filename = os.path.join(brain_folder, "rest_apis.json")
    file_path = pathlib.Path(full_filename)
    if file_path.is_file():
        with open(full_filename, 'r', encoding='utf-8') as file_in:
            rest_apis = json.load(file_in)

def save_config():
    global brain_folder
    global rest_apis

    output_json(brain_folder, "rest_apis.json", rest_apis)

def machine_readable(human_readable_string):
    return_string = human_readable_string.replace("https://", "")
    return_string = return_string.replace(":", "_")
    return_string = return_string.replace(".", "_")
    return_string = return_string.replace("/", "_")
    return_string = return_string.replace("\\t", "_")
    return_string = return_string.replace(" ", "_")
    return_string = return_string.replace("__", "_")
    return_string = return_string.replace("__", "_")
    return_string = return_string.replace("__", "_")

    return return_string

def csv_to_list_of_dictionaries(in_folder, in_file):
    list_of_dictionaries = []

    with open(os.path.join(in_folder, in_file), newline='') as in_file_csv:
        reader = csv.DictReader(in_file_csv)
        for row in reader:
            list_of_dictionaries.append(row)

    return list_of_dictionaries

def add_rest_apis(in_file):
    global in_folder
    global rest_apis

    list_of_art_apis = csv_to_list_of_dictionaries(in_folder, in_file)
    for record in list_of_art_apis:
        index = record["api_name"]
        if index not in rest_apis.keys():
            rest_apis[index] = record["api_url"]

    save_config()

def get_info_on_rest_apis():
    global out_folder

    for key, value in rest_apis.items():
        url = value
        index = machine_readable(url) + ".json"
        if not file_exists(apis_folder, index):
            json_data = get_info_on_rest_api(url)
            output_json(apis_folder, index, json_data)

def get_info_on_rest_api(url):
    response = requests.get(url)

    print(url)
    print(response.status_code)

    return response.json()

def main():
    load_config()
    add_rest_apis("rest_apis.csv")
    get_info_on_rest_apis()

if __name__ == "__main__":
    main()