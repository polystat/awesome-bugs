from pathlib import Path
import logging
import os
import yaml
import shutil

# Here we take all yml files and extract source code from them
# In addition check file structure

CODE_PATH = 'temp_YML'
TEMP_PATH = 'temp'

REQUIRED_KEYS = [
    'title',
    'features',
    'language',
    'problem',
    'code',
    'test_type'
]


def get_samples(code_path):
    code_samples_paths = []

    for root, dirs, files in os.walk(code_path):
        for file in files:
            if file.endswith('.yml'):
                code_samples_paths.append(os.path.join(root, file))

    return code_samples_paths


def check_file_structure(file_content, file_name):
    for key in REQUIRED_KEYS:
        if key not in file_content.keys():
            logging.warning(f'file {file_name} does not contain {key} required section')


def get_code_samples(paths):
    for path in paths:
        print(f'Prepare file: {path}')
        try:
            get_code_sample(path)
        except yaml.YAMLError as exc:
            print(exc)
        except IOError:
            print('An IOError has occurred!')


def get_code_sample(path):
    with open(path, 'r') as stream:
        data = yaml.safe_load(stream)

    lang = data['language']
    file_name = os.path.basename(path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    check_file_structure(data, file_name)

    # for lang in languages:
    lang_section = 'code'
    if lang_section in data.keys():
        code_files = data[lang_section]
        lang_code_path = os.path.join(TEMP_PATH, lang)

        Path(lang_code_path).mkdir(parents=True, exist_ok=True)

        #
        if isinstance(code_files, dict):
            for name, code in code_files.items():
                lang_file_name = file_name_without_ext + '_' + name + '.' + lang

                with open(os.path.join(lang_code_path, lang_file_name), 'w') as f:
                    f.write(code)
        else:
            code = code_files
            lang_file_name = file_name_without_ext + '.' + lang

            with open(os.path.join(lang_code_path, lang_file_name), 'w') as f:
                f.write(code)
    else:
        logging.warning(f'file {file_name} does not contain code a sample for {lang}')


def run():
    code_samples = get_samples(CODE_PATH)
    print(f'detected files: {str(code_samples)}')

    shutil.rmtree(TEMP_PATH, ignore_errors=True)
    get_code_samples(code_samples)

    print('Done!')


if __name__ == '__main__':
    run()
