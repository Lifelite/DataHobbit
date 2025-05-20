import argparse
import json
import os
import re
import sys

import xmltodict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.DataHobbit.DCObject import DCObject

tab = "\t"

parser = argparse.ArgumentParser(
    description="Converts XML or JSON files to Dataclass",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    exit_on_error=True,
    add_help=True,
    prog="data_hobbit",
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    help="Direct system path to a JSON, XML or XSD file",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Directory the place output .py file with Dataclass"
)

parser.add_argument(
    "-d",
    "--directory",
    type=str,
    help="Directory to JSON/XSD files, will parse all files within into data classes."
)

parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="Name of parent Dataclass",
)

parser.add_argument(
    "-ad",
    "--apply_defaults",
    type=bool,
    help="Apply default values for all fields using the values within provided JSON/XSD file",
)


def get_default_path(is_input=False, dir_string=None):
    cwd = os.getcwd()
    if dir_string:
        cwd = dir_string

    source_files = []
    for file in os.listdir(cwd):
        if file.endswith(".json"):
            source_files.append(os.path.join(cwd, file))
        elif file.endswith(".xsd"):
            source_files.append(os.path.join(cwd, file))
        elif file.endswith(".xml"):
            source_files.append(os.path.join(cwd, file))

    if source_files and len(source_files) == 1:
        return os.path.join(source_files[0])
    elif source_files and is_input:
        return None
    elif source_files and len(source_files) > 1:
        return source_files
    else:
        raise Exception("No JSON, XML, or XSD files found in current directory.  "
                        "Provide directory or file using --directory or --input")

def parse_file(file_path):
    if file_path.endswith(".json"):
        try:
            with open(args.input, "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            print("Provided input file path does not exist")
            exit(1)
        except json.decoder.JSONDecodeError:
            print("Provided input file path does not contain a valid JSON file or file contains malformed JSON")
            exit(1)
    if file_path.endswith(".xsd") or file_path.endswith(".xml"):
        try:
            with open(file_path, "r") as f:
                return xmltodict.parse(f.read())
        except FileNotFoundError:
            print("Provided input file path does not exist")
            exit(1)
        except Exception as e:
            print(f"There is a problem with the xml in {file_path} or other issue with parsing, more info below:")
            print(f"\t{e}")


parser.set_defaults(
    input=get_default_path(is_input=True),
    output=os.path.join(os.getcwd(), "sample.py"),
    directory=get_default_path(),
    name="GeneratedDataclass"
)

def create_dataclasses(class_name, provided_args, provided_data):
    try:
        dc_builder = DCObject(
            class_name,
            provided_args.apply_defaults,
            provided_data,
            top_parent=True
        )
        if not provided_args.output.endswith(".py"):
            provided_args.output += ".py"
        with open(provided_args.output, "w") as f:
            f.write(dc_builder.build())
            print("File created successfully at {}".format(provided_args.output))
            exit(0)
    except FileNotFoundError:
        print("Provided output file path does not exist")
        exit(1)

args = parser.parse_args()
file_list = None
output_data = []
if args.input:
    output_data.append(parse_file(args.input))

elif args.directory:
    if isinstance(args.directory, str):
        try:
            file_list = get_default_path(dir_string=args.directory)

        except FileNotFoundError:
            print("Provided input file path does not exist")
            exit(1)

    elif isinstance(args.directory, list):
        file_list = args.directory
    for file in file_list:
        output_data.append(parse_file(file))




name = re.findall(r"\S", args.name)

if isinstance(name, list):
    name = "".join(name)
elif not name:
    print("\nProvided name was empty, defaulting back to file name")
    name = None

counter = 0
for data_set in output_data:
    if name:
        name = f"{name}{f"_{counter}" if counter > 0 else ''}"
    elif args.input:
        name = f"{args.input}{f"_{counter}" if counter > 0 else ''}"
    elif file_list:
        try:
            name = os.path.basename(file_list[counter])
            name = name.rsplit(".", 1)[0]
        except IndexError:
            name = None

    create_dataclasses(
        class_name=name,
        provided_args=args,
        provided_data=data_set,
    )
