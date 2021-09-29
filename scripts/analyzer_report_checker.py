import copy
import json
import logging
import re

# from coverity_parser import CoverityParser
from filters import read_sample_filters, read_global_filters
from typing import Iterable
from analyzer_report import AnalyzerReport, AnalyzerReportRow
from report_parsers import ClangTidyParser
INPUT_ARTIFACT_PATH = "./samples_parameters.json"


def filter_error_types(
        plain_res: Iterable[AnalyzerReportRow],
        global_filters: list[str],
        filters_by_sample: dict[str, list[str]]
):
    """
    plain_res - list of tuples of analyzer's results
    filters - lists of regex filters
    returns a new list with filtered input
    """
    filtered_res = []

    for r in plain_res:
        ok = True

        sample_path = r.file
        error_type_val = r.error_type

        for fltr in global_filters:
            if re.fullmatch(fltr, error_type_val) is not None:
                ok = False

        for fltr in filters_by_sample[sample_path]:
            if re.fullmatch(fltr, error_type_val) is not None:
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

        params = safe_samples_parameters[res.file]

        # Any hit in any specified line = hit in the sample
        if res.line_number in params["Lines"] and \
                res.file in curr_not_found:

            curr_hits.append(res.line_number)
            curr_not_found.remove(res.file)
        else:
            curr_misses.append(res.line_number)

    return {
        "hits": curr_hits,
        "misses": curr_misses,
        "not_found": list(curr_not_found),
    }


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    parsers = (
        # CoverityParser(),
        ClangTidyParser(),
    )

    analyzer_reports: list[AnalyzerReport] = []

    for p in parsers:
        analyzer_reports.append(p.parse())

    # Compare to labels
    try:
        with open(INPUT_ARTIFACT_PATH, "r") as f:
            samples_parameters = json.load(f)
    except FileNotFoundError as e:
        logging.error("Can't load samples parameters!")
        exit(1)

    # Retrieving filters
    # filters_by_sample = {}
    #
    # for sample_path in samples_parameters.keys():
    #     filters_by_sample[sample_path] = read_sample_filters(sample_path)
    #
    # global_filters = read_global_filters()

    # In hits and misses
    # keys are analyzers' names
    # values are list of source_ref_line (can be used as a key for .csv)
    hits = {}
    misses = {}

    # Not found contains plain paths to code samples with undetected errors
    # for each analyzer
    not_found = {}

    # for an_rep in analyzer_reports:
    #     filtered_results = filter_error_types(an_rep.results, global_filters, filters_by_sample)
    #
    #     stat = check_for_any_hit(samples_parameters, filtered_results, global_filters, filters_by_sample)
    #
    #     hits[an_rep.analyzer] = stat["hits"]
    #     misses[an_rep.analyzer] = stat["misses"]
    #     not_found[an_rep.analyzer] = stat["not_found"]

    # Generate artifacts
    for an_rep in analyzer_reports:
        an_rep.save(".")  # to the working directory

    with open("hits.json", "w+") as f:
        json.dump(hits, f)

    with open("misses.json", "w+") as f:
        json.dump(misses, f)

    with open("not_found.json", "w+") as f:
        json.dump(not_found, f)

    # Generate output
    # for an_rep in analyzer_reports:
    #     max_hits = len(samples_parameters.keys())
    #     an_name = an_rep.analyzer
    #
    #     print("'{}' analyzer produced: ".format(an_name))
    #     print(
    #         f"{len(hits[an_name])} hits ({len(hits[an_name]) / max_hits} of max {max_hits})")
    #     print(
    #         f"{len(misses[an_name])} ({len(misses[an_name]) / len(an_rep.results)} of all results)")
    #     print(f"{len(not_found[an_name])} samples were not found. They are:\n")
    #     print("\n".join(not_found[an_name]))
    #     print()

    print("Done!")
