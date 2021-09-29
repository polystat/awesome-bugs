import logging
import json
import copy
import re

from parser import Parser
from analyzer_report import AnalyzerReport, ResCols
from coverity_parser import CoverityParser
from filters import read_sample_filters, read_global_filters

INPUT_ARTIFACT_PATH = "./samples_parameters.json"


def filter_error_types(plain_res, global_filters, filters_by_sample):
    """plain_res - list of tuples of analyzer's results and returns a new list with filtered input
    filters - lists of regex filters
    """
    filtered_res = []

    for r in plain_res:
        ok = True

        sample_path = r[ResCols.code_sample.value]
        error_type_val = r[ResCols.error_type.value]

        for f in global_filters:
            if re.fullmatch(f, error_type_val) is not None:
                ok = False

        for f in filters_by_sample[sample_path]:
            if re.fullmatch(f, error_type_val) is not None:
                ok = False

        if ok:
            filtered_res.append(r)

    return filtered_res


def check_for_any_hit(params, results, global_filters, filters_by_sample):
    """Returns dict with 3 lists:
    hits - any error that was found in one of the lines specified in sample parameters
    misses - any error that is not considered a hit
    not_found - errors specified in sample parameters but not found by analyzer
    """

    # XXX : can be resource consuming
    safe_samples_parameters = copy.deepcopy(samples_parameters)

    curr_hits = []
    curr_misses = []
    curr_not_found = set(safe_samples_parameters.keys())

    for res in results:

        params = safe_samples_parameters[res[ResCols.code_sample.value]]

        # Any hit in any specified line = hit in the sample
        if res[ResCols.code_line.value] in params["Lines"] and \
                res[ResCols.code_sample.value] in curr_not_found:

            curr_hits.append(res[ResCols.source_ref_line.value])
            curr_not_found.remove(res[ResCols.code_sample.value])
        else:
            curr_misses.append(res[ResCols.source_ref_line.value])

    return {
        "hits": curr_hits,
        "misses": curr_misses,
        "not_found": list(curr_not_found),
    }


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    parsers = (
        CoverityParser(),
    )

    analyzer_reports = []

    for p in parsers:
        analyzer_reports.append(p.parse())

    # Compare to labels

    samples_parameters = None

    with open(INPUT_ARTIFACT_PATH, "r") as f:
        samples_parameters = json.load(f)

    if samples_parameters == None:
        logging.error("Can't load samples parameters!")
        exit(1)

    # Retreiving filters

    filters_by_sample = {}

    for sample_path in samples_parameters.keys():
        filters_by_sample[sample_path] = read_sample_filters(sample_path)

    global_filters = read_global_filters()

    # In hits and misses
    # keys are analyzers' names
    # values are list of source_ref_line (can be used as a key for .csv)
    hits = {}
    misses = {}

    # Not found contains plain paths to code samples with undetected errors
    # for each analyzer
    not_found = {}

    for an_rep in analyzer_reports:
        filtered_results = filter_error_types(an_rep.results, global_filters, filters_by_sample)

        stat = check_for_any_hit(samples_parameters, filtered_results, global_filters, filters_by_sample)

        hits[an_rep.analyzer] = stat["hits"]
        misses[an_rep.analyzer] = stat["misses"]
        not_found[an_rep.analyzer] = stat["not_found"]

    # Generate artifacts
    for an_rep in analyzer_reports:
        an_rep.save("")  # to the working directory

    with open("hits.json", "w+") as f:
        json.dump(hits, f)

    with open("misses.json", "w+") as f:
        json.dump(misses, f)

    with open("not_found.json", "w+") as f:
        json.dump(not_found, f)

    # Generate output
    for an_rep in analyzer_reports:
        max_hits = len(samples_parameters.keys())
        an_name = an_rep.analyzer

        print("'{}' analyzer produced: ".format(an_name))
        print(
            "{} hits ({} of max {})".format(str(len(hits[an_name])), str(len(hits[an_name]) / max_hits), str(max_hits)))
        print(
            "{} ({} of all results)".format(str(len(misses[an_name])), str(len(misses[an_name]) / len(an_rep.results))))
        print("{} samples were not found. They are:\n".format(len(not_found[an_name])))
        print("\n".join(not_found[an_name]))
        print("")

    print("Done!")
