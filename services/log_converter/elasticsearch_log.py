from tkinter.messagebox import NO
from templates_format import text

import json
import re


class LogElasticConverterService:
    def __init__(self, log_file_path: str, type: str, output: str):
        self.log_file_path = log_file_path
        self.type = type

        if self.type == "json" and output == "output.txt":
            self.output = "output.json"
        else:
            self.output = output

    def get_details_log_elastic(self, log_file_line: str, log_id: str) -> dict:
        log_elastic = {
            "status": False,
            "id": log_id,
            "timestamp": None,
            "level": None,
            "component": None,
            "cluster_name": None,
            "message": None,
            "error_message": None
        }

        match = re.findall(r'\[(.*?)\]', log_file_line)
        if len(match) > 3:
            index_message_from = log_file_line.index(match[3].strip()) + len(match[3]) + 1
            log_elastic["status"] = True
            log_elastic["timestamp"] = match[0].strip()
            log_elastic["level"] = match[1].strip()
            log_elastic["component"] = match[2].strip()
            log_elastic["cluster_name"] = match[3].strip()
            log_elastic["message"] = log_file_line[index_message_from:].strip()
            log_elastic["error_message"] = ''

        return log_elastic

    def json_format(self) -> None:
        with open(self.log_file_path, mode='r') as log_file:
            log_file_lines = log_file.readlines()
            error_status = True
            log_id = 1
            logs = []
            try:
                for log_file_line in log_file_lines:
                    log_elastic = self.get_details_log_elastic(log_file_line, log_id)
                    if log_elastic["status"]:
                        error_status = True

                        del log_elastic["status"]
                        logs.append(log_elastic)

                        log_id = log_id + 1
                    else:
                        if error_status:
                            logs[-1].update({"error_message": log_file_line.strip()})

                        error_status = False

            except Exception as e:
                raise(e)

        with open(self.output, "w") as output_file:
            json.dump(logs, output_file)

    def text_format(self) -> None:
        with open(self.log_file_path, 'r') as log_file:
            log_file_lines = log_file.readlines()
            error_status = True
            log_id = 1

            try:
                with open(self.output, mode="w") as output_file:
                    output_file.write(text.line())
                    for log_file_line in log_file_lines:
                        log_elastic = self.get_details_log_elastic(log_file_line, log_id)
                        if log_elastic["status"]:
                            error_status = True
                            output_file.write(f"id: {log_elastic['id']}\n")
                            output_file.write(f"timestamp: {log_elastic['timestamp']}\n")
                            output_file.write(f"level: {log_elastic['level']}\n")
                            output_file.write(f"component: {log_elastic['component']}\n")
                            output_file.write(f"cluster_name: {log_elastic['cluster_name']}\n")
                            output_file.write(f"message: {log_elastic['message']}\n")

                            if log_elastic["level"] not in ("WARN", "DEBUG"):
                                output_file.write("error_message:\n")
                                output_file.write(text.line())

                            log_id = log_id+1
                        else:
                            if error_status:
                                output_file.write(f"error_message: {log_file_line.strip()}\n")
                                output_file.write(text.line())

                            error_status = False

            except Exception as e:
                raise(e)
