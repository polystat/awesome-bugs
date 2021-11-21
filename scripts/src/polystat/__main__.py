from pathlib import Path
import os
import shutil

# Script is being run from the repo root dir

SOURCE_PATH = os.path.join('temp', 'eo')
RESULT_PATH = os.path.join('res', 'eo-out')
POLYSTAT_FILE = 'polystat-1.0-SNAPSHOT-jar-with-dependencies.jar'


def run_polystat():
    shutil.rmtree('temp_polystat', ignore_errors=True)
    for root, dirs, files in os.walk(SOURCE_PATH):
        if len(dirs) == 0:
            case_name = os.path.basename(root)

            # prepare the temp folder
            temp_path = os.path.join('temp_polystat', case_name)
            Path(temp_path).mkdir(parents=True, exist_ok=True)

            # prepare the folder for results
            result_path = os.path.join(RESULT_PATH, case_name)
            Path(result_path).mkdir(parents=True, exist_ok=True)
            res_path = os.path.join(result_path, 'out.txt')

            os.system(f'java -jar {POLYSTAT_FILE} {root} {temp_path} >{res_path}')

    print("Polystat analysis completed")


def main():
    run_polystat()


if __name__ == "__main__":
    main()
