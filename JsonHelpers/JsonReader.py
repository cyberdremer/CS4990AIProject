import json
import os


class JsonReader:
    def __init__(self):
        self.json_data = {}

    def read_in_data(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    self.json_data[filename[:-5]] = json.load(file)

        return self.json_data




