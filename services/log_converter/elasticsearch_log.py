from templates_format import text

import re


class LogElasticConverterService:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

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

    def json_format(self) -> dict:
        with open(self.log_file_path, mode='r') as log_file:
            log_file_lines = log_file.readlines()
            error_status = True
            log_id = 1
            body_logs = []
            try:
                for log_file_line in log_file_lines:
                    log_elastic = self.get_details_log_elastic(log_file_line, log_id)
                    if log_elastic["status"]:
                        error_status = True

                        del log_elastic["status"]
                        body_logs.append(log_elastic)

                        log_id = log_id + 1
                    else:
                        if error_status:
                            body_logs[-1].update({"error_message": log_file_line.strip()})

                        error_status = False

                return body_logs

            except Exception as e:
                raise(e)

    def text_format(self) -> str:
        with open(self.log_file_path, 'r') as log_file:
            log_file_lines = log_file.readlines()
            error_status = True
            log_id = 1

            try:
                body_logs = ""
                body_logs += text.line()
                for log_file_line in log_file_lines:
                    log_elastic = self.get_details_log_elastic(log_file_line, log_id)
                    if log_elastic["status"]:
                        error_status = True
                        body_logs += f"id: {log_elastic['id']}\n"
                        body_logs += f"timestamp: {log_elastic['timestamp']}\n"
                        body_logs += f"level: {log_elastic['level']}\n"
                        body_logs += f"component: {log_elastic['component']}\n"
                        body_logs += f"cluster_name: {log_elastic['cluster_name']}\n"
                        body_logs += f"message: {log_elastic['message']}\n"

                        if log_elastic["level"] not in ("WARN", "DEBUG"):
                            body_logs += "error_message:\n"
                            body_logs += text.line()

                        log_id = log_id+1
                    else:
                        if error_status:
                            body_logs += f"error_message: {log_file_line.strip()}\n"
                            body_logs += text.line()

                        error_status = False

                return body_logs

            except Exception as e:
                raise(e)
