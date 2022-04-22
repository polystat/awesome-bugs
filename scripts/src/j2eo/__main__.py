import subprocess
import os
import sys

# Here we run J2EO translator

# As an input it takes:
#  - a path to j2eo.jar file
#  - a path to a folder with .java source files
#  - a path to a folder where a .eo will be output
#  - a path to a folder where stdout logs will be saved

def run_j2eo(j2eo_file, sources_folder_path, result_folder_path, stdout_folder_path):
    results = []
    # Run J2EO for all input .java files
    output = subprocess.run(
        ["java", "-jar", j2eo_file, "-o", result_folder_path, sources_folder_path],
        capture_output=True,
        encoding="latin1",
    )
    print(output.stderr)
    results.append(output.stdout)

    # Write results to file
    result_file_path = os.path.join(stdout_folder_path, "j2eo-out.txt")
    with open(result_file_path, "w") as fw:
        fw.write("".join(sorted(results)))
    print("J2EO translation completed")


def main():
    # Read arguments
    if len(sys.argv) == 5:
        j2eo_file = sys.argv[1]
        sources_folder_path = sys.argv[2]
        result_folder_path = sys.argv[3]
        stdout_folder_path = sys.argv[4]
    else:
        print("Wrong number of arguments")
        return

    run_j2eo(j2eo_file, sources_folder_path, result_folder_path, stdout_folder_path)


if __name__ == "__main__":
    main()
