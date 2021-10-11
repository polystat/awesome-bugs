import copy
import re
from typing import Iterable

from scripts.src.analyze_reports.report import AnalyzerReportRow


def filter_error_types(
    plain_res: Iterable[AnalyzerReportRow],
    global_filters: list[str],
    filters_by_sample: dict[str, list[str]],
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
        if res.line_number in params["Lines"] and res.file in curr_not_found:

            curr_hits.append(res.line_number)
            curr_not_found.remove(res.file)
        else:
            curr_misses.append(res.line_number)

    return {
        "hits": curr_hits,
        "misses": curr_misses,
        "not_found": list(curr_not_found),
    }
