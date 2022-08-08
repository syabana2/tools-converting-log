from os.path import exists

import argparse


def checkFile(file):
    return exists(file)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument('file')
    ap.add_argument("-o", "--output", required=False, nargs="?", const=".", default=".", type=str, help="output path file, default current path.")
    ap.add_argument("-t", "--type", required=False, nargs="?", const="text", default="text", type=str, help="type output file, default type Text.")
    args = vars(ap.parse_args())

    if checkFile(args["file"]):
        print("File Found!")
    else:
        print("Error: File Not Found!")
