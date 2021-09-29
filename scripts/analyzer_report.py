import os
import csv
from enum import Enum


class ResCols(Enum):
    code_sample = 0
    file = 1
    code_line = 2
    error_type = 3
    source_ref_line = 4


class AnalyzerReport:
    """Class that stores data from a single run of specific static analyzer"""

    def __init__(self, results, analyzer, report_ref):
        """Results hold a list of tuples with results. The format is:
        [(code_sample, file, code_line, error_type, source_ref_line), ...]
        source_ref_line is a line number inside the report"""

        self.results = results

        # Invariant: results are always validated
        if not AnalyzerReport.validate_results(results):
            raise ValueError(f"Results values for report '{report_ref}' by '{analyzer}' are in incorrect format!")

        self.analyzer = analyzer
        """Analyzer id"""

        self.report_ref = report_ref
        """Report location. Can be either path ot URL to an artifact"""

    def save(self, dir_path, file_name=None):
        """Save results to csv file and other fields in json file.
        Default file name is <analyzer_name>.(csv|json)"""
        if file_name is None:
            file_name = self.analyzer

        csv_path = os.path.join(dir_path, file_name) + ".csv"
        json_path = os.path.join(dir_path, file_name) + ".json"
        with open(csv_path, "w+") as f:
            csv_writer = csv.writer(f)
            for r in self.results:
                csv_writer.writerow(r)

    @staticmethod
    def validate_results(raw_results):
        return all([
            # Check if it is list
            isinstance(raw_results, list),
            # Ensuring it contains tuples of specific length
            all([isinstance(t, tuple) and len(t) == 5 and all([
                # Check data types
                isinstance(t[ResCols.code_sample.value], str),
                isinstance(t[ResCols.file.value], str),
                isinstance(t[ResCols.code_line.value], int),
                isinstance(t[ResCols.error_type.value], str),
                isinstance(t[ResCols.source_ref_line.value], int), ]) for t in raw_results]),
        ])
