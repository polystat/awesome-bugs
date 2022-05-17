import os


def filter_defect(f):
    temp_path = os.path.join("tests", "errors.txt")
    with open(temp_path, "r") as r:
        errors = [x.strip() for x in r.readlines() if not x.startswith("-")]
    return any(e in f for e in errors)


# Searching for YAML files in the given path
def get_test_files_paths(code_path):
    test_case_paths = []
    for root, dirs, files in os.walk(code_path):
        for file in files:
            if filter_defect(file) and file.endswith(".yml"):
                test_case_paths.append(os.path.join(root, file))
    return test_case_paths
