import os
import sys
import re
from pathlib import Path

# Script is being run from the repo root dir

# The script forms yml files form sources files
# As input it takes:
#  - a path to folder with source files
#  - a path for resulting yaml files


YML_TEMPLATE = '''title: {title}
description: 
features: 
problem: {problem}
language: {language}
test_type: {test_type}
code: {code}
eoCode: |
  {eoCode}'''

BAD_GOOD_CODE_TEMPLATE = \
    '''
    bad: |
        {bad}
    good: |
        {good}
    '''

FILE_FILTERS = [
    r'.*\.eo',
    r'.*\.ya?ml'
]


def generate_yml_files_safe(in_path, out_path):
    try:
        generate_yml_files(in_path, out_path)
    except IOError:
        print('An IOError has occurred!')


def generate_yml_files(in_path, out_path):
    for root, dirs, files in os.walk(in_path):
        if len(dirs) == 0:
            # exclude good if paired bad case exists
            files = exclude_good(files, root)

            files = list(
                filter(
                    lambda f: all(
                        re.fullmatch(f_filter, f) is None
                        for f_filter in FILE_FILTERS
                    ),
                    files
                )
            )

            for file in files:
                print(
                    'processing {} ... '.format(os.path.join(root, file)),
                    end=''
                )

                process_file(root, file, out_path)

                print('OK')

    print('Yaml files generated')


# If good case is linked with bad one, we shouldn't process it, so exclude
def exclude_good(files, root):
    cleared_list = []
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        bad_case = os.path.join(root, file_name[:-5] + file_extension)
        if file_name.endswith('_good') and os.path.isfile(bad_case):
            continue
        else:
            cleared_list.append(file)

    return cleared_list


def process_file(root, file, out_path):
    file_path = os.path.join(root, file)

    with open(file_path, 'r') as fr:
        raw_code = fr.readlines()
        yml_file_path = os.path.join(out_path, root)
        folder_name = os.path.basename(root)
        file_name, file_extension = os.path.splitext(file)
        yml_file_name = file_name + '.yml'
        ext = file_extension

        Path(yml_file_path).mkdir(parents=True, exist_ok=True)

        test_type = get_test_type(root, file_name, file_extension)

        # form code section
        if test_type == 'mixed':
            code = form_mixed_code(root, file_name, file_extension, raw_code)
        else:
            code = '|\n    ' + '    '.join(raw_code)

        # get eo code if exists
        eo_code = get_eo_code(root, file_name)

        # generate and create yml file
        with open(os.path.join(yml_file_path, yml_file_name), 'w') as fw:
            file_content = YML_TEMPLATE.format(
                title=file_name,
                code=code,
                language=ext[1:],
                problem=folder_name,
                test_type=test_type,
                eoCode='  '.join(eo_code)
            )
            fw.write(file_content)


def get_eo_code(root, file_name):
    eo_code = ''
    eo_path = os.path.join(root, file_name + '.eo')
    if os.path.isfile(eo_path):
        with open(eo_path, 'r') as f:
            eo_code = f.readlines()

    return eo_code


def get_test_type(root, file_name, file_ext):
    # with assumption that paired good cases was excluded
    if file_name.endswith('_good'):
        return 'good'

    possible_good_case = os.path.join(root, file_name + '_good' + file_ext)

    if os.path.isfile(possible_good_case):
        return 'mixed'
    else:
        return 'bad'


def form_mixed_code(root, file_name, file_extension, code_bad_case):
    good_path = os.path.join(root, file_name + '_good' + file_extension)
    with open(good_path, 'r') as f:
        code_good_case = f.readlines()

    return BAD_GOOD_CODE_TEMPLATE.format(
        bad=(' ' * 8).join(code_bad_case),
        good=(' ' * 8).join(code_good_case)
    )


def main():
    # IN = 'tests'
    # OUT = 'temp_YML'
    # generate_yml_files(IN, OUT)

    if len(sys.argv) == 3:
        generate_yml_files_safe(sys.argv[1], sys.argv[2])
    else:
        print('Wrong parameters')


if __name__ == '__main__':
    main()
