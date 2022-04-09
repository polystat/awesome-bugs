from typing import Iterable
from dataclasses import dataclass
from pprint import pformat
from typing import Callable
from pathlib import Path
import os


@dataclass()
class AnalyzerReportRow:
    file_path: str
    error_type: str
    error_message: str
    error_position: (int, int) = (0, 0)

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


class AnalyzerReportExceptionRow(AnalyzerReportRow):
    def __init__(
        self,
        file_path,
        error_type="Exception",
        error_message="[An exception was thrown]",
    ):
        self.file_path = file_path
        self.error_type = error_type
        self.error_message = error_message


@dataclass()
class AnalyzerStatistic:
    true_positive: int = 0
    false_positive: int = 0
    true_negative: int = 0
    false_negative: int = 0
    exceptions: int = 0
    accuracy: float = 0
    precision: float = 0
    recall: float = 0
    F1: float = 0

    def dict(self) -> dict:
        return {
            "true_positive": self.true_positive,
            "false_positive": self.false_positive,
            "true_negative": self.true_negative,
            "false_negative": self.false_negative,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "F1": self.recall,
        }


@dataclass()
class ErrorStatistic:
    error: str
    statistic: AnalyzerStatistic


class AnalyzerReport:
    """Class that stores data from a single run of specific static analyzer"""

    results: Iterable[AnalyzerReportRow]
    analyzer: str
    source_path: str
    report_path: str
    error_statistics: list[ErrorStatistic]
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
        self.error_statistics = []
        self.statistic = AnalyzerStatistic()

    def filter(
        self, predicate: Callable[[AnalyzerReportRow], bool]
    ) -> "AnalyzerReport":
        self.results = list(filter(predicate, self.results))
        return self

    def update_statistic(self):
        # Get paths to sources from tests
        source_paths = []
        for root, dirs, files in os.walk(self.source_path):
            if len(dirs) == 0:
                source_paths.append(root.replace("\\", "/"))

        # Split exceptions and results (analyzers messages)
        exceptions, result_paths = [], []
        for x in self.results:
            (exceptions, result_paths)[x.error_type != "Exception"].append(
                # Take only folders name, not files
                x.file_path
                if Path(x.file_path).is_dir()
                else os.path.dirname(x.file_path)
            )

        # Calculation general statistic
        self.statistic = self.calculate_statistic(
            source_paths, result_paths, exceptions
        )

        # Get errors for which test are exist
        with open("tests/errors.txt") as errors_file:
            errors = [x.strip() for x in errors_file.readlines()]

        # Calculation statistic per errors
        for error in errors:
            e_result_paths = [x for x in result_paths if error in x]
            e_source_paths = [x for x in source_paths if error in x]
            e_exceptions = [x for x in exceptions if error in x]
            stat = self.calculate_statistic(
                e_source_paths, e_result_paths, e_exceptions
            )
            self.error_statistics.append(ErrorStatistic(error, stat))

    @staticmethod
    def calculate_statistic(source, results, exceptions):
        stat = AnalyzerStatistic()
        for test in source:
            if test in results:
                if test.find("-bad") != -1:
                    stat.true_positive += 1
                elif test.find("-good") != -1:
                    stat.false_positive += 1
            elif test not in exceptions:
                if test.find("-bad") != -1:
                    stat.false_negative += 1
                elif test.find("-good") != -1:
                    stat.true_negative += 1
        stat.exceptions = len(exceptions)

        total = (
            stat.true_positive
            + stat.true_negative
            + stat.false_positive
            + stat.false_negative
            + stat.exceptions
        )
        positives_count = stat.true_positive + stat.false_positive
        if total != 0:
            stat.accuracy = (stat.true_positive + stat.true_negative) / total

        if positives_count != 0:
            stat.precision = stat.true_positive / positives_count

        if stat.true_positive + stat.false_negative != 0:
            stat.recall = stat.true_positive / (
                stat.true_positive + stat.false_negative
            )

        if stat.precision + stat.recall != 0:
            stat.F1 = (
                2
                * (stat.precision * stat.recall)
                / (stat.precision + stat.recall)
            )

        return stat

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
