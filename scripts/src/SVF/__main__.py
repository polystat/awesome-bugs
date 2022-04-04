import subprocess
from pathlib import Path
import os
import sys
import shutil
import re

# Here we perform SVF analysis

# As an input it takes:
#  - a path to a folder with .cpp source files
#  - a path to a temp folder for .bc files
#  - a path to a folder where resulting file SVF-out.txt will be generated


def run_svf(
    sources_folder_path, bc_folder_path, result_folder_path, svf_bin_path
):
    def svf_check(opt):
        output = subprocess.run(
            ["saber", opt, "-stat=False", full_path],
            env=env,
            encoding="latin1",
            capture_output=True,
        )
        # Getting output and removing unicode color
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        out = ansi_escape.sub("", output.stderr)
        if len(out) > 0:
            print(out)
        result = ""
        if len(out) != 0:
            result = "\n" + out
        return result

    # clear temp folder by removing and creating it
    shutil.rmtree(bc_folder_path, ignore_errors=True)
    Path(bc_folder_path).mkdir(parents=True, exist_ok=True)

    generate_bc_files(sources_folder_path, bc_folder_path)

    # Adding SVF to path
    env = os.environ.copy()
    env["PATH"] = os.path.join(os.getcwd(), svf_bin_path) + ":" + env["PATH"]

    # Run SVF analysis for each test case
    results = []
    for root, dirs, files in os.walk(bc_folder_path):
        for file in files:
            print(f"SVF analyze the file: {file}")
            full_path = os.path.join(root, file)

            # For now, it is not possible to run SVF with all checkers
            # simultaneously, so run one by one and concatenate their results
            case_result = (
                full_path
                + svf_check("-leak")
                + svf_check("-dfree")
                + svf_check("-fileck")
                + "\n"
            )
            results.append(case_result)

    # Write results to file
    Path(result_folder_path).mkdir(parents=True, exist_ok=True)
    result_file_path = os.path.join(result_folder_path, "SVF-out.txt")
    with open(result_file_path, "w") as file:
        file.write("".join(sorted(results)))

    print("SVF analysis completed")


# Generating bc files from .cpp sources
def generate_bc_files(sources_folder_path, bc_folder_path):
    file_paths = get_files(sources_folder_path)
    for path in file_paths:
        full_path = os.path.join(path, "source.cpp")
        case_name = os.path.basename(path)
        bc_path = os.path.join(bc_folder_path, case_name)

        bc_file_path = bc_path + ".bc"
        subprocess.run(
            ["clang", "-c", "-emit-llvm", "-g", full_path, "-o", bc_file_path]
        )


# Extraction of all .cpp sources files from the given path
def get_files(sources_folder_path):
    paths = []
    for root, dirs, files in os.walk(sources_folder_path):
        for file in files:
            if file.endswith(".cpp"):
                paths.append(root)
    return paths


def main():
    # Read arguments
    if len(sys.argv) == 5:
        sources_folder_path = sys.argv[1]
        bc_folder_path = sys.argv[2]
        result_folder_path = sys.argv[3]
        svf_bin_path = sys.argv[4]
    else:
        print("Wrong number of arguments")
        return

    run_svf(
        sources_folder_path, bc_folder_path, result_folder_path, svf_bin_path
    )


if __name__ == "__main__":
    main()
