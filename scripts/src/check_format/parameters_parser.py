import logging
import os
import re

# Script is being run from the repo root dir
CODE_PATH = "code"
COMMON_FILES = ["README.md"]
ARTIFACT_NAME = "samples_parameters.json"
ARTIFACT_PATH = "./samples_parameters.json"

FILE_FILTERS = [
    r".*\.eo",  # EO translations
    r"filters\.txt"  # error filters
]


def analyze_dirs(code_path):
    code_samples_paths = []

    for root, dirs, files in os.walk(code_path):
        # Finding leaf dirs
        if len(dirs) == 0:

            filtered_files = list(filter(
                lambda f: all(re.fullmatch(f_filter, f) is None for f_filter in FILE_FILTERS),
                files
            ))

            # Checking if structure is correct
            if "README.md" not in filtered_files:
                logging.error(
                    f"Path '{root}' should contain code sample, but there is no README.md (it is case sensitive)")
                return None

            if len(filtered_files) == 1:
                logging.error(f"Path '{root}' does not contain source file")
                return None

            if len(filtered_files) > 2:
                logging.error(f"Path '{root}' contains more than one source files")
                return None

            # This code sample is OK
            code_samples_paths.append(root)

    return code_samples_paths


def detect_code_samples(code_path):
    return analyze_dirs(code_path)


def check_if_lines(input_str):
    raw_line_numbers = input_str.split(",")
    line_numbers = []
    for raw_line_no in raw_line_numbers:
        try:
            line_numbers.append(int(raw_line_no))
        except Exception:
            return False
    return True


def preprocess_lines(input_str):
    raw_line_numbers = input_str.split(",")
    line_numbers = []
    for raw_line_no in raw_line_numbers:
        line_numbers.append(int(raw_line_no))
    return line_numbers


# Structure: { parameter_name : (is_required : bool ,
#                                checker : (input_str) => bool), 
#                                preprocessor : (input_str) => Object }
allowed_parameters = {
    "Name": {
        "is_required": False,
        "checker": None,
        "preprocessor": None,
    },
    "FailureType": {
        "is_required": False,
        "checker": None,
        "preprocessor": None,
    },
    "ErrorType": {
        "is_required": False,
        "checker": None,
        "preprocessor": None,
    },
    "Source": {
        "is_required": False,
        "checker": None,
        "preprocessor": None,
    },
    "CodeType": {
        "is_required": True,
        "checker": None,
        "preprocessor": None,
    },
    "Lines": {
        "is_required": True,
        "checker": check_if_lines,
        "preprocessor": preprocess_lines,
    },
}


def parse_input(text: str):
    # Extracting strings with parameters

    blocks = re.findall(r"```((.|\n)*)```", text, flags=re.MULTILINE)

    if len(blocks) == 0:
        logging.error("Header is not found")
        exit(1)

    logging.debug(text)

    logging.debug("found block '{}'".format(blocks[0][0]))
    logging.debug(blocks)

    parameters_matches = re.findall(r"#\s*(\w*)\s*:(.*)", blocks[0][0])

    logging.debug(parameters_matches)

    parameters = {}

    # Building parameters dict and checking if paramaters are allowed

    for match in parameters_matches:
        logging.debug(match[0])
        logging.debug(match[1].strip())

        if match[0] in parameters.keys():
            logging.error(f"Repeating parameter {match[0]}!")
            return None

        parameters[match[0]] = match[1].strip()

    return parameters


def validate_input(parameters):
    # Checking if paramaters are allowed

    for key, value in parameters.items():
        if key not in allowed_parameters.keys():
            logging.error(f"Parameter {key} is not allowed!")
            return False

    # Checking if all mandatory parameters are in place

    for key, value in allowed_parameters.items():
        if value["is_required"] and key not in parameters.keys():
            logging.error(f"Required parameter {key} not found!")
            return False

    # Validating parameters values

    for key, value in parameters.items():

        if allowed_parameters[key]["checker"] is None:
            continue

        if not allowed_parameters[key]["checker"](value):
            logging.error(f"Parameter '{key}' has an incorrect value ({value})!")
            return False

    # We are OK

    return True


def preprocess_input(parameters):
    """Preprocesses input. Modifies input dict!"""
    for key, value in parameters.items():
        if allowed_parameters[key]["preprocessor"] is None:
            continue
        parameters[key] = allowed_parameters[key]["preprocessor"](value)
    return parameters
