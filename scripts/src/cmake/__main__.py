import os

# Script is being run from the repo root dir
CODE_PATH = "code"
CMAKE_TEMPLATE = """
cmake_minimum_required(VERSION 3.20)
project(AwesomeBugs)

set(CMAKE_CXX_STANDARD 14)

add_executable(AwesomeBugs
    {files}
)

"""


def run_cmake():
    if not os.path.exists("build"):
        os.mkdir("build")
    os.system("cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -S . -B build")


def generate_cmakelists():
    paths = []
    for root, dirs, files in os.walk(CODE_PATH):
        if len(dirs) == 0:
            for file in files:
                if file.endswith(".cpp"):
                    paths.append(os.path.join(root, file))

    with open("CMakeLists.txt", "w") as f:
        f.write(CMAKE_TEMPLATE.format(files="\n\t".join(sorted(paths))))


def main():
    generate_cmakelists()
    run_cmake()


if __name__ == "__main__":
    main()
