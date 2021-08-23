import logging
import json
import copy

from parser import Parser
from analyzer_results import AnalyzerResults, ResCols
from coverity_parser import CoverityParser

INPUT_ARTIFACT_PATH = "./samples_parameters.json"

if __name__ == "__main__":

	parsers = (
		CoverityParser(),
	)

	analyzer_results = []

	for p in parsers:
		analyzer_results.append(p.parse())

	# Compare to labels

	samples_parameters = None

	with open(INPUT_ARTIFACT_PATH, "r") as f:
		samples_parameters = json.load(f)

	if samples_parameters == None:
		logging.error("Can't load samples parameters!")
		exit(1)

	# In hits and misses 
	# keys are analyzers' names
	# values are list of source_ref_line (can be used as a key for .csv)
	hits = {}
	misses = {}

	# Not found contains plain paths to code samples with undetected errors
	# for each analyzer
	not_found = {}

	for an_res in analyzer_results:

		# XXX : can be resource consuming
		safe_samples_parameters = copy.deepcopy(samples_parameters)

		curr_hits = []
		curr_misses = []
		curr_not_found = set(safe_samples_parameters.keys())

		for res in an_res.results:
			# TODO : Filter out sample specific ignored error types
			params = safe_samples_parameters[res[ResCols.code_sample.value]]

			# Any hit in any specified line = hit in the sample
			if res[ResCols.code_line.value] in params["Lines"] and \
				res[ResCols.code_sample.value] in curr_not_found:

				curr_hits.append(res[ResCols.source_ref_line.value])
				curr_not_found.remove(res[ResCols.code_sample.value])
			else:
				curr_misses.append(res[ResCols.source_ref_line.value])

		hits[an_res.analyzer] = curr_hits
		misses[an_res.analyzer] = curr_misses
		not_found[an_res.analyzer] = list(curr_not_found)


	# Generate artifacts
	for an_res in analyzer_results:
		an_res.save("")

	with open("hits.json", "w+") as f:
		json.dump(hits, f)

	with open("misses.json", "w+") as f:
		json.dump(misses, f)

	with open("not_found.json", "w+") as f:
		json.dump(not_found, f)

	# Generate output
	for an_res in analyzer_results:
		max_hits = len(safe_samples_parameters.keys())
		an_name = an_res.analyzer

		print("'{}' analyzer produced: ".format(an_name))
		print("{} hits ({} of max {})".format(str(len(hits[an_name])), str(len(hits[an_name]) / max_hits), str(max_hits)))
		print("{} ({} of all results)".format(str(len(misses[an_name])), str(len(misses[an_name]) / len(an_res.results))))
		print("{} samples were not found. They are:".format(len(not_found[an_name])))
		print("\n".join(not_found[an_name]))
		print("")

	print("Done!")