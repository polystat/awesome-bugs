import subprocess
from pathlib import Path
import os
import sys
import shutil

# Here we make Polystat analysis

# As an input it takes:
#  - a path to polystat.jar file
#  - a path to a folder with .eo source files
#  - a path to a temp folder for interim Polystat processes
#  - a path to a folder where a report will be generated


def run_polystat(polystat_file, sources_folder_path,
                 temp_folder_path, result_folder_path):
    results = []
    shutil.rmtree(temp_folder_path, ignore_errors=True)
    Path(result_folder_path).mkdir(parents=True, exist_ok=True)

    # Run Polystat analysis for each test case
    for root, dirs, files in os.walk(sources_folder_path):
        if len(dirs) == 0:
            print(f"Polystat analyze the file: {root}")
            case_name = os.path.basename(root)

            # Prepare the temp folder
            temp_path = os.path.join(temp_folder_path, case_name)
            Path(temp_path).mkdir(parents=True, exist_ok=True)

            output = subprocess.run([
                "java",
                "-jar",
                polystat_file,
                "--sarif",
                root,
                temp_path,
            ],
                capture_output=True
            )
            case_result = temp_path + "\n" + output.stdout.decode("latin1")
            print(output.stderr.decode("cp1250"))
            results.append(case_result)

    # Write results to file
    result_file_path = os.path.join(result_folder_path, "eo-out.txt")
    with open(result_file_path, "w") as fw:
        fw.write("".join(sorted(results)))

    print("Polystat analysis completed")


def main():
    # Read arguments
    if len(sys.argv) == 5:
        polystat_file = sys.argv[1]
        sources_folder_path = sys.argv[2]
        temp_folder_path = sys.argv[3]
        result_folder_path = sys.argv[4]
    else:
        print("Wrong number of arguments")
        return

    run_polystat(polystat_file, sources_folder_path,
                 temp_folder_path, result_folder_path)


if __name__ == "__main__":
    main()
