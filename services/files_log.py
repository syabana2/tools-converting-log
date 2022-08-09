import json
import sys

class FilesLogService:
    def __init__(self, type_file: str, output_file: str):
        self.type_file = type_file

        if self.type_file == "json" and output_file == "output.txt":
            self.output_file = "output.json"
        else:
            self.output_file = output_file

    def save(self, body_log: str or dict):
        with open(self.output_file, 'w') as output_file:
            if self.type_file == "json":
                json.dump(body_log, output_file)
            else:
                output_file.write(body_log)

    def create_output_file(self):
        try:
            with open(self.output_file, "w") as output_file:
                output_file.write('')
        except Exception as e:
            print(e)
            sys.exit(1)
