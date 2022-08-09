from os.path import exists
from services.log_converter.elasticsearch_log import LogElasticConverterService
from services.files_log import FilesLogService

import argparse
import sys


def main():
    """ main function for process converting log.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("log_file_path", type=str, help="location filename log, example=var/log/elasticsearch.log")
    ap.add_argument("-o", "--output-file", required=False, nargs="?", const="output.txt", default="output.txt", type=str, help="output path file, default current path.")
    ap.add_argument("-t", "--type-file", required=False, nargs="?", const="text", default="text", type=str, help="type output file, default type Text. option: json|text")
    args = vars(ap.parse_args())

    if exists(args["log_file_path"]):
        if args["type_file"] not in ("json", "text"):
            args["type_file"] == "text"

        if args["type_file"] == "json" and args["output_file"] == "output.txt":
            args["output_file"] = "output.json"

        log_converter_svc = LogElasticConverterService(args["log_file_path"], args["type_file"])
        files_log_svc = FilesLogService(args["type_file"], args["output_file"])
        files_log_svc.create_output_file()

        body_logs = log_converter_svc.process()

        files_log_svc.save(body_logs)

    else:
        print("Error: File Not Found!")
        sys.exit(1)

    print(f"Converting {args['log_file_path']} in {args['output_file']} success..")


if __name__ == "__main__":
    main()
