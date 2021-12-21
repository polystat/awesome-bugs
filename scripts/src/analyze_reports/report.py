from typing import Iterable
from dataclasses import dataclass
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
    hits: int
    misses: int

    def __init__(
        self,
        results: Iterable[AnalyzerReportRow],
        analyzer: str,
        report_path: str,
        hits: int,
        misses: int,
    ):
        self.results = results
        self.analyzer = analyzer
        self.report_path = report_path
        self.hits = hits
        self.misses = misses

    def filter(
        self, predicate: Callable[[AnalyzerReportRow], bool]
    ) -> "AnalyzerReport":
        self.results = list(filter(predicate, self.results))
        return self

    def __str__(self) -> str:
        return f"""AnalyzerReport(
    analyzer={self.analyzer},
    report_path={self.report_path},
    results={pformat(self.results)},
    hits={self.hits},
    misses={self.misses}
)"""

    def __repr__(self):
        return str(self)
