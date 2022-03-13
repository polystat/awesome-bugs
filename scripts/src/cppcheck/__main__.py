import subprocess
from pathlib import Path
import os
import sys

# Here we make Cppcheck analysis

# As an input it takes:
#  - a path to a folder with .cpp source files
#  - a path to a folder where a report will be generated


def run_cppcheck(sources_folder_path, result_folder_path):
    print("Cppcheck analysis started")
    Path(result_folder_path).mkdir(parents=True, exist_ok=True)

    output = subprocess.run(
        [
            "cppcheck",
            sources_folder_path,
            "--template",
            "{file},{line},{column},{severity},{message}",
        ],
        capture_output=True,
        encoding="latin1",
    )
    print(output.stderr)

    # Write results to the file
    result_file_path = os.path.join(result_folder_path, "cppcheck-out.txt")
    with open(result_file_path, "w") as fw:
        fw.write(output.stderr)

    print("Cppcheck analysis completed")


def main():
    # Read arguments
    if len(sys.argv) == 3:
        sources_folder_path = sys.argv[1]
        result_folder_path = sys.argv[2]
    else:
        print("Wrong number of arguments")
        return

    run_cppcheck(sources_folder_path, result_folder_path)


if __name__ == "__main__":
    main()
