from parameters_parser import *

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)

	logging.debug("Current working dir: {}".format(os.getcwd()))

	paths = detect_code_samples(CODE_PATH)
	print("detected code samples: {}".format(str(paths)))

	samples_parameters = {}

	for sample_path in paths:
		readme_path = os.path.join(sample_path, "README.md")
		with open(readme_path, "r") as f:
			print("processing {} ... ".format(sample_path), end="")

			text = f.read()
			parameters = parse_input(text)

			if parameters == None or not validate_input(parameters):
				exit(1)

			parameters = preprocess_input(parameters)

			samples_parameters[sample_path] = parameters

			print("OK")

	logging.info("Saving parameters to the file")

	with open(ARTIFACT_PATH, "w+") as artifact_file:
		json.dump(samples_parameters, artifact_file, indent=4)

	print("Done!")