from scripts.src.check_format.parameters_parser import *
import json


def run():
    logging.basicConfig(level=logging.INFO)

    logging.debug(f"Current working dir: {os.getcwd()}")

    paths = detect_code_samples(CODE_PATH)
    print(f"detected code samples: {str(paths)}")

    samples_parameters = {}

    for sample_path in paths:
        readme_path = os.path.join(sample_path, "README.md")
        with open(readme_path, "r") as f:
            print(
                "processing {} ... ".format(sample_path),
                end="",
            )

            text = f.read()
            parameters = parse_input(text)

            if parameters is None or not validate_input(parameters):
                exit(1)

            parameters = preprocess_input(parameters)

            samples_parameters[sample_path] = parameters

            print("OK")

    logging.info("Saving parameters to the file")

    with open(ARTIFACT_PATH, "w+") as artifact_file:
        json.dump(samples_parameters, artifact_file, indent=4)

    print("Done!")


if __name__ == "__main__":
    run()
