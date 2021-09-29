import os
import csv
from typing import Iterable
from dataclasses import dataclass
import json
from pprint import pformat


@dataclass(frozen=True)
class AnalyzerReportRow:
    file: str
    line_number: int
    column_number: int
    error_type: str
    error_message: str

    def dict(self) -> dict:
        return {
            "file": self.file,
            "line_number": self.line_number,
            "column_number": self.column_number,
            "error_type": self.error_type,
            "error_message": self.error_message,
        }


class AnalyzerReport:
    """Class that stores data from a single run of specific static analyzer"""

    def __init__(self,
                 results: Iterable[AnalyzerReportRow],
                 analyzer: str,
                 report_path: str
                 ):
        """Results hold a list of tuples with results. The format is:
        [(code_sample, file, code_line, error_type, source_ref_line), ...]
        source_ref_line is a line number inside the report"""

        self.results = results

        self.analyzer = analyzer
        """Analyzer id"""

        self.report_path = report_path
        """Report location. Can be either path to a URL or an artifact"""

    def save(self, dir_path, file_name=None):
        """Save results to csv file and other fields in json file.
        Default file name is <analyzer_name>.(csv|json)"""
        if file_name is None:
            file_name = self.analyzer

        csv_path = os.path.join(os.path.abspath(dir_path), file_name) + ".csv"
        json_path = os.path.join(os.path.abspath(dir_path), file_name) + ".json"
        with open(json_path, "w") as f:
            json.dump([r.dict() for r in self.results], f)

        with open(csv_path, "w") as f:
            field_names = [
                "file",
                "line_number",
                "column_number",
                "error_type",
                "error_message",
            ]
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            for r in self.results:
                writer.writerow(r.dict())

    def __str__(self) -> str:
        return (
            f"""AnalyzerReport(
    analyzer={self.analyzer},
    report_path={self.report_path},
    results={pformat(self.results)}
)"""
        )

    def __repr__(self):
        return str(self)
