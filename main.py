from os.path import exists

import argparse
import re
import json
import sys


def checkFile(file):
    return exists(file)


def readFileJSON(file, path):
    read_file = open(file, 'r')
    lines = read_file.readlines()
    id = 1
    data = []
    try:
        for line in lines:
            match = re.findall(r'\[(.*?)\]', line)
            if len(match) > 3:
                error_status = True
                index_string = line.index(match[3].strip()) + len(match[3]) + 1
                data_entity = {
                    "id": id,
                    "timestamp": match[0].strip(),
                    "level": match[1].strip(),
                    "component": match[2].strip(),
                    "cluster_name": match[3].strip(),
                    "message": line[index_string:].strip(),
                    "error_message": "",
                }

                data.append(data_entity)

                id = id+1

            else:
                if error_status:
                    data[-1].update({"error_message": line.strip()})

                error_status = False


    except Exception as e:
        raise(e)

    with open(path, "w") as file:
        json.dump(data, file)


def readFile(file, path):
    read_file = open(file, 'r')
    lines = read_file.readlines()
    i = 1

    try:
        with open(path, mode="w") as file:
            try:
                file.write("=========================================================================================================================================================\n")
                for line in lines:
                    match = re.findall(r'\[(.*?)\]', line)
                    if len(match) > 3:
                        error_status = True
                        file.write(f"no: {i}\n")
                        file.write(f"timestamp: {match[0].strip()}\n")
                        file.write(f"level: {match[1].strip()}\n")
                        file.write(f"component: {match[2].strip()}\n")
                        file.write(f"cluster_name: {match[3].strip()}\n")

                        index_string = line.index(match[3].strip()) + len(match[3]) + 1

                        file.write(f"message: {line[index_string:].strip()}\n")

                        if match[1].strip() not in ("WARN", "DEBUG"):
                            file.write("error_message:\n")
                            file.write("=========================================================================================================================================================\n")

                        i = i+1
                    else:
                        if error_status:
                            file.write(f"error_message: {line.strip()}\n")
                            file.write("=========================================================================================================================================================\n")

                        error_status = False

            except Exception as e:
                print(e)
                sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument("-o", "--output", required=False, nargs="?", const="./output.txt", default="./output.txt", type=str, help="output path file, default current path.")
    ap.add_argument("-t", "--type", required=False, nargs="?", const="text", default="text", type=str, help="type output file, default type Text.")
    args = vars(ap.parse_args())

    if checkFile(args["file"]):
        if args["type"] == "json":
            if args["output"] == "./output.txt":
                args["output"] = "./output.json"

            readFileJSON(args["file"], args["output"])
        else:
            readFile(args["file"], args["output"])
    else:
        print("Error: File Not Found!")
        sys.exit(1)

    print(f"Generating {args['type']} log in {args['output']} success..")
