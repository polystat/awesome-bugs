import os
import glob


def filter_defect(f):
    temp_path = os.path.join("tests", "errors.txt")
    with open(temp_path, "r") as r:
        errors = [x.strip() for x in r.readlines() if not x.startswith("-")]
    return any(e in f for e in errors)


def get_test_files_paths(code_path, glob_pattern=''):
    """ Searching for YAML files in the given path.

    :param code_path: root path for tests
    :param glob_pattern: glob to filter files
    :return: absolute paths to found files
    """
    test_case_paths = []
    pattern = glob_pattern if not glob_pattern == '' else '**/*'
    for file in glob.glob(pattern, root_dir=code_path, recursive=True):
        if filter_defect(file) and file.endswith(".yml"):
            test_case_paths.append(os.path.join(code_path, file))
    return test_case_paths
