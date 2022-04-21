import subprocess
import os
import sys

# Here we make Polystat analysis

# As an input it takes:
#  - a path to polystat.jar file
#  - a path to a folder with .eo source files
#  - a path to a folder where a report will be generated
#  - tag, appended to the report name


def run_polystat(polystat_file, sources_folder_path, result_folder_path, report_tag):
    results = []
    # Run Polystat analysis for each test case
    for root, dirs, files in os.walk(sources_folder_path):
        if len(dirs) == 0:
            print(f"Polystat analyze the file: {root}")
            case_name = os.path.basename(root)
            output = subprocess.run(
                ["java", "-jar", polystat_file, root, "--sarif"],
                capture_output=True,
                encoding="latin1",
            )
            path = os.path.join(sources_folder_path, case_name)
            case_result = path + "\n" + output.stdout
            print(output.stderr)
            results.append(case_result)

    # Write results to file
    result_file_path = os.path.join(result_folder_path, "polystat-" + report_tag + "-out.txt")
    with open(result_file_path, "w") as fw:
        fw.write("".join(sorted(results)))
    print("Polystat analysis completed")


def main():
    # Read arguments
    if len(sys.argv) == 5:
        polystat_file = sys.argv[1]
        sources_folder_path = sys.argv[2]
        result_folder_path = sys.argv[3]
        report_tag = sys.argv[4]
    else:
        print("Wrong number of arguments")
        return

    run_polystat(polystat_file, sources_folder_path, result_folder_path, report_tag)


if __name__ == "__main__":
    main()
