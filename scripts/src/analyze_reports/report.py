from typing import Iterable
from dataclasses import dataclass
from pprint import pformat
from typing import Callable
from pathlib import Path
import os


@dataclass(frozen=True)
class AnalyzerReportRow:
    file_path: str
    error_type: str
    error_message: str

    def dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "error_position": self.error_position,
            "error_type": self.error_type,
            "error_message": self.error_message,
        }

    def __str__(self) -> str:
        row, column = self.error_position
        if row == 0 and column == 0:
            return f"{self.file_path}: {self.error_message}"
        else:
            return (
                f"{self.file_path} {self.error_position}: {self.error_message}"
            )


class AnalyzerStatistic:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int

    def __init__(
        self,
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    ):
        self.true_positive = true_positive
        self.false_positive = false_positive
        self.true_negative = true_negative
        self.false_negative = false_negative

    def dict(self) -> dict:
        return {
            "true_positive": self.true_positive,
            "false_positive": self.false_positive,
            "true_negative": self.true_negative,
            "false_negative": self.false_negative,
        }


class AnalyzerReport:
    """Class that stores data from a single run of specific static analyzer"""

    results: Iterable[AnalyzerReportRow]
    analyzer: str
    source_path: str
    report_path: str
    statistic: AnalyzerStatistic

    def __init__(
        self,
        results: Iterable[AnalyzerReportRow],
        analyzer: str,
        source_path: str,
        report_path: str,
    ):
        self.results = results
        self.analyzer = analyzer
        self.source_path = source_path
        self.report_path = report_path
        self.statistic = AnalyzerStatistic()

    def filter(
        self, predicate: Callable[[AnalyzerReportRow], bool]
    ) -> "AnalyzerReport":
        self.results = list(filter(predicate, self.results))
        return self

    def calculate_statistic(self):
        source_paths = []
        for root, dirs, files in os.walk(self.source_path):
            if len(dirs) == 0:
                source_paths.append(root.replace("\\", "/"))

        result_paths = [
            x.file if Path(x.file).is_dir() else os.path.dirname(x.file)
            for x in self.results
        ]

        stat = self.statistic
        for test in source_paths:
            if test in result_paths:
                if test.find("-bad") != -1:
                    stat.true_positive += 1
                if test.find("-good") != -1:
                    stat.false_positive += 1
            else:
                if test.find("-bad") != -1:
                    stat.false_negative += 1
                if test.find("-good") != -1:
                    stat.true_negative += 1

    def __str__(self) -> str:
        return f"""AnalyzerReport(
    analyzer={self.analyzer},
    source_path={self.report_path},
    report_path={self.report_path},
    results={pformat(self.results)},
    statistic={pformat(self.statistic)},
)"""

    def __repr__(self):
        return str(self)
