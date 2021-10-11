import logging
import json
from scripts.src.analyze_reports.report import AnalyzerReport
from scripts.src.report_parsers import ClangTidyParser
from functools import reduce
INPUT_ARTIFACT_PATH = "./samples_parameters.json"


def run():
    logging.basicConfig(level=logging.DEBUG)

    parsers = {
        ClangTidyParser(): [lambda row: row.error_type != "note"]
    }
    analyzer_reports: list[AnalyzerReport] = []

    for parser, preds in parsers.items():
        report = parser.parse()
        for pred in preds:
            report = report.filter(pred)
        analyzer_reports.append(report)

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


if __name__ == "__main__":
    run()
