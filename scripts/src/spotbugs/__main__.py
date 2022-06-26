import subprocess
import os
import sys

# Here we make Spotbugs analysis

# As an input it takes:
#  - a path to spotbugs.jar file
#  - a path to a folder with .java source files
#  - a path to a folder where a report will be generated


def run_spotbugs(spotbugs_file, sources_folder_path, result_folder_path):
    results = []
    # Run Spotbugs analysis for each test case
    for root, dirs, files in os.walk(sources_folder_path):
        if len(dirs) == 0:
            print(f"Spotbugs analyze the file: {root}")
            case_name = os.path.basename(root)
            if len(files) == 1:
                # create .jar with debug info
                output = subprocess.run(
                    ["javac", os.path.join(root, files[0]), "-g"],
                    capture_output=True,
                    encoding="latin1",
                )
                print(output.stderr)
            output = subprocess.run(
                ["java", "-jar", spotbugs_file, "-textui", "-sarif", root],
                capture_output=True,
                encoding="latin1",
            )
            path = os.path.join(sources_folder_path, case_name)
            case_result = path + "\n" + output.stdout + "\n"
            print(output.stderr)
            results.append(case_result)

    # Write results to file
    result_file_path = os.path.join(result_folder_path, "spotbugs-out.txt")
    with open(result_file_path, "w") as fw:
        fw.write("\n".join(sorted(results)))
    print("Spotbugs analysis completed")


def main():
    # Read arguments
    if len(sys.argv) == 4:
        spotbugs_file = sys.argv[1]
        sources_folder_path = sys.argv[2]
        result_folder_path = sys.argv[3]
    else:
        print("Wrong number of arguments")
        return

    run_spotbugs(spotbugs_file, sources_folder_path, result_folder_path)


if __name__ == "__main__":
    main()
