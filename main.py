from os.path import exists
from services.log_converter.elasticsearch_log import LogElasticConverterService

import argparse
import sys


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("log_file_path", type=str, help="location filename log, example=var/log/elasticsearch.log")
    ap.add_argument("-o", "--output", required=False, nargs="?", const="output.txt", default="output.txt", type=str, help="output path file, default current path.")
    ap.add_argument("-t", "--type", required=False, nargs="?", const="text", default="text", type=str, help="type output file, default type Text. option: json|text")
    args = vars(ap.parse_args())

    if exists(args["log_file_path"]):
        log_converter_svc = LogElasticConverterService(args["log_file_path"], args["type"], args["output"])

        if args["type"] == "json":
            log_converter_svc.json_format()

        else:
            log_converter_svc.text_format()

    else:
        print("Error: File Not Found!")
        sys.exit(1)

    print(f"Generating {args['type']} log in {args['output']} success..")
