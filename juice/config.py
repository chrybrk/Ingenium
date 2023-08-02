from juice.core import *

class ConfigurationManager:
    def __init__(self, path):
        self.config_path = path
        self.config = {}

    def change_path(self, new_path):
        self.config_path = new_path
        self.load_config()

    def load_config(self):
        f = open(self.config_path, "r")
        self.config = json.load(f)
        f.close()

    def dump_config(self, head, body, context):
        f = open(self.config_path, "w")

        new_data = self.config
        if head not in new_data.keys(): new_data[head] = {}
        new_data[head][body] = context
        self.config = new_data

        json.dump(self.config, f)
        f.close()

    def get_config(self, head, body, dt): return dt(self.config[head][body])
