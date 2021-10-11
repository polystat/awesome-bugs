import os
import csv
from typing import Iterable
from dataclasses import dataclass
import json
from pprint import pformat
from typing import Callable


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

    results: Iterable[AnalyzerReportRow]
    analyzer: str
    report_path: str

    def __init__(
        self, results: Iterable[AnalyzerReportRow], analyzer: str, report_path: str
    ):
        self.results = results
        self.analyzer = analyzer
        self.report_path = report_path

    def filter(
        self, predicate: Callable[[AnalyzerReportRow], bool]
    ) -> "AnalyzerReport":
        self.results = list(filter(predicate, self.results))
        return self

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
        return f"""AnalyzerReport(
    analyzer={self.analyzer},
    report_path={self.report_path},
    results={pformat(self.results)}
)"""

    def __repr__(self):
        return str(self)
