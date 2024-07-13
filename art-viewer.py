
import os
import pathlib
import csv
import requests
import json

from api_classes.art_inst_chicago import ArtInstChicago
from api_classes.met_museum import MetMuseum

data_folder = "data"
brain_folder = os.path.join(data_folder, "brain")
apis_folder = os.path.join(brain_folder, "apis")
in_folder = os.path.join(data_folder, "in")
out_folder = os.path.join(data_folder, "out")

rest_apis = {}
rest_api_classes = {}

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

def output_json(folder_name, json_filename, json_data):
    if is_empty(json_data):
        return

    full_filename = os.path.join(folder_name, json_filename)
    with open(full_filename, 'w', encoding='utf-8') as file_out:
        json.dump(json_data, file_out, indent=4)

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

def assign_api_classes():
    global apis_folder

    for api_name, api_url in rest_apis.items():
        if api_name == "Art Institute of Chicago":
            this_api = ArtInstChicago(apis_folder, api_url)
            rest_api_classes[api_name] = this_api
        elif api_name == "The Metropolitan Museum of Art Collection":
            this_api = MetMuseum(apis_folder, api_url)
            rest_api_classes[api_name] = this_api

def load_api_classes():
    for rest_api_class in rest_api_classes:
        rest_api_classes[rest_api_class].load()

def main():
    load_config()
    add_rest_apis("rest_apis.csv")
    assign_api_classes()
    load_api_classes()

if __name__ == "__main__":
    main()