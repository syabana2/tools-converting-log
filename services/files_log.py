import json
import sys

class FilesLogService:
    """ a class for processing file like save or create file.
    """

    def __init__(self, type_file: str, output_file: str):
        """
        Args:
            type_file (str): type of file, json or text
            output_file (str): location saving file log has been converted.
        """

        self.type_file = type_file
        self.output_file = output_file

    def save(self, body_log: str or dict):
        """ for saving the file.

        Args:
            body_log (strordict): body which want to write to a file.
        """
        with open(self.output_file, 'w') as output_file:
            if self.type_file == "json":
                json.dump(body_log, output_file)
            else:
                output_file.write(body_log)

    def create_output_file(self):
        """ create file for measuring the folder for saving file exists.
        """
        try:
            with open(self.output_file, "w") as output_file:
                output_file.write('')
        except Exception as e:
            print(e)
            sys.exit(1)
