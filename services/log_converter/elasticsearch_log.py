from helper import text
from datetime import datetime

import re


class LogElasticConverterService:
    """ a class used to convert elasticsearch log.
    """

    def __init__(self, log_file_path: str, type_file: str):
        """
        Args:
            log_file_path (str): location log file elasticsearch.
        """

        self.log_file_path = log_file_path
        self.type_file = type_file

    def get_details_log_elastic(self, log_file_line: str, log_id: str) -> dict:
        """extract the information from elastic log.
        key status in 'log_elastic' variable is used for check this log
        is new log or not. for get the status is by converting first string
        surrounded by '[]' to date, if it's success thats mean this is new log.

        Args:
            log_file_line (str): the contents of the log file in one line.
            log_id (str): ID of the log.

        Returns:
            dict: a dict which used for body log elasticsearch.
        """

        log_elastic = {
            "status": False,
            "id": log_id,
            "timestamp": None,
            "level": None,
            "component": None,
            "server_name": None,
            "message": None,
            "error_message": None
        }

        match = re.findall(r'\[(.*?)\]', log_file_line)

        try:
            timestamp_date = match[0].strip().split()[0]

            # convert string to date to check this is new log or not.
            datetime.strptime(timestamp_date, '%Y-%m-%d')

            if len(match) > 3:
                index_message_from = log_file_line.index(match[3].strip()) + len(match[3]) + 1
                log_elastic["status"] = True
                log_elastic["timestamp"] = match[0].strip()
                log_elastic["level"] = match[1].strip()
                log_elastic["component"] = match[2].strip()
                log_elastic["server_name"] = match[3].strip()
                log_elastic["message"] = log_file_line[index_message_from:].strip()
                log_elastic["error_message"] = ''
        except:
            pass

        return log_elastic

    def process(self) -> dict:
        """processing the conversion to text or json formatting.

        Returns:
            dict: body log from the json/text format conversion process.
        """

        with open(self.log_file_path, mode='r') as log_file:
            log_file_lines = log_file.readlines()
            error_status = True
            log_id = 1

            if self.type_file == "json":
                return self.json_format(log_file_lines, error_status, log_id)
            else:
                return self.text_format(log_file_lines, error_status, log_id)

    def json_format(self, log_file_lines, error_status: bool, log_id: int) -> dict:
        """processing log with json format.

        Args:
            log_file_lines (file.read): content of the log line by line.
            error_status (bool): error status check for log level debug or warn.
            log_id (int): id of the log.

        Returns:
            dict: _description_
        """

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

    def text_format(self, log_file_lines, error_status: bool, log_id: int) -> str:
        """processing log with text format.

        Args:
            log_file_lines (file.read): content of the log line by line.
            error_status (bool): error status check for log level debug or warn.
            log_id (int): id of the log.

        Returns:
            dict: _description_
        """

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
                    body_logs += f"server_name: {log_elastic['server_name']}\n"
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
