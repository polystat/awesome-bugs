from pathlib import Path
import logging
import os
import sys
import yaml
import shutil
from scripts.src.utilities import get_test_files_paths

# Here we take all YAML files from the input folder, if files have
# the correct structure - extract source code from them and write
# them to the resulting folder

# As an input it takes:
#  - a path to a folder with YAML files
#  - a path to a resulting temp folder with source files

# According to the README.md we should have such fields in our YAML files
REQUIRED_KEYS = ["title", "description", "features", "bad", "good"]


# Path (file) processing
def process_file(file_path, out_path):
    # Read file
    with open(file_path, "r") as stream:
        file_content = yaml.safe_load(stream)

    # Checking if all required keys exist
    # If the file doesn't contain at least one key - the file
    # will not be processed
    absent_keys = get_absent_keys(file_content)
    if len(absent_keys) > 0:
        logging.warning(
            f"file {file_path} does not contain"
            f" {str(absent_keys)} required section"
        )
        return False

    # extract source files (bad and good cases)
    source_files = (
        get_sources(file_content, "bad") +
        get_sources(file_content, "good")
    )

    # Write given sources to resulting folder
    write_sources(source_files, file_path, out_path)


# Check for required keys
def get_absent_keys(file_content):
    absent_keys = []
    for key in REQUIRED_KEYS:
        if key not in file_content.keys():
            absent_keys.append(key)
    return absent_keys


# Extract source files of given type (bad, good) from the file content
def get_sources(file_content, source_type):
    source_files = []
    for file in file_content[source_type]:
        source_files.append(
            (source_type, file, file_content[source_type][file])
        )
    return source_files


# Write found source files to the result folder
# If the path doesn't exist - it will be created
# The resulting path has such a structure:
# - resulting folder: temp\sources
# - language: cpp
# - case name - case type: mutual-recursion-bad
# - source file name: foo.cpp
# We have such path in the result:
# temp\sources\cpp\mutual-recursion-bad\foo.cpp
def write_sources(source_files, base_file_path, out_path):
    base_file_name = os.path.basename(base_file_path)
    base_file_name_without_ext = os.path.splitext(base_file_name)[0]
    for source_type, file_name, source_content in source_files:
        case_name = base_file_name_without_ext + "-" + source_type
        lang = os.path.splitext(file_name)[-1][1:]
        folder_path = os.path.join(out_path, lang, case_name)
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        full_path = os.path.join(folder_path, file_name)
        with open(full_path, "w") as f:
            f.write(source_content)


def run():
    # Read arguments
    if len(sys.argv) == 3:
        tests_folder_path = sys.argv[1]
        result_folder_path = sys.argv[2]
    else:
        print("Wrong number of arguments")
        return

    # Get file paths
    test_files_paths = get_test_files_paths(tests_folder_path)
    print(f"Detected files: {str(test_files_paths)}")

    # Free the result folder
    shutil.rmtree(result_folder_path, ignore_errors=True)

    # Process found files
    for path in test_files_paths:
        print(f"Process file: {path}")
        process_file(path, result_folder_path)

    print("Source files extracted successfully!")


if __name__ == "__main__":
    run()
