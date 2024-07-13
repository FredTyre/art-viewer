import os
import pathlib
import json
import requests

class RestAPI:
    apis_folder = ""
    api_url = ""

    def __init__(self, apis_folder, api_url):
        self.apis_folder = apis_folder
        self.api_url = api_url

    def is_empty(self, variable):
        if variable is None:
            return True

        if isinstance(variable, str) and variable == "":
            return True

        if isinstance(variable, list) and len(variable) <= 0:
            return True

        if isinstance(variable, dict) and len(variable.keys()) <= 0:
            return True

        return False

    def file_exists(self, folder_name, json_filename):
        filename_full_path = os.path.join(folder_name, json_filename)
        file_path = pathlib.Path(filename_full_path)

        return file_path.is_file()

    def machine_readable(self, human_readable_string):
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

    def output_text(self, folder_name, filename, text_data):
        if self.is_empty(text_data):
            return

        full_filename = os.path.join(folder_name, filename)
        with open(full_filename, 'w', encoding='utf-8') as file_out:
            file_out.write(text_data)

    def output_json(self, folder_name, json_filename, json_data):
        if self.is_empty(json_data):
            return

        full_filename = os.path.join(folder_name, json_filename)
        with open(full_filename, 'w', encoding='utf-8') as file_out:
            json.dump(json_data, file_out, ensure_ascii=False, indent=4)

    def load_json(self, folder_name, json_filename):
        full_filename = os.path.join(folder_name, json_filename)
        with open(full_filename, 'r', encoding='utf-8') as file_in:
            json_data = json.load(file_in)

        if self.is_empty(json_data):
            return {}

        return json_data

    def load(self):
        json_data = self.get_request(self.api_url)

    def get_request(self, url):
        index = self.machine_readable(self.api_url) + ".json"
        if self.file_exists(self.apis_folder, index):
            return self.load_json(self.apis_folder, index)

        response = requests.get(url)
        # print(url)
        # print(response.status_code)
        json_data = response.json()
        self.output_json(self.apis_folder, index, json_data)

        return json_data