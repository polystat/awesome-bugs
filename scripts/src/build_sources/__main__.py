import os
import sys

# Here we generate a CMakeLists file based on the CPP sources
# and make a build using it

# As input it takes:
#  - a path to the folder with source files
#  - a path to the resulting build folder


CMAKE_TEMPLATE = """
cmake_minimum_required(VERSION 3.20)
project(AwesomeBugs)

set(CMAKE_CXX_STANDARD 14)

add_executable(AwesomeBugs
    {files}
)
"""


def generate_cmakelists(sources_folder_path):
    paths = []
    # Collect CPP sources
    for root, dirs, files in os.walk(sources_folder_path):
        if len(dirs) == 0:
            for file in files:
                if file.endswith(".cpp"):
                    paths.append(os.path.join(root, file))

    # Insert into CMakeLists file template
    with open("CMakeLists.txt", "w") as f:
        f.write(CMAKE_TEMPLATE.format(files="\n\t".join(sorted(paths))))


def run_cmake(build_folder_path):
    # Create a build folder if not exist
    if not os.path.exists(build_folder_path):
        os.mkdir(build_folder_path)

    # Run building process.
    # DCMAKE_EXPORT_COMPILE_COMMANDS=ON is important because
    # the exported DB will be used by CSA
    os.system("cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -S . -B build")


def main():
    # Read arguments
    if len(sys.argv) == 3:
        sources_folder_path = sys.argv[1]
        build_folder_path = sys.argv[2]
    else:
        print("Wrong number of arguments")
        return

    # Generation CMakeList from CPP source files
    generate_cmakelists(sources_folder_path)
    print("Cmake file generated")

    # Build based on CMakeList file
    run_cmake(build_folder_path)
    print("Cmake build completed")


if __name__ == "__main__":
    main()
